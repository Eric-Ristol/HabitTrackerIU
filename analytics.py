import sqlite3
import db


    
def connection(database_name): 
    global db_name
    db_name = database_name


"""List of all currently tracked habits:"""

def list_habits()->list:
    """
    Returns a list of all current habits from the  habits table.
    The first entry of the list is an header of what is every value of the rest of the list.
    This list is more intended to be where to get all relevant information for the user e.g forgot active habits or the frequency of some habit.
    """
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT habit_name, description, frequency, creation_date FROM habits'''
    cursor.execute(query)
    habits_names_list = cursor.fetchall()
    habits_names_list = [('habit name, description, frequency, creation date')] + habits_names_list
    return habits_names_list



"""List of all habits with the same frequency"""

def same_frequency_list(frequency)->list:
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT habit_name FROM habits WHERE frequency = ?'''
    cursor.execute(query,(frequency,))
    frequency_names_list = cursor.fetchall()
    if not frequency_names_list:#When a list is empty, it returns False by default
        return False
    return frequency_names_list


"""These functions are used for the streaks functions and struggle functions"""


def get_checks(habit_name)->list:
    #This function returns a binary list of 0s and 1s that are the checks of a habit used in streak and struggle functions.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT checking FROM habit_{habit_name}'''
    cursor.execute(query)
    result = cursor.fetchall()  #This is a list of tuples
    checks_list = [item[0] for item in result]  #Get only the first value of each tuple
    return checks_list


def only_names_list()->list:
    #Returns a list of all habit names, only names, that's the main diference with list_habits. This function is used in overall streak and struggle.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT habit_name FROM habits'''
    cursor.execute(query)
    habits_names_list = cursor.fetchall()
    if habits_names_list is None:
        print("There are no habits created in the database, please, create them first.")
        return False
    return habits_names_list



"""Longest run streak for a given habit."""


def streak(habit_name)->int:
    """With this function we get the highest streak. Also is posible to obtain all the streaks with just returning streak ."""
    checks_list = get_checks(habit_name)
    length = len(checks_list)
    count = []
    index = 0
    streak = []
    
    while index < length:
        read = checks_list[index]
        if read == 1:
            count.append(1)
        elif read == 0:#The appropiate syntax is else because only 0 and 1 are possible, but I wrote it in this way to make it more readable, and with the other else statement I ensure an easy debugging in case the paramenter is changed by accident.
            if count:#Checks that count is not empty, if empty == False if filled == True
                streak.append(sum(count))
                count = []
        else:
            raise ValueError("The check off table has to be filled with 0s and 1s only.")
        index += 1
    
    if index == length:#This condition appends the count amount in case the list does not end in a 0 or 0s.
        if count:#Checks that count is not empty, if empty == False if filled == True
            streak.append(sum(count))
            count = []
    if not streak: #This checks if the list is empty, and if it is assigns 0 to the list. This could happen if the list is only 0s.
        streak = [0]
    highest_streak = max(streak)
    return highest_streak



"""Longest run streak of all defined habits,"""


def overall_streak()->int:
    habits_names_list = only_names_list()
    habits_names_list = [item[0] for item in habits_names_list]#Transforms the list of tuples into a list of strings  
    num_habits = len(habits_names_list)
    index = 0
    overall_streak = [0]
    while index < num_habits:
        habit_name = habits_names_list[index] # [index] is because habit_name from habits_names_list returns a list with all habits names, but I need to read one by one for every loop cycle.
        overall_streak.append(streak(habit_name))
        index += 1
    longest_streak = max(overall_streak)
    
    return longest_streak
        





"""-Struggling habits, i.e the habits that have been checked off less."""



def struggle(habit_name)->int:
    """With this function we get the highest struggle. Also is posible to obtain all the struggles with just returning struggle ."""
    checks_list = get_checks(habit_name)
    length = len(checks_list)
    count = []
    index = 0
    struggle= []

    while index < length:
        read = checks_list[index]
        if read == 0:
            count.append(1)
        elif read == 1:#The appropiate syntax is else because only 0 and 1 are possible, but I wrote it in this way to make it more readable, and with the other else statement I ensure an easy debugging in case the paramenter is changed by accident.
            if count: #Checks that count is not empty, if empty == False if filled == True
                struggle.append(sum(count))
                count = []
        else:
            raise ValueError("The check off table has to be filled with 0s and 1s only.")
        index += 1

    if index == length:#This condition appends the count amount in case the list does not end in a 0 or 0s.
        if count:#Checks that count is not empty, if empty == False if filled == True
            struggle.append(sum(count))
            count = []
    if not struggle: #This checks if the list is empty, and if it is assigns 0 to the list. This could happen if the list is only 1s.
        struggle = [0]
    highest_struggle = max(struggle)
    return highest_struggle




