import sqlite3
from functools import reduce
import db
from db import connection

    
def connection(database_name):
    global db_name
    db_name = database_name


"""List of all currently tracked habits"""
def list_habits():
    """
    Returns a list of all current habits from the  habits table.
    The first entry of the list is an header of what is every value of the rest of the list.
    This list is more intended to be where to get all relevant information for the user e.g forgot active habits or the periodicity of some habit.
    """
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT habit_name, description, periodicity, creation_date FROM habits'''
    cursor.execute(query)
    habits_names_list = cursor.fetchall()
    habits_names_list = [('habit_name, description, periodicity, creation_date')] + habits_names_list
    return habits_names_list



"""List of all habits with the same periodicity"""
def same_period(periodicity):
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT habit_name FROM habits WHERE periodicity = ?'''
    cursor.execute(query,(periodicity,))
    periodicity_names_list = cursor.fetchall()
    if not periodicity_names_list:
        return False
    return periodicity_names_list


"""This functions are used for the streaks functions and struggle functions"""

#For given name funcitons
#Just return a binary list that are the checksoff of a habit.
#This function also checks the existence of the habit to prevent further errors.
def get_checks(habit_name:str)-> int:
    #Look for the existence of the habit.
    periodicity, success = db.search_habit(habit_name) #In this case periodicity is not used, but I have to creaste the variable because the function return 2 values, one is periodicity and the other is a boolean.
    if not success:
        print("This habit does not exist!")
        return False #If the habit is not found, the rest of the function is not executed.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT checking FROM habit_{habit_name}'''
    cursor.execute(query)
    result = cursor.fetchall()  #This is a list of tuples
    if result is None:
        return False
    checks_list = [item[0] for item in result]  #Get only the first value of each tuple
    return True, checks_list

