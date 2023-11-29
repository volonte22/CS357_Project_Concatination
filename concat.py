#Author @ Jack Volonte
#Date: 11/29/2023
#Decription: This concat.py file will read in a file that contains 2 DFAs or NFAs
#chosen from the user and return a concatenated version through a GUI window.

#imports
from tkinter import simpledialog, filedialog
import random
import tkinter as tk
import numpy as np

#global variables initalization
file_names = ["Test Case 1 (NFA).txt", "Test Case 4 (NFA).txt", "Test Case 3 (NFA).txt", "Test Case 2 (DFA).txt",
              "Test Case 5 (DFA).txt"]
file = None
concat_legit = False
concatenation_type = ""
global_font_first_display = ("Helvetica", 29, 'bold')

#runs the program
def run():
    #pick, read, and set variables from file
    pick_file()
    A, B = read_file(file)
    concatenation_type = "nfa"
    info = ""

    #initial print of NFAs/DFAs
    if concatenation_type == "nfa":
        info = "Input NFA 1: \n" + format_input(A, -1, True, False)
        info += "\nInput NFA 2: \n" + format_input(B, -1, False, True)
    elif concatenation_type == "dfa":
        info = "Input DFA 1: \n" + format_input(A, -1, False, True)
        info += "\nInput DFA 2: \n" + format_input(B, -1, False, True)

    #if type = nfa, create nfa concatenation
    if concatenation_type == "nfa":
        C, old_A, old_B = create_concat_nfa(A, B)
        info += "\nConcatenated NFA:\n" + format_input(C, -1, False, False)

    #if type is dfa, create dfa concatenation
    if concatenation_type == "dfa":
        D, B, A = create_concat_dfa(A, B)
        info += "\nConcatenated DFA:\n" + format_input(D, -1, False, False)


    #highlight keywords
    keywords_to_highlight = ["Concatenated DFA:", "Concatenated NFA:"]

    #display result to the gui window
    display_on_gui(info, keywords_to_highlight, concatenation_type)


#reads in file and formats then places the information into arrays
def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        #split on : and take everything after
        parsed_data = line.split(': ', 1)[-1].strip()
        #add parsed data to array
        data.append(parsed_data)

    #numpy array from parsed data
    result_array = np.array(data)

    array_a = []
    array_b = []
    count = 0
    for i in result_array:
        if i == 'B' or count > 0:
            count = count + 1
            array_b.append(i)
        else:
            array_a.append(i)

    return array_a, array_b

#prints a definition given a DFA or NFA
def print_input(X):
    print("Name: " + X[0])
    print("Q: " + X[1])
    print("E: " + X[2])
    print("q: " + X[3])
    print("F: " + X[4])
    print("Transition Table (delta): " + X[5]+"\n")

#creates a NFA for the concatination of 2 NFAs
def create_concat_nfa(A, B):

    AB = []
    #name
    AB.append(str(A[0] + B[0]))
    #variables Q
    AB.append(getQ(A[1], B[1]))
    #language E
    AB.append(getE(A[2], B[2]))
    #initial
    AB.append(A[3])
    #final
    AB.append(B[4])
    #connections
    AB.append(epsilon_transitions(A[5], B[5], A[4], B[3]))

    return AB, B, A

#create a DFA for the concatination of 2 DFAs
def create_concat_dfa(A, B):

    AB = []
    #name
    AB.append(str(A[0] + B[0]))
    #variables Q
    AB.append(getQ(A[1], B[1]))
    #language E
    E = getE(A[2], B[2])
    AB.append(E)
    #initial
    AB.append(A[3])
    #final
    AB.append(B[4])
    #connections
    AB.append(dfa_transitions(A, B, A[5], B[5], E, A[4], B[3]))

    return AB, B, A