"""Longest struggle of all defined habits,"""


def overall_struggle()->int:
    habits_names_list = only_names_list()
    habits_names_list = [item[0] for item in habits_names_list]#Transforms the list of tuples into a list of strings.
    num_habits = len(habits_names_list)
    index = 0
    overall_struggle= [0]
    while index < num_habits:
        habit_name = habits_names_list[index]# [index] is because habit_name from habits_names_list returns a list with all habits names, but I need to read one by one for every loop cycle.
        overall_struggle.append(struggle(habit_name))
        index += 1
    longest_struggle = max(overall_struggle)

    return longest_struggle






"""Build function to ensure correct inputs"""

def empty(value):
    #This function ensures that the user does not enter an empty value, eliminates innecesary spaces, and avoids the user to introduce special characters.
    #In case of just unnecessary spaces, the function eliminates them, and don't ask the user to write the sentence again.
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
        print("2. List of all habits with the same frequency")
        print("\n3. Longest run streak of all defined habits")
        print("4. Longest run streak for a given habit")
        print("\n5. Longest struggle of all defined habits")
        print("6. Longest struggle for a given habit")

        print("\n7. Exit to the habit tracker CLI")

        choice = empty(input("\nEnter your choice (1-7): "))
        

        if choice == "1":
            if db.check_if_habits_empty():
                print("There are no active habits created in the database, please, create them first.")
                continue
            habits_names_list = list_habits()
            print()
            print(habits_names_list[0])
            print()
            for index in range(1, len(habits_names_list)):#This for loop is intended to remove the underscores from the habit names and descriptions, and print the list of habits with an empty line between every tuple of the original habits_names_list(i.e the habit with it's characteristics).
                habits_names_list[index] = tuple( val.replace("_"," ") if isinstance(val, str) else val for val in habits_names_list[index])
                print(habits_names_list[index])
                print()
        elif choice == "2":
            while True: #Check if the input value is an integer or not, and if not asks again until an intger is introduced.
                try:
                    frequency = int(input("Enter the frequency (in days): "))
                    if frequency < 1:
                        print("The frequency has to be greater than 0!")
                        return int(empty(str(frequency)))#I have to transform the value into a string to manage it with the empty function because .strip is not possible with integers.Finally I transform it again into an INTEGER because the database only manages INTEGER in the frequency value.
                    break
                except ValueError:
                    print("This value has to be an integer!")
            frequency_names_list = same_frequency_list(frequency)
            if not frequency_names_list:
                print("There are no habit with this frequency")
                continue
            print()
            for index in range(0, len(frequency_names_list)):
                frequency_names_list[index] = tuple( val.replace("_"," ") if isinstance(val, str) else val for val in frequency_names_list[index])
                print(frequency_names_list[index])
                print()


        elif choice == "3":
            if db.check_if_habits_empty():
                print("There are no active habits created in the database, please, create them first.")
                continue
            longest_streak = overall_streak()
            print(f"Longest streak: {longest_streak} days")
        elif choice == "4":
            habit_name = empty(input("For which habit do you want to get the longest streak?: "))
            habit_name = habit_name.replace(" ", "_")
            frequency, success = db.search_habit(habit_name) #In this case frequency is not used, but I have to creaste the variable because the function return 2 values, one is frequency and the other is a boolean.
            if not success:
                print("This habit does not exist!")
                continue #If the habit is not found, the rest of the function is not executed.
            highest_streak = streak(habit_name)
            print( f"{highest_streak} days")

        
        elif choice == "5":
            if db.check_if_habits_empty():
                print("There are no active habits created in the database, please, create them first.")
                continue
            longest_struggle = overall_struggle()
            print(f"Longest struggle: {longest_struggle} days")
        elif choice == "6":
            habit_name = empty(input("For which habit do you want to get the longest struggle?: "))
            habit_name = habit_name.replace(" ", "_")
            frequency, success = db.search_habit(habit_name) #In this case frequency is not used, but I have to creaste the variable because the function return 2 values, one is frequency and the other is a boolean.
            if not success:
                print("This habit does not exist!")
                continue #If the habit is not found, the rest of the function is not executed.
            highest_struggle = struggle(habit_name)
            print( f"{highest_struggle} days")


        elif choice == "7":
            print("Exiting the Analytics module. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

