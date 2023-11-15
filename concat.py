from tkinter import simpledialog
import numpy as np
import pandas as pd
import random
import tkinter as tk

#runs the program ; (True, False) for NFA concat. ; (False, True) for DFA concat.
def run():
    #read input and initalize variables
    A, B = read_file("input.txt")
    old_A = A
    old_B = B

    #get type from user
    concatenation_type = get_concatenation_type()

    #initial print of NFAs/DFAs
    if concatenation_type == "nfa":
        info = "Input NFA " + A[0] +": \n" + format_input(A, -1, "", "", "", True, False, A, B, A, B)
        info += "\nInput NFA " + B[0] + ": \n" + format_input(B, -1, "", "", "", False, True, A, B, A, B)
    elif concatenation_type == "dfa":
        info = "Input DFA " + A[0] + ": \n" + format_input(A, -1, "", "", "", True, False, A, B, A, B)
        info += "\nInput DFA " + B[0] + ": \n" + format_input(B, -1, "", "", "", False, True, A, B, A, B)

    #if type = nfa, create nfa concatenation
    if concatenation_type == "nfa":
        C, modified_components_A, orig_components_A, modified_components_B, orig_components_B, old_A, old_B = create_concat_dfa(A, B)
        orig_components_A = A[1]
        orig_components_B = B[1]
        info += "\nNew NFA " + A[0] + ": \n" + format_input(A, modified_components_A, orig_components_A,
                                            modified_components_B, orig_components_B, True, False, A, B, old_A, old_B)
        info += "\nNew NFA " + B[0] + ": \n" + format_input(B, modified_components_A, orig_components_A,
                                            modified_components_B, orig_components_B, False, True, A, B, old_A, old_B)
        info += "\nConcatenated NFA:\n" + format_input(C, modified_components_A, orig_components_A, modified_components_B, orig_components_B,
                                                       False, False, A, B, old_A, old_B)

    #if type is dfa, create dfa concatenation
    if concatenation_type == "dfa":
        D, modified_components_A, orig_components_A, modified_components_B, orig_components_B, B, A = create_concat_dfa(A, B)
        orig_components_A = A[1]
        orig_components_B = B[1]
        info += "\nNew DFA " + A[0] + ": \n" + format_input(A, modified_components_A, orig_components_A,
                                            modified_components_B, orig_components_B, True, False, A, B, old_A, old_B)
        info += "\nNew DFA " + B[0] + ": \n" + format_input(B, modified_components_A, orig_components_A,
                                                       modified_components_B, orig_components_B, False, True, A, B, old_A, old_B)
        info += "\nConcatenated DFA:\n" + format_input(D, modified_components_A, orig_components_A, modified_components_B, orig_components_B, False, False, A, B, old_A, old_B)

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

    A, modified_components_A, orig_components_A = modify_array(A, True, False)
    print(A[0] + " after changes: \n")
    print_input(A)
    B, modified_components_B, orig_components_B = modify_array(B, False, True)
    print(B[0] + " after changes: \n")
    print_input(B)

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

    print("Concatinated NFA of " + A[0] + " and " + B[0] + "; " + AB[0] + ":")
    return AB, modified_components_A, orig_components_A, modified_components_B, orig_components_B, B, A

#create a DFA for the concatination of 2 DFAs
def create_concat_dfa(A, B):

    A, modified_components_A, orig_components_A = modify_array(A, True, False)
    print(A[0] + " after changes: \n")
    print_input(A)
    B, modified_components_B, orig_components_B = modify_array(B, False, True)
    print(B[0] + " after changes: \n")
    print_input(B)

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
    AB.append(dfa_transitions(A[5], B[5], E, A[4], B[3]))
    print("Concatinated DFA of " + A[0] + " and " + B[0] + "; " + AB[0] + ":")
    return AB, modified_components_A, orig_components_A, modified_components_B, orig_components_B, B, A

#create the epsilon transitions and rewrite the transition table
def epsilon_transitions(A, B, component_1, component_2):
    components_1_list = [part.strip() for part in component_1.strip("{}").split(",")]
    component_2 = component_2.strip("{}")
    result = A
    for i in components_1_list:
        output = "{" + i + ", " + component_2 + ", e}"
        result = result + ", " + output

    result = result + ", " + B
    return result

#create the transitions from one DFA to another and rewrite/format the transition table
def dfa_transitions(A, B, E, component_1, component_2):
    components_1_list = [part.strip() for part in component_1.strip("{}").split(",")]
    component_2 = component_2.strip("{}")
    E = "(" + E.strip("{}") + ")"
    result = A
    for i in components_1_list:
        output = "{" + i + ", " + component_2 + ", " + E + "}"
        result = result + ", " + output
    result = result + ", " + B
    return result

