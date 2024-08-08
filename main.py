# Python Script that utilizes PySimpleGui to create a user interface for parsing important data out of a death certificate pdf file 
# the GUI sends the validated file path selected by the other to a sub program "pdf_to_text.py" who's main function pdf_main(file path)
# will then process the pdf and obtain the information that we want (obtained from datavalues.txt) the path to datavalues.txt may need to be
# updated inside of main function of pdf_main in pdf_to_text
# after parsing is completed the returned dictionary is displayed in a preview column on the GUI this column is a editable text window
# the text inside it can be edited and saved or you can open the edited or unedited text inside of excel for pasting into word document merge

import PySimpleGUI as sg
import os

# my own libraries
from pdf_to_text import pdf_main_function
from pdf_to_text import output_files_main_function
from pdf_to_text import make_pdf_files_name_main_function
#
#
#reassembles dictionary from multiline element
def str_to_dict(string):
    lines = str.splitlines(string)
    length = len(lines)
    newdict = {}
    
    for i in range(length):
        line = lines[i]
        
        if i % 3 == 0:
            newdict[line] = lines[i + 1]   
    return newdict



# second argument is for future development of multiple parsing method caparison
# to output the best and most correct results from all methods
# only fulling working method is pdf_miner.six named after the main library that is used

# function runs file through pdf_main if the path for the file is valid
# then prints the results in the output element of the right column in the main window
def run_selected_script(file_path, script):
    results = pdf_main_function(file_path)
        
    return results


# is called by the run_selected_script function to validate the file path
# before the file is sent to pdf main to get parsed and then returned
def validate_file_path(path):
    if os.path.exists(path):
        return True
    return False

def open_theme_window():
    layout_change_theme_window = [
        [sg.T(text="Current Theme:", tooltip="Pressing clear on the main window will update the theme"), sg.T(text=sg.theme(), tooltip="Pressing clear on the main window will update the theme")],
        [sg.Listbox(values=sg.theme_list(), size=(20, 15), key="-theme_list-", tooltip="Pressing clear on the main window will update the theme", enable_events=True)],
        [sg.T("To finish updating the theme clear main window")],
        [sg.Button("Ok", key="-window_theme_ok-")],

    ]
    
    window_change_theme = sg.Window("Theme", layout_change_theme_window, modal=True)
    
    while True:
        event, values = window_change_theme.read()
        
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        
        if event == "-theme_list-":
            sg.theme_global(values['-theme_list-'][0])
            window_change_theme.close()
            open_theme_window()
            
        if event == "-window_theme_ok-":
            window_change_theme.close()
            file_path = ""
            open_settings_window(file_path)
            break
        
    window_change_theme.close()
    
    return
        
            
            
         

    

    


# Called from the settings button on the main window, to open the
# settings sub window, contains the settings options and saves those 
def open_settings_window(file_path):    
    # a sub window of the main window
    # opened by the button settings to open a settings window
    
    current_file_path = ""
    
    if not file_path == "":
        current_file_path = file_path
        

    layout_settings_window = [
        [sg.Input(default_text=current_file_path, key="-custom_save_location-"), sg.FolderBrowse("Change Save Location", key="-change_save_location-")],
        [sg.HSep()],
        [sg.T(text="Current Theme:"), sg.T(text=sg.theme()), sg.Button("Change Theme", key="-change_theme-")],
        [sg.VP()],
        [sg.HSep()],
        [sg.VP()],
        [sg.Button("Save & Exit", key="-save_exit-"), sg.Button("Close", key="-close_settings-")],
    ]

    
    window_settings = sg.Window("Settings", layout_settings_window, modal=True)

    # settings windows event loop
    while True:
        event, values = window_settings.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break            
            
        if event == "-close_settings-":
            break
        
        if event == "-save_exit-":
            Saved = False
            break
            
        if event == "-change_theme-":
            open_theme_window()
            window_settings.close()
        
    window_settings.close()
    
    return


# Creates and launches the gui for the program
# the main window layout is broken down into 3 parts: top row, right column, left column
# the top row is to allow for the selection of a pdf file to be parsed and loaded into the program
# the file browse button is not apart of the left column but the top row

# the left columns is for the buttons that run options scripts to parse the pdf file and create a output or result
# that result is then sent to be displayed in the right column

