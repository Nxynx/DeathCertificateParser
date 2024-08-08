from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

import csv
import re
import pandas as pd
import os


# sorts the pdf lltboxes with other boxes close enough to be a possible match for the question above the found line
# takes a path to the desired pdf
# returns a list of a possible question and a possible match
def find_matching_pdf_questions_and_answers(pdf_file_path):
    pdf = open(pdf_file_path, 'rb')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(pdf)
    boxes = []
    matches = []
    pdf.close
    
    for page in pages:
        interpreter.process_page(page)
        layout = device.get_result()
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
                boxes.append(lobj)


    for box in boxes:
        left, bottom, right, top = box.bbox
        # the detection boundary of the y value
        ylimit = bottom - 16
        # the distance that the left side of a question and a answer can be from one another
        xlimit = 16
        for find in boxes:
            leftf, bottomf, rightf, topf = find.bbox
            if bottomf < bottom and bottomf > ylimit:
                if leftf < left + xlimit and leftf > left - xlimit :
                    match = []
                    match.append(box)
                    match.append(find)
                    matches.append(match)
    return matches

def get_questions_and_answers(path_to_answers_we_want, matches):
    questionlist = []
    with open(path_to_answers_we_want, "r", encoding="utf-8") as file:
        for line in file:
            if not line == "\n":
                questionlist.append(line)

    temp = []
    # gets the strings out of the lltboxes from the pdf object
    for match in matches:
        for question in questionlist:
            regex = re.escape(question)
            if re.search(regex, match[0].get_text(), re.IGNORECASE):
                temp.append([match[0].get_text(), match[1].get_text()])
                
    matches = temp
    
    return matches

def sort_list_of_lists(data):
    def extract_key(header):
        header = header.lstrip('*').strip()
        # makes numeric and alpha-numerical parts
        parts = header.split('.', 1)
        if len(parts) == 2:
            # gets numeric part
            num_part = parts[0]
            # gets aplha part
            alpha_part = parts[1].strip()
            
            # gets parts for more accurate sorting
            num_part_digits = ''.join(c for c in num_part if c.isdigit())
            num_part_alpha = ''.join(c for c in num_part if not c.isdigit())
            
            # Return a tuple for sorting
            return (num_part_digits.isdigit(),    # when true numeric part
                int(num_part_digits) if num_part_digits else float('inf'),  # Numeric part
                num_part_alpha,    # Alpha part of numeric
                alpha_part)        # Alpha-numerical part
            
        # if num not found returns false
        return (False, float('inf'), '', header.strip())
    
    sorted_data = sorted(data, key=lambda x: extract_key(x[0]))

    return sorted_data

def make_matches_dict(matches):
    # key is the start of the question, values is the var name to be the key for the answer we find
    # which follows the question in the list of matches
    # this dict is not the final group of matching pairs that gets returned but only used to initialize
    # the var names to be keys in the pairs dict below that will be returned it is the main output of this whole file
    tempname = {
        "1.": "name",
        "2.": "sex",
        "3.": "social_security_number",
        "4a.": "age",
        "6.": "birth_place",
        "7a.": "residence",
        "7b.": "county",
        "7c.": "town_or_city",
        "7d.": "street_and_number",
        "9.":"surviving_spouse",
        "11a.":"fathers_name",
        "11b.":"fathers_birth_place",
        "12a.":"mothers_maiden_name",
        "12b.": "mothers_birth_place",
        "23.":"date_of_death", 
    }
    
    pairs = {}               
    remove = []
    qcount = 0
    # gets rid of duplicate matches if they have more than one \n in the string
    # we have to subtract deletedcount from the next remove[place] to be removed because the total
    # list length is now also shorter by one
    for match in matches:
        for key in tempname:
            regex = re.escape(key)
            if re.search(regex, match[0], re.IGNORECASE):
                newlinechar = 0
                regexx = re.escape("\n")
                for c in match[1]:
                    if re.search(regexx, c, re.IGNORECASE):
                        newlinechar += 1
                
                        
                if newlinechar > 1:
                    remove.append(qcount)

                qcount += 1
    deletedcount = 0
    for num in remove:
        num = num - deletedcount
        del matches[num]
        deletedcount += 1
    
    # pairs the var names with the start of the questions and their following values
    for match in matches:
        for key in tempname:
            regex = rf'\A\*?\s*{re.escape(key)}'
            if re.search(regex, match[0], re.IGNORECASE):
                value = tempname[key]
                pairs[value] = match[1]
                                              
    return pairs

def repl_func(m):
    # process regular expression match groups for word upper-casing problem
    return m.group(1) + m.group(2).upper()

def clean_and_capitalize(matches):
    data = matches
    
    if isinstance(data["name"], str):
        # clean for saving output as csv file
        temp = {}
        for key in data.keys():
            value = data[key]
            value = value.strip("\n")
            value = value.lower()
            s = value
            s = re.sub(r"(^|\s)(\S)", repl_func, s)
            temp[key] = s
        data = temp
        
    matches = data
    
    return matches

# may need a path to the answers, or "answers_file_path"
# returns the matching pdf pairs for pdf to text
def pdf_main_function(pdf_file_path):
    # needs to be current or will not work
    answers_file_path = r"datavalues.txt"
    matches = find_matching_pdf_questions_and_answers(pdf_file_path)
    matches = get_questions_and_answers(answers_file_path, matches)
    sorted_list = sort_list_of_lists(matches)
    matches = sorted_list
    matches = make_matches_dict(matches)
    matches = clean_and_capitalize(matches)
    
    
    return matches 


# function takes data from multiline element in the gui, and the new file paths for 
# a xlsx file and then for a csv file, then writes both files in the path locations
# will return a 0 on success
def output_files_main_function(data, xlsx_file_path, csv_file_path):
    # tests to see if data is probably a dict
    if isinstance(data["name"], str):

        with open(csv_file_path, 'w') as output:
            writer = csv.writer(output)
            for key, value in data.items():
                writer.writerow([key, value])
    
        # writes and opens the xlsx file from the csv file
        df_new = pd.read_csv(str(csv_file_path), encoding='latin-1')
        GFG = pd.ExcelWriter(xlsx_file_path)
        df_new.to_excel(GFG, index=False, header=False)
        GFG._save()

    return 0



# creates the names for the dataframes to use to write the new xlsx file and the new csv files
def make_pdf_files_name_main_function(name_from_data, path_to_folder_for_output):
    path = path_to_folder_for_output
    
    xlsx_name = name_from_data + ".xlsx"
    csv_name = name_from_data + ".csv"
    
    xlsx_file_name = os.path.join(path, xlsx_name)
    csv_file_name = os.path.join(path, csv_name)    
    
    return xlsx_file_name, csv_file_name