#create the epsilon transitions and rewrite the transition table
def epsilon_transitions(A, B, component_1, component_2):
    components_1_list = [part.strip() for part in component_1.strip("{}").split(",")]
    component_2 = component_2.strip("{}")
    result = A
    for i in components_1_list:
        output = "{" + i + ", " + component_2 + ", (e)}"
        result = result + ", " + output

    result = result + ", " + B
    return result

#create the transitions from one DFA to another and rewrite/format the transition table
def dfa_transitions(A, B, A_trans, B_trans, E, input_str, replacement_str):
    result = A_trans + ", "
    input_list = [part.strip() for part in input_str.strip("{}").split(",")]
    replacement_list = [part.strip() for part in replacement_str.strip("{}").split(",")]

    for i in input_list:
        modified_string = B_trans.replace(replacement_list[0], i)
        result += modified_string + ", "

    return result

#returns the unique states of both DFA's/NFA's
def getQ(A, B):
    components1 = A[1:-1].split(', ')
    components2 = B[1:-1].split(', ')

    all_components = components1 + components2

    modified_components = []

    #check for duplicates
    for component in all_components:
        if all_components.count(component) > 1:
            modified_component = random.randint(1, 100)
            while modified_component in modified_components:
                modified_component = random.randint(1, 100)
            modified_components.append(modified_component)
        else:
            modified_components.append(component)

    result_string = '{' + ', '.join(str(comp) for comp in modified_components) + '}'

    return result_string

#returns the E (language) found within both DFA's/NFA's
def getE(A, B):
    components1 = A[1:-1].split(', ')
    components2 = B[1:-1].split(', ')

    unique_components = list(set(components1 + components2))

    result_string = '{' + ', '.join(unique_components) + '}'

    return result_string

#highlights text of output
def highlight_text(text_widget, keywords):
    for keyword in keywords:
        start_index = text_widget.search(keyword, "1.0", tk.END)
        while start_index:
            end_index = text_widget.index(tk.END)
            text_widget.tag_add("highlight", start_index, end_index)
            text_widget.tag_configure("highlight", background="yellow")
            start_index = text_widget.search(keyword, end_index, tk.END)

#displays formatted text
def display_on_gui(info, keywords, concatenation_type):
    root = tk.Tk()
    root.title("Concatenation of two " + concatenation_type.upper() + "s")
    root.geometry("1920x1080")

    text = tk.Text(root, wrap="word", width=1280, height=720, font=("Helvetica", 26))
    text.pack()


    text.insert("1.0", info)

    #highlight keywords
    highlight_text(text, keywords)

    root.mainloop()

#formats output to be displayed in a window
def format_input(X, modified_components_A, A, B):
    result = ""
    if (modified_components_A == -1 and A == True and B == False): #A Case
        result = ""
        result += "Name: " + X[0] + "\n"
        result += "Q: " + X[1] + "\n"
        result += "E: " + X[2] + "\n"
        result += "q: " + X[3] + "\n"
        result += "F: " + X[4] + "\n"
        result += "Transition Table (delta): " + X[5] + "\n"
    elif (modified_components_A == -1 and A == False and B == True): #B Case
        result = ""
        result += "Name: " + X[0] + "\n"
        result += "Q: " + X[1] + "\n"
        result += "E: " + X[2] + "\n"
        result += "q: " + X[3] + "\n"
        result += "F: " + X[4] + "\n"
        result += "Transition Table (delta): " + X[5] + "\n"
    elif (modified_components_A == -1 and A == False and B == False):  # Final Concatenated Case
        result = ""
        result += "Name: " + X[0] + "\n"
        result += "Q: " + X[1] + "\n"
        result += "E: " + X[2] + "\n"
        result += "q: " + X[3] + "\n"
        result += "F: " + X[4] + "\n"
        result += "Transition Table (delta): " + X[5] + "\n"
    return result

