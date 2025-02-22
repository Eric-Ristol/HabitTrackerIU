import sqlite3, os
from datetime import datetime, timedelta


"""Functions for correct operation"""


def date_format(date):
    #Date _format is intended to force the user to introduce a date in the format YYYY-MM-DD, also avoids the user to introduce a date with spaces.
    #There is no need to execute date_format with empty(), because .strip() is inside this function.
    while True:
        try:
            date.strip()
            return datetime.strptime(date, "%Y-%m-%d").date()#Note: the .date() transforms the datetime object with date and time to only date
        except ValueError:
            date = input("Your date does not follow (YYYY-MM-DD). Try again:")


def connection(database_name):
    #This function is intended to change between main.db and test.db, but could be used for create any other databases
    global db_name
    db_name = database_name


def erase(database_name):
    #Erase db completely, used in test_habit_tracker.py
    os.remove(database_name)



"""Main habits table"""



def create_habits_table():
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        frequency INTEGER NOT NULL,
                        creation_date TEXT NOT NULL)''')
    connect.commit()


def insert_habit(habit_name, description, frequency, creation_date):
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    cursor.execute('''INSERT INTO habits (habit_name, description, frequency, creation_date) VALUES (?, ?, ?, ?)''', (habit_name, description, frequency, creation_date,))
    connect.commit()
    connect.close()


def rename_habit_in_habits_table(new_habit_name, new_description, habit_name):
    #It's remarkable that the creation date is not modified, neither the frequency.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()

    search = cursor.execute(f'''SELECT * FROM habits WHERE habit_name = ?''', (habit_name,))
    
    if search is None:
        return False
    else:
        cursor.execute('''UPDATE habits SET habit_name = ?, description = ? WHERE habit_name = ?''', (new_habit_name, new_description, habit_name,))
        connect.commit()
        connect.close()


def delete_habit_in_habits_table(habit_name):
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''DELETE FROM habits WHERE habit_name = ?'''
    cursor.execute(query, (habit_name,))
    connect.commit()
    connect.close()


def search_habit(habit_name)->bool:
    #This function is key to avoid errors when the user want to perform any action.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT * FROM habits WHERE habit_name = ?'''
    cursor.execute(query, (habit_name,))
    habit_info = cursor.fetchone()
    #print(f"INFO FROM DATABASE: {habit_info}")#Print is just for testing purposes.Not necessary.
    if habit_info is None:
        return 0, False #The return of the number 0 is only for compatibilty reasons, it make this function more handy.

    return habit_info[3], True #habitinfo[3]==frequency

def check_if_habits_empty()->bool:
    #This function is only used in analytics in the overall functions.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    cursor.execute('''SELECT COUNT(*) FROM habits;''')
    status = cursor.fetchone()
    status = status[0]#The return value that SQL returns is a tuple(0,) so I have to transform it into an integer.
    if status == 0:
        return True
    return False




"""Habit check off tables"""





def create_habit_checkoff_table(habit_name, today):
    """
    This function creates a table with the name of a new habit in which checks off are registered. 
    Also is filled with an initial value with the creation date and checking as 0.
    This initial value is fundamental to later create intermediate dates from the creation date to the first check off.
    """
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    #The table is created without information inside
    query = f'''
    CREATE TABLE IF NOT EXISTS habit_{habit_name} (
        check_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_date TEXT NOT NULL,
        checking INTEGER NOT NULL
    )'''
    cursor.execute(query)
    connect.commit()
    #Initial value
    query = f'''INSERT INTO habit_{habit_name} (event_date, checking) VALUES ( ?, ? )'''
    cursor.execute(query, (today, 0))
    connect.commit()
    connect.close()


def delete_habit_checkoff_table(habit_name):
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f"DROP TABLE habit_{habit_name}"
    cursor.execute(query)
    connect.commit()
    connect.close()


def rename_habit_checkoff_table(new_habit_name, habit_name):
    #For this function habit name is always passed to the database with underscores, because SQL does not accept spaces in the name of a table.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    try:
        query = f'''ALTER TABLE habit_{habit_name} RENAME TO habit_{new_habit_name}''' 
        cursor.execute(query)
    except sqlite3.OperationalError: #SQL is not case-sensitive, so it would not distinguish between habit_hello and habit_Hello and will throw this error in case of some kind of typo corecting of the habit_name, so with this try except I avoid this little problematic.
        pass
    connect.commit()
    connect.close()


