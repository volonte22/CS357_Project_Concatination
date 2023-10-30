import numpy as np
import pandas as pd


def run():
    A,B = read_file("input.txt")
    print(A)
    print(B)

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        # Split the line at ':' and take everything after it
        parsed_data = line.split(': ', 1)[-1].strip()
        # Add the parsed data to the array
        data.append(parsed_data)

    # Create a numpy array from the parsed data
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









run()