#get DFA or NFA concatenation option from user
def get_concatenation_type():
    root = tk.Tk()
    root.withdraw()

    #get concatenation type
    concatenation_type = simpledialog.askstring("Concatenation Type", "Enter 'NFA' or 'DFA' for concatenation:")

    #check is valid
    while concatenation_type.lower() not in ["nfa", "dfa"]:
        concatenation_type = simpledialog.askstring("Invalid Input", "Please enter 'NFA' or 'DFA':")

    return concatenation_type.lower()

#prompt user to pick file to concatenate for
def pick_file():
    #perform action for concatenate button
    def perform_action():
        global file
        global concat_legit
        if file is not None and concat_legit is True:
            print(f"Creating concatenation of DFA or NFA for file: {file}")
            root.destroy()
        else:
            print("No file selected or wrong concatenation entry.")
            concat_the_file_wrong()


    #select file
    def select_file():
        global file
        file = filedialog.askopenfilename()
        print(f"Selected file: {file}")
        update_label()

    #update concatenation_type variable
    def update_concatenation_type():
        global concatenation_type
        concatenation_type = concat_box.get()
        # check is valid
        if concatenation_type.lower() not in ["nfa", "dfa"]:
            update_label_concat_wrong()
        else:
            global concat_legit
            concat_legit = True
            update_label_concat_right()

    # display file once its chosen
    def update_label_concat_wrong():
        concat_prompt.config(text="Wrong input - please enter 'DFA' or 'NFA:'", foreground='red', font=global_font_first_display)

    def update_label_concat_right():
        concat_prompt.config(text="Concatenation type accepted", foreground='green', font=global_font_first_display)

    def concat_the_file_wrong():
        global file
        global concat_legit
        if concat_legit is False and file is None:
            concat_the_file.config(text="Invalid concatenation type and no file selected...", foreground='red', font=global_font_first_display)
        elif concat_legit is True and file is None:
            concat_the_file.config(text="No file was selected...", foreground='red', font=global_font_first_display)
        elif concat_legit is False and file is not None:
            concat_the_file.config(text="Invalid concatenation type...", foreground='red', font=global_font_first_display)

    #display file once its chosen
    def update_label():
        select_file_prompt.config(text=f"Selected file: {file}")

    root = tk.Tk()
    root.title("Concatenation of two DFAs or NFAs")
    root.geometry("1920x1080")

    # spacing for visual improvement
    spacing_prompt = tk.Label(root, text="\n",
                              font=global_font_first_display)
    spacing_prompt.pack(pady=10)

    #button stuff for select file
    select_button = tk.Button(root, text="Select File - choose from finder (test files included in project folder)",
                              command=select_file, font=global_font_first_display, bg='lightgray')
    select_button.pack(pady=10)

    #display file initalization
    select_file_prompt = tk.Label(root, text="")
    select_file_prompt.pack(pady=10)

    # spacing for visual improvement
    spacing_prompt = tk.Label(root, text="\n\n",
                              font=global_font_first_display)
    spacing_prompt.pack(pady=10)

    #concatenation label + text box
    concat_prompt = tk.Label(root, text="Concatenation Type Entry - Enter 'NFA' or 'DFA':", font=global_font_first_display)
    concat_prompt.pack(pady=10)
    concat_box = tk.Entry(root, width=50, bg='lightgray', font=global_font_first_display)
    concat_box.pack(pady=10)

    #update concat type
    concat_type_response = tk.Button(root, text="Update Concatenation Type", command=update_concatenation_type,
                                     font=global_font_first_display, bg='lightgray')
    concat_type_response.pack(pady=10)

    # spacing for visual improvement
    spacing_prompt = tk.Label(root, text="\n\n",
                              font=global_font_first_display)
    spacing_prompt.pack(pady=10)


    #do the concatenation on the selected file
    concat_the_file = tk.Label(root, text="")
    concat_the_file.pack(pady=5)
    concat_file_button = tk.Button(root, text="Concatenate The Contents", command=perform_action,
                                   font=global_font_first_display, bg='lightgray')
    concat_file_button.pack(pady=10)

    #start loop
    root.mainloop()