def compare_creation_checkoff_dates(habit_name, check_off_date)->str:
    """
    Only used into habit class -> fuction: check_off_date
    This function is key when ensuring that check off is not in the future nor before to the creation date of the habit, ensuring a good logic in the program behaviour.
    Regardless is not relationed with this function is good to know that checks off in the future are not allowed, but create an habit in the future is allowed, that's because of the common use of for instance New Year's resolutions.
    """
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT * FROM habits WHERE habit_name = ?'''
    cursor.execute(query,(habit_name,))
    search_result = cursor.fetchone() #Here no if statemnt to check the existence of something inside the table is created because when this table is created is always filled with the creation date, so always have someting to read, also this table never is cleared, only can change it's name or be deleted if the habit is.
    creation_date = search_result[4] #search_result[4] == event_date
    connect.close()

    #Tranform string dates to date objects
    creation_date = datetime.strptime(creation_date, "%Y-%m-%d").date()
    check_off_date = datetime.strptime(check_off_date, "%Y-%m-%d").date()
    today = datetime.today().date()

    #Check if the check-off date is valid. Not before the creation date nor in the future from today.
    while check_off_date < creation_date or check_off_date > today:
        if check_off_date < creation_date:
            print(f"The check-off date ({check_off_date}) is older than the creation date ({creation_date})!")
        elif check_off_date > today:
            print(f"The check-off date ({check_off_date}) is in the future. Today is {today}!")
        
        check_off_date = date_format(input("Introduce a valid check off date (YYYY-MM-DD): "))

    return check_off_date.strftime("%Y-%m-%d") #return this value is relevant bacuse it could be the same introduced check off date or could be a new one that fits the requierements.


def create_intermediate_dates_checkoff_table(habit_name, check_off_date)->str:
    """
    This function creates as many events as days in between of the last value in the check_off_table of a habit and the check off date.
    Is used in both check off functions in the habit class
    """
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    #Get the last value in it's check off table
    query = f'''SELECT * FROM habit_{habit_name} ORDER BY check_id DESC LIMIT 1'''
    cursor.execute(query)
    last_date = cursor.fetchone()
    last_date = last_date[1]#None is not possible because the existence of the habit is being checked beforehand.

    #Creation of the intermediate dates through a loop
    start_date = datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)
    check_off_date = datetime.strptime(check_off_date, "%Y-%m-%d")

    while start_date <= check_off_date:
        start = start_date.strftime("%Y-%m-%d") #Change the date to a object date to be able to use it in the query.
        query = f'''INSERT INTO habit_{habit_name} (event_date, checking) VALUES ( ?, ? )'''
        cursor.execute(query, (start, 0)) #With that we automaticaly assign 0 to the checking value to the intermediate dates between the last check off until the selected day or today.
        start_date = start_date + timedelta(days=1)
    connect.commit()
    connect.close()
    return check_off_date #This is the new check off date that is going to be used in habits.py further.
    #maybe delete

def check_off(habit_name,check_off_date, frequency):
    """
    Update values of events into the check off table of an habit from 0 to 1
    As frequent the habit is as many checks off, i.e if an habit is every 7 days, every time is checked off, the selcted day and 6 days before are checked off (0->1)
    """
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    check_off_date = datetime.strptime(check_off_date, "%Y-%m-%d")  # Convert string to a datetime object
    start_date = check_off_date - timedelta(days=frequency-1)
    while start_date <= check_off_date:
        str_start_date = start_date.strftime("%Y-%m-%d")#I transform the date to a string to be able to use it in the query.
        query = f'''UPDATE habit_{habit_name} SET checking = 1 WHERE event_date = ?'''
        cursor.execute(query, (str_start_date,))
        start_date += timedelta(days=1)#Adds one day to the start day to complete all days in the inbetween frequency.
    connect.commit()#The commit statement could be inside the loop, but I prefer to have it outside to probably avoid longer times of execution.
    connect.close()


def show_check_off(habit_name, check_off_date, frequency):
    #Only intended for verification purpose and responsibilty of the app with the user.
    #This function can be reused to see all the checks of the table wih some adjust.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    check_off_date = datetime.strptime(check_off_date, "%Y-%m-%d")  # Convert string to a datetime object
    start_date = check_off_date - timedelta(days=frequency-1)
    while start_date <= check_off_date:
        str_start_date = start_date.strftime("%Y-%m-%d")#I transform the date to a string to be able to use it in the query.
        query = f'''SELECT * FROM habit_{habit_name} WHERE event_date = ?'''
        search = list(cursor.execute(query, (str_start_date,)))
        check = search
        print(check)
        start_date = start_date + timedelta(days=1)


def search_checkoff_table(habit_name)->bool:
    #Only used in test_habit_tracker.py
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT name FROM sqlite_master WHERE type='table' AND name=?'''
    cursor.execute(query, (f"habit_{habit_name}",))
    table_exists = cursor.fetchone()
    connect.close()
    if table_exists is None:
        return False
    return True


def search_check_off(habit_name, check_off_date)->str:
    #Only used in test_habit_tracker.py
    #This function only returns the date of a successfull check off(1), and if check off is 0 returns an empty list.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT * FROM habit_{habit_name} WHERE event_date = ? AND checking = ?'''
    search_result = list(cursor.execute(query, (check_off_date, 1,)))
    if search_result is None:
        check_off_confirmation = []
    print(search_result)
    #search_result as none is not possible because this function is executed acknowledged of previous check off.

    check_off_confirmation = [item[1] for item in search_result] #return only the second value of the tuple, in this case the date that has a 1 value.

    print(check_off_confirmation)
    return check_off_confirmation
