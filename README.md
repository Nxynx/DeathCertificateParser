# Death Certificate Parser

## Video Demonstration
[![Click to watch the video](https://img.youtube.com/vi/jEx1ik8xk4g/0.jpg)](https://www.youtube.com/watch?v=jEx1ik8xk4g)

## Description
When starting on this project, my original plan was to use an optical character recognition engine to parse a picture taken from a phone or a photo scan of an official Idaho death certificate. After the photo was taken and parsed, the program would then return a CSV and XLSX file of the requested information on the deceased.

As for what information should be returned and how the program would know what should be returned, I would use a simple text file that could be easily altered without affecting the program yet still searching for the new values, while not returning anything that would be removed. Since the values would rarely if ever need to be changed, I felt that it wasn't necessary to include the text file in the program's user interface. This still allowed for the requested information to be changed without a need to hard code any values or increase the complexity of the program.

When deciding which optical character recognition engine to use, I first looked at "OpenCV," which is primarily used for computer vision tasks, but it has a text module that includes functionalities for optical character recognition. Choosing OpenCV would also allow me to easily do any image pre-processing that I needed to without the need for another library or creating one myself. The next option that I looked at was "Tesseract," an open-source optical character recognition engine maintained by Google. It supports various languages and provides very robust text recognition capabilities; however, Tesseract isn't written in a programming language that I already know, which would require me to learn a new C++. While looking into Tesseract, I found a Python wrapper for it called Pytesseract, which is also compatible with OpenCV, meaning I could use both together. I believe that this was definitely the right choice since Pytesseract boasts higher accuracy and broader language support for fonts and non-standard layouts, while I would also be able to leverage the advanced image preprocessing tools from OpenCV.

However, all of this was for naught as my programming skills at the time and my knowledge of image preprocessing and AI models simply weren't enough to get clean results from the very complex backgrounds of a death certificate. It was at this point that I decided to pivot my approach. What I decided to go with was a PDF version of the death certificates, and I believed that the unofficial abstract versions would give me the best results as the formatting of that document was very clear and each section was easy to distinguish.

My method for parsing the data would also change as my knowledge of Pytesseract and preprocessing was still too lacking and learning the needed skill could take months. When looking through the libraries created for the purpose of parsing a PDF document, I found and decided to go with PDFminer.six, which is the current version of PDFminer for Python 2 (though my project is written in Python 3). Obtaining the desired information from the document is done by the file `pdf_to_text.py`, which utilizes the Python library PDFminer.six.

Inside my main function, the first thing that I do is define the path to the list of data I wish to retrieve. This data is stored as a string in a text file, with each string on its own line. The string is taken directly from the abstract death certificate and is required to match exactly. The next step is using PDFminer's functions to pull all the characters from the document, group them into words, and then back into sentences. After the library's functions are done, it returns to me a Python object called an "LTTextBox." This object contains locational information about where it is located inside the document and what strings are at that location.

Then, using the `datavalues.txt` file which contains the strings we pulled off the abstract death certificate, we can compare all of the strings in the PDF document and save the `LTTextBoxes` of our matches into a list. This gives us a list of all the questions we want answers to and their locations, but not any answers. However, we know that an abstract death certificate has specific formatting, where a question always has its answer in the box directly below itself. Knowing this, we can use the locational data from the list of `LTTextBoxes` that match our strings and then search for the nearest `LTTextBox` that is within the custom limits I've set. We don't want boxes that have a similar y-value, as they would be a box to its left or right; the box we want is the closest beneath it.

Now that we have what we believe is the data we want, we can do some cleaning and change it into our desired format, as all information on an abstract death certificate is capitalized. Afterward, the text box can be reasonably sure that it contains the desired information, but not 100%. However, we can also do some more easy and quick tests to double-check that the information is actually what we want. For example, a Social Security number is made up of 9 characters with each character being a whole number. Using a few small checks like this allows us to greatly increase the accuracy of the returned data.

Once all of these things are done, our data is cleaned up and formatted in the manner we want it to be. We sort it and then return it to the user interface for the user to choose what to do with it.

I wanted my program to be far less intimidating than a command line, which is why the program comes with a GUI. However, the library I chose was, in retrospect, a mistake. The first reason for this is that recently their license has changed and now requires users to pay for real use cases. The second reason is that I believe my time would have been better spent learning a more common library, especially one that has better community support and documentation.

The user interface I went with is called PySimpleGUI. My GUI has 3 windows: the main window allows a user to select a PDF file, and then using the buttons I have created and added to the window, it calls the function `run_selected_script` after validating the file type and file path of the PDF document. The called function will take the PDF file's path and give it to the main function of the `pdf_to_text.py` file, which then parses the data and returns the results to a PySimpleGUI element called a multiline. The multiline is an editable text box inside the window; the results are shown in this element in a CSV format and allow the user to easily add, edit, or correct any information they wish. These edits will be reflected in the final output CSV and XLSX files.

The second window apart from the user interface is the settings window. This window allows the user to change the save location of the output file; by default, this is the same path as the PDF document's file path. The window also shows the output file path and allows the user to launch our third and final window, which allows the changing of themes for the entire GUI. The final window is a small list of all the default themes available for PySimpleGUI. Once a new theme is selected, a user simply needs to close out of the settings windows and then press the clear button in the main window, and the application will update with the new theme applied.

All of the windows were designed with columns and separators to allow the window's size to be as fully customizable as possible from full screen to tiny; the window will adjust its component sizes to fit as best as possible. All of the buttons have errors that will pop up if their use cases are not met, preventing the application from crashing and telling the user what they need to do to use said button properly.

## Required Libraries

- PySimpleGUI
- PDFMiner
- PDFminer.six
- pandas
- openpyxl

###### July 8th, 2024
