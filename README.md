Author @ Jack Volonte 

Date: 11/29/2023

Title: CS357_Project_Concatination

Description: Concatination of two NFAs or DFAs using Python

Run from main.py
  - select a file and enter the concatenation type - "dfa" or "nfa"
  - click "concatenate the contents"

Test files included from project proposal document:
  - Test Case 1 (NFA).txt
  - Test Case 2 (DFA).txt
  - Test Case 3 (NFA).txt
  - Test Case 4 (NFA).txt
  - Test Case 5 (DFA).txt


If you want to create a file to concatenate a DFA or NFA, then you must follow the following format (any change will result in a failed file read) - IGNORE ALL BULLET POINT SYMBOLS, SIMPLY USED FOR SPACING ON THIS DOCUMENT:
  - Name 1
  - Q: {contents inside of the curly brace}
  - E: {contents inside of the curly brace}
  - q: {contents inside of the curly brace}
  - F: {contents inside of the curly brace}
  - O: {contents inside of the curly brace}
  - Name 2
  - Q: {contents inside of the curly brace}
  - E: {contents inside of the curly brace}
  - q: {contents inside of the curly brace}
  - F: {contents inside of the curly brace}
  - O: {contents inside of the curly brace}


Example:
  - A
  - Q: {q0, q1}
  - E: {a, b}
  - q: {q0}
  - F: {q1}
  - O: {q0, q1, (b)}, {q1, q1, (a, b)}}
  - B
  - Q: {q2, q3}
  - E: {a, b}
  - q: {q2}
  - F: {q3}
  - O: {q2, q3, (a)}, {q3, q3, (a,b)}

If you have any questions or problems with the code, please contact me by email @ volonte22@up.edu