# the right column is a area to display the result of the pdf file and the selected script
# the result should be editable and the edits should be able to be saved or opened in another program
def main():
    # the main window layout 
    # allows for file selections and scripts to be run on that file
    # a preview of the scripts output should show up in the preview window
    # the preview window should allow the result to be edited before being saved
    # and or opened with another application

    # keys for the main window
    # are commented above window event loop
    layout_main_window = [
        [
            #top row of the main_windows layout, for selecting the input pdf file to then run out scripts on and show the results in the preview window
            [
                [sg.T("PDF File", p=((10, 0), (0, 0))), sg.In(key="-input_file-", expand_x=True), sg.FileBrowse(target="-input_file-", p=((15, 15), (0, 0)), file_types=(("PDF Files", "*.PDF"),))]
            ],
            
            [sg.HSeparator(pad=((0, 0), (15, 15)))],
            [sg.Text("Editor", p=((10, 0), (0, 0)))],
            
            # right side column of the main windows layout, which is also the preview 
            # window for text output and editing said output for corrections
        
            sg.Column(
                        [   
                            [sg.Multiline(default_text="", expand_x=True, expand_y=True, key="-multiline-")]
                        ],
                        expand_y=True,
                        expand_x=True
                        
                    ),
                    
            # left side column of the main window layout, has the buttons for the different programs to be run on the input file
            sg.Column(
                        [
                            [sg.Button("Parse PDF", key="-parse_pdf-")],
                            [sg.Button("Save Parse", key="-save_output-")],
                            [sg.Button("Open in Excel", key="-xlsx-")],
                            [sg.Button("Clear", key="-clear-")],
                            [sg.VStretch()],
                            [sg.VPush()],
                            [sg.HSeparator(pad=((0, 0), (15, 15)))],
                            [sg.VPush()],
                            [sg.VStretch()],               
                            [sg.Button("Settings", key="-open_settings_window-", p=((0, 0), (0, 20)))],
                        ],
                        
                        element_justification="c",
                        size=(110, 800),         
                    ),
        
        ],            
    ]
    
    window_main = sg.Window("Death Certificate Parser", layout_main_window, size=(550, 600), resizable=True)

    parse_finished = False
    results = {}
    multiline_saved = False

    
    # Main windows event loop
    # browse file button: KEY = "-input_file-"
    # parse pdf button: KEY = "-parse_pdf-"
    # settings button: KEY = "-open_settings_window-"
    # save output button: KEY = "-save_output-"
    # open in excel button: KEY = "-xlsx-"
    # multiline column: KEY = "-multiline-"
    # clear button: KEY  = "-clear-"
    while True: 
        event, values = window_main.read()
        
        
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        
        if event == "-parse_pdf-":
            if validate_file_path(values["-input_file-"]):
                # second argument is for future development of multiple parsing method caparison
                # to output the best and most correct results from all methods
                # only fulling working method is pdf_miner.six named after the main library that is used
                # file path is checked by the called script and another function that is called by this one
                results = run_selected_script(values["-input_file-"], "pdf_miner.six")
                
                # prints the key value pair in the multiline element
                if parse_finished:
                    window_main["-multiline-"].update("")
                sg.cprint_set_output_destination(window_main, "-multiline-")
                
                for result in results:
                    sg.cprint(result)
                    sg.cprint(results[result])
                    sg.cprint("")
                
                parse_finished = True
                   
            else:
                sg.popup("Invalid File Path")                
            
        if event == "-open_settings_window-":
            open_settings_window(values["-input_file-"])
            
        if event == "-save_output-":
            if parse_finished:
                results = str_to_dict(values["-multiline-"])
                
                path_to_pdf_file = values["-input_file-"]
                path_to_pdf_files_folder = os.path.dirname(path_to_pdf_file)
                xlsx_files_name, csv_files_name = make_pdf_files_name_main_function(results["name"], path_to_pdf_files_folder)
                
                output_files_main_function(results, xlsx_files_name, csv_files_name)
                multiline_saved = True
            else:
                sg.popup("Please parse a PDF")
        
        # saves and opens the result into excel
        if event == "-xlsx-":
            if multiline_saved:
                results = str_to_dict(values["-multiline-"])
                xlsx_file, csv_file = make_pdf_files_name_main_function(results["name"], path_to_pdf_files_folder)
                
                os.startfile(xlsx_file)
            else:
                sg.popup("Please save the Parse")
                
        if event == "-clear-":
            window_main.close()
            main()
            
    window_main.close()
    
    return

if __name__ == "__main__":
    
    
    main()
    
    ("PDF Files", "*.PDF")

