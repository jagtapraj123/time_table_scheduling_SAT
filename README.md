# Time Table Scheduling Program

This program is a python program that is based on Time Table Scheduling to SAT reduction approach.

We first encode the problem in Propositional Logic and use 'z3 SAT Solver' to find if there can be a time table.

If there can be a time table the program will make an Excel Sheet and print it.
 

## Requirements
This program requires the following libraries
1. [z3](https://github.com/Z3Prover/z3/releases) SAT Solver for Python
2. XlsxWriter for python 
```bash
pip install XlsxWriter
```
3. copy
4. json

## Usage
1. Make sure you have all the required libraries.
2. Make sure you have the input JSON file in the correct format. 
3. Run the main.py file to check if there can exist a time table or not.
```bash
python main.py
```
4. If there can exist a time table the program will create an Excel Worksheet with name TimeTable.xlsx and print the time table in that file.


## JSON Format for Input
Should have
1. "Room Types" specifying all the sizes. e.g. ["small", "big"]
2. "Classrooms" specifying all classes with sizes. e.g. [ ["T1", "small"],
        ["LH1", "big"] ]
3. "Courses" list

"Courses" must specify:
1. Course Name. e.g. "cs201"
2. List of classroom sizes possible for that course. e.g. ["small", "big"]
3. List of lectures time required for that course. e.g. [1.5, 1.5]
4. List of Professors teaching that course. e.g. ["Amal", "Clint"]
5. List of batches attending that course. e.g. ["cs btech 18"]

#### Note:
1.  If some course requires classroom size of small, big size classroom can also be used for that course if small size classroom is unavailable.
Hence put ["small", "big"] instead of "small".
2. If multiple batches are going to attend a course, put them in a list.
e.g. ["cs btech 16", "ee btech 16", "me btech 16"]

## Purpose
We created this Time Table Scheduling Program as part of a programming assignment of **CS 228**: Logic in Computer Science taught at **IIT Goa**.

## Team
1. Raj S. Jagtap
2. Neeraj Khatri
3. Ujjawal Tiwari 

## Contributing
Any suggestions in improving are appreciated.

## License
[MIT](https://choosealicense.com/licenses/mit/)
