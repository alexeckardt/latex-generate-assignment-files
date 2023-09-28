import os
import subprocess
import pyperclip;
import datetime;
import generate_aux as aux;

bufferLength = aux.get_config('buffer_length')
BigBufferString = ("%% " + "-"*bufferLength + " %%\n")*3
BufferString = "%% " + "-"*bufferLength + " %%\n"
SectionBuffer = BufferString + "%\n"*2 + "%\t\t\t\t{}\n" + "%\n"*2 + BufferString

#Get
assignment_details = aux.assignments

#Dir
generateDirectory = not aux.get_config("save_to_clipboard_instead_of_directory")
baseDir = os.path.abspath(aux.get_config("generation_directory"))

#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------

def create_body(assignmentstruct):

    # 
    assignmenttype = assignmentstruct['name']
    if assignmenttype == "Assignment (Questions)": #assignment
        return create_body_assignment();

    # 
    if assignmenttype == "Assignment (Parts)": #parts assignment
        return create_body_assignment_2();

    #
    # Empty Body -- No setup parts
    return "\n\n\n"


def create_body_assignment():
        
    bodystr = ""
    qnum = int(aux.input_string("Assignment: Number of Questions: "))

    #Generate the Lines
    for i in range(qnum):
        bodystr += "\section{Question XXXX}\n\subsection{a)}\n\n".replace("XXXX", str(i+1)) + BufferString + "\n"

    return bodystr;

#----------------------------------------------------------------------------------

def create_body_assignment_2():
    
    #Str
    bodystr = ""
    qnum = int(aux.input_string("Assignment Parts: Number of Parts: "))
    useRomans = aux.get_config("parts_assignment_uses_roman_numerals")

    #Generate Body
    for i in range(qnum):
        
        part = i+1

        if useRomans:
            part = aux.int_to_roman(i+1);


        bodystr += "{BIGBUFFER}\n\n"
        bodystr += "\section{Part " + part + "}\n" 
        bodystr += "subsection{a)}\n\n"
        bodystr += BufferString + "\n"

    return bodystr;


#---------------------------------------------------------------------------------

def replace_in_list_to_str(linelist, phrasesDict):

    returnString = ""

    for i in range(len(linelist)):
        line = linelist[i];

        #Replace all Froms with Tos
        for phrase in phrasesDict.keys():
            line = line.replace("{" + phrase + "}", phrasesDict[phrase])

        #Append the new line
        returnString += line

    return returnString;



#---------------------------------------------------------------------------------

def open_folder_vscode(local):

    if not aux.get_config('open_saved_directory_in_vscode'):
        return

    # Transform
    directory_path = os.path.abspath(local)
    directory_path = directory_path.replace('\\', "/")

    print(f'Attempting to Open {directory_path} in VSCode...')

    try:
        subprocess.run(["code", "", directory_path], check=True)
    except Exception as e:
        print(f"Error: {e}")
        print("This may be due to you not having code as an evironment variable. Set a new variable 'code' with the value being the path the the executeable of VS Code.")
    else:
        print(f"Visual Studio Code opened with directory '{directory_path}'")

#---------------------------------------------------------------------------------

def main():

    #Open File For Reading
    lines = []
    with open("template.txt", "r") as f:
        lines = f.readlines();

    #Prompt
    phrases = {};
    code = aux.input_string_upper("Enter Course Code: ");

    phrases["COURSECODE"] = code

    # Choose the Assignment
    assignment_selected = aux.choose_assignment(assignment_details);
    phrases["ASSIGNMENTTYPE"] = assignment_selected["display_name"]
    phrases["ASSIGNMENTNUM"] = input("Enter Assignment Num: ");


    # Make new Directoty
    subdir = assignment_selected["directory"] + phrases["ASSIGNMENTNUM"]
    newDir = f"{baseDir}/{code.lower()}/{subdir}"
    newDir = newDir.replace('\\', '/')

    #
    # Make
    if (not os.path.exists(newDir)):
        os.makedirs(newDir)
    else:
        print('File Exists.')
        open_folder_vscode(newDir);
        return

    #
    #
    print('\nNew Assignment Detected .. Enter Build Information...')

    phrases["DUEDATE"] = aux.input_duedate();
    phrases["AUTHORS"] = aux.input_authors();
    phrases["BODY"] = create_body(assignment_selected);

    phrases["BIGBUFFER"] = BigBufferString;
    phrases["BUFFER"] = BufferString;

    #Replace
    copyString = replace_in_list_to_str(lines, phrases);

    #
    # Generate in directory?
    if not generateDirectory:
        pyperclip.copy(copyString)
        print("\nCopied to Clipboard!!\n\n")
        return 0;

    # Place the latex file in 
    with open(newDir + "/main.tex", 'w') as f:
        f.writelines(copyString);

    #
    # Open the folder
    open_folder_vscode(newDir);
    return 0


if __name__ == "__main__":
    main()