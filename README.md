# Habit tracker backend
This is a university project for the International University of Applied Sciences in the subject Object-Oriented and Functional Programming with Python. The task was to develop a backend solution for a habit tracker app.

Object-Oriented Programming (OOP) is required in habit.py, while the rest of the code follows a functional programming approach.
<br />

## Features
-Implementation of an easy CLI.

-Any frequency greater than 1 day can be used.

-Computes streaks and struggles.

-A profesional storage solution like SQLite3 was used.

-Check completion is possible at any time between of the habit creation and today. 

## Required packages
These are the strings that have to be input in your terminal to install the packages to run this code.

`pip install pytest`

if the above commands doesn't work you should try with:

`pip3 install pytest`

## How to run the program
-If you want to use it without predefined data, you just have to run main.py and interact with the CLI.

-If you want to use it with the predefined data, predefined_data.py must be executed before main.py. In both cases, main.db will be the db, and if you do both the data will be merged without any problem.

-If tests are run, you do not have to worry about your current database information because an alternate test.db is created for this purpose.


## About testing
Running test_habit.py executes all functions that users can interact with.
Only positive cases are considered, as all possible failures are handled in main.py and the analytics.py module.

## Repository
Go to [Habit tracker](https://github.com/Eric-Ristol/HabitTrackerIU)

### Author
Eric Ristol

Developed as part of the **Object-Oriented and Functional Programming with Python** course (DLBDSOOFPP01) in the International University of Applied Sciences.