#For overall functions
def only_name_list():

    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT habit_name FROM habits'''
    cursor.execute(query)
    habits_names_list = cursor.fetchall()
    if habits_names_list is None:
        print("There are no habits created into the database, please, create them first.")
        return False
    return habits_names_list



"""- and return the longest run streak for a given habit."""



#With this function we get the highest streak. Also is posible to obtain all the streak.
def streak(habit_name)-> int:
    checks_list = get_checks(habit_name)
    if not checks_list: #This means if check list is empty.
        return
    


    length = len(checks_list)
    count = []
    index = 0
    streak = []
    
    while index < length:
        read = checks_list[index]
        if read == 1:
            count.append(1)
        elif read == 0:
            if count:
                streak.append(sum(count))
                count = []
        index += 1
    #This condition appends the count amount in case of the list does not end in a 0 or 0s.
    if index == length:
        if count:
            streak.append(sum(count))
            count = []
    if not streak: #This checks if the list is empt, if is empty returns false, which is the problematic outocme.
        streak = [0]
    highest_streak = max(streak)
    return highest_streak


"""- return the longest run streak of all defined habits,"""



def overall_streak()->int:
    habits_names_list = only_name_list()
    habits_names_list = [item[0] for item in habits_names_list]#COnverts the list of tuples ino a list of strings  
    num_habits = len(habits_names_list)
    index = 0
    overall_streak = [0]
    while index < num_habits:
        habit_name = habits_names_list[index]
        overall_streak.append(streak(habit_name))# The [0] is because habit_name from habits_names_list returns a list with habit_name,description,periodicity and creation_date, but I only need the habit_name.
        index += 1
    longest_streak = max(overall_streak)
    return longest_streak
        





"""-Struggling habits, i.e the habits that have been checked off less."""



def struggle(habit_name)->int:#Is just the straks function but counting 0s instead of 1s
    if get_checks(habit_name) == False:
        return
    checks_list = get_checks(habit_name)

    length = len(checks_list)
    count = []
    index = 0
    struggle= []

    while index < length:
        read = checks_list[index]
        if read == 0:
            count.append(1)
        elif read == 1:
            if count: #Checks that count is not empty, if empty == False if filled == True
                struggle.append(sum(count))
                count = []
        index += 1
    #This condition appends the count amount in case of the list does not end in a 0 or 0s.
    if index == length:
        if count:
            struggle.append(sum(count))
            count = []
    if not struggle: #This checks if the list is empt, if is empty returns false, which is the problematic outocme.
        struggle = [0]
    highest_struggle = max(struggle)
    return highest_struggle




"""- return the longest struggle of all defined habits,"""


def overall_struggle()->int:
    habits_names_list = only_name_list()
    habits_names_list = [item[0] for item in habits_names_list]#COnverts the list of tuples ino a list of strings  
    num_habits = len(habits_names_list)
    index = 0
    overall_struggle= [0]
    while index < num_habits:
        habit_name = habits_names_list[index]
        overall_struggle.append(struggle(habit_name))# The [0] is because habit_name from habits_names_list returns a list with habit_name,description,periodicity and creation_date, but I only need the habit_name.
        index += 1
    longest_struggle = max(overall_struggle)
    return longest_struggle








def empty(value):
    #This function ensures that the user does not enter an empty value, eliminates innecesary spaces, and avoids the user to introduce special characters.
    #In case of just inncesary spaces, the function eliminates them, and don't ask the suer to write the sentence again
    while True:
        check = value.strip()
        if all(char.isalnum() or char.isspace() for char in check) and check:
            return check
        print("This value is empty, or has special characters. Please enter valid value.")
        value = input("Try again: ")


def module():
    while True:

        print("\nAnalytics module....")
        print("\n1. List of all currently tracked habits")
        print("2. List of all habits with the same periodicity")
        print("\n3. Longest run streak of all defined habits")
        print("4. Longest run streak for a given habit")
        print("\n5. Longest struggle of all defined habits")
        print("6. Longest struggle for a given habit")

        print("\n7. Exit to the habit tracker CLI")

        choice = empty(input("\nEnter your choice (1-7): "))
        
        
        if choice == "1":
            habits_names_list = list_habits()
            habits_names_list[0] = habits_names_list[0].replace('_', ' ')  #Modify the header
            # Modify each tuple inside the data
            habits_names_list[1:] = [tuple(val.replace('_', ' ') if isinstance(val, str) else val for val in row) for row in habits_names_list[1:]]#This line was extracted directly from a chatGPT answer because of it's complexity and irrelevance in the overall of the project.
            print(habits_names_list)

        elif choice == "2":
            while True: #Check if the input value is an integer or not, and if not asks again until an intger is introduced.
                try:
                    periodicity = int(input("Enter the periodicity (in days): "))
                    if periodicity < 1:
                        print("The periodicity has to be greater than 0!")
                        return int(empty(str(periodicity)))#I have to transform the value into a string to manage it with the empty function because .strip is not possible with integers.Finally I transform it again into an INTEGER because the database only manages INTEGER in the periodicicty value.
                    break
                except ValueError:
                    print("This value has to be an integer!")
            periodicity_names_list = same_period(periodicity)
            if periodicity_names_list == False:
                print("There are no habit with this periodicity")
                return
            periodicity_names_list = [(val.replace('_', ' ') if isinstance(val, str) else val) for val in periodicity_names_list[0]]
            print(periodicity_names_list)


        elif choice == "3":
            longest_streak = overall_streak()
            print(f"Longest streak: {longest_streak} days")
        elif choice == "4":
            habit_name = empty(input("For which habit do you want to get the longest streak?: "))
            

            habit_name = habit_name.replace(" ", "_")
            highest_streak = streak(habit_name)
            print( f"{highest_streak} days")

        
        elif choice == "5":
            longest_struggle = overall_struggle()
            print(f"Longest struggle: {longest_struggle} days")
        elif choice == "6":
            habit_name = empty(input("For which habit do you want to get the longest struggle?: "))
            habit_name = habit_name.replace(" ", "_")
            highest_struggle = struggle(habit_name)
            print( f"{highest_struggle} days")


        elif choice == "7":
            print("Exiting the Analytics module. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