#returns the unique states of both DFA's/NFA's
def getQ(A, B):
    components1 = A[1:-1].split(', ')
    components2 = B[1:-1].split(', ')

    all_components = components1 + components2
    unique_components = list(set(all_components))

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

#modify components to not be repeating (checking if input is valid)
def modify_components(components, modified_components, A, B):
    modified_components_set = set(modified_components.values())
    new_components = []

    #replace each repeating component of both DFAs or NFAs w/random numbers
    for component in components:
        if '(' in component:
            nested_components = component[1:-1].split(',')
            modified_nested_components = modify_components(nested_components, modified_components, A, B)
            new_component = '{' + ', '.join(modified_nested_components) + '}'
            new_components.append(new_component)
        elif component.startswith('q'):
            #replace q components with random numbers
            if component in modified_components:
                new_component = modified_components[component]
            else:
                if A:
                    modified_component = random.randint(1, 100)
                if B:
                    modified_component = random.randint(101, 200)
                while modified_component in modified_components_set:
                    if A:
                        modified_component = random.randint(1, 100)
                    if B:
                        modified_component = random.randint(101, 200)
                modified_components[component] = modified_component
                modified_components_set.add(modified_component)
                new_component = modified_component
            new_components.append(new_component)
        else:
            new_components.append(component)
    return new_components

def modify_array(input_array, A, B):
    modified_components = {}
    modified_array = []

    for i, item in enumerate(input_array):
        if item.startswith('{'):
            components_list = item[1:-1].split(', ')
            print(components_list)
            modified_components_list = modify_components(components_list, modified_components, A, B)
            modified_item = '{' + ', '.join(str(comp) for comp in modified_components_list) + '}'
            modified_array.append(modified_item)
        else:
            modified_array.append(item)

    return modified_array, modified_components, modified_components_list


#highlights text
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

    text = tk.Text(root, wrap="word", width=1280, height=720, font=("Helvetica", 16))
    text.pack()

    text.insert("1.0", info)

    #highlight keywords
    highlight_text(text, keywords)

    root.mainloop()


#formats output to be displayed in a window
def format_input(X, modified_components_A, orig_components_A, modified_components_B, orig_components_B, A, B, AA, BB, old_A, old_B):
    result = ""
    print(old_A)
    if (modified_components_A == -1 and A == True and B == False): #A Case NO CHANGES YET
        result = ""
        result += "Name: " + X[0] + "\n"
        result += "Q: " + X[1] + "\n"
        result += "E: " + X[2] + "\n"
        result += "q: " + X[3] + "\n"
        result += "F: " + X[4] + "\n"
        result += "Transition Table (delta): " + X[5] + "\n"
    elif (modified_components_A == -1 and A == False and B == True): #B Case NO CHANGES YET
        result = ""
        result += "Name: " + X[0] + "\n"
        result += "Q: " + X[1] + "\n"
        result += "E: " + X[2] + "\n"
        result += "q: " + X[3] + "\n"
        result += "F: " + X[4] + "\n"
        result += "Transition Table (delta): " + X[5] + "\n"
    elif (modified_components_A != -1 and A == False and B == True):  # A Case W/CHANGES
        result = ""
        result += "Name: " + X[0] + "\n"
        result += "Original Q: " + X[1] + " ;  New Q: " + str(old_A[1]) + "\n"
        result += "E: " + X[2] + "\n"
        result += "Original q: " + X[3] + " ;  New q: " + str(old_A[3]) + "\n"
        result += "Original F: " + X[4] + " ;  New F: " + str(old_A[4]) + "\n"
        result += "Original Transition Table (delta): " + X[5] + " ; New Transition Table (delta): " + str(old_A[5]) + "\n"
    elif (modified_components_A != -1 and A == True and B == False):  # A Case W/CHANGES
        result = ""
        result += "Name: " + X[0] + "\n"
        if (str(old_A[1]) != X[1]):
            result += "Original Q: " + X[1] + " ;  New Q: " + str(old_B[1]) + "\n"
        else:
            result += "Q: " + X[1] + "\n"
        result += "E: " + X[2] + "\n"
        result += "Original q: " + X[3] + " ;  New q: " + str(old_B[3]) + "\n"
        result += "Original F: " + X[4] + " ;  New F: " + str(old_B[4]) + "\n"
        result += "Original Transition Table (delta): " + X[5] + " ; New Transition Table (delta): " + str(old_B[5]) + "\n"
    elif (modified_components_A != -1 and A == False and B == False):  # A Case W/CHANGES
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
