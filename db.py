import sqlite3, os
from datetime import datetime, timedelta


"""Build function to ensure correct inputs"""


def date_format(date):
    #Date _format is intended to force the user to introduce a date in the format YYYY-MM-DD, also avoids the user to introduce a date with spaces.
    #There is no need to execute date_format with empty().
    while True:
        try:
            date.strip()
            return datetime.strptime(date, "%Y-%m-%d").date()#Note: the .date() transforms the datetime object with date and time to only date
        except ValueError:
            date = input("Your date does not follow (YYYY-MM-DD). Try again:")


#This function is intended to use this script for main.db and test.db
def connection(database_name):
    global db_name
    db_name = database_name

#Erase db
def erase(database_name):
    os.remove(database_name)


"""Main habits table"""




def create_habits_table():
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        periodicity INTEGER NOT NULL,
                        creation_date TEXT NOT NULL)''')
    connect.commit()


def insert_habit(habit_name, description, periodicity, creation_date):
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    cursor.execute('''INSERT INTO habits (habit_name, description, periodicity, creation_date) VALUES (?, ?, ?, ?)''', (habit_name, description, periodicity, creation_date,))
    connect.commit()
    connect.close()


def rename_habit_in_habits_table(new_habit_name, new_description, habit_name):
    #It's remarkable that the creation date is not modified, neither the periodicity.
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


#This function is key to avoid errors when the user want to perform any action that is not create an habit, this fucntion return the periodicity of the habit and a boolean that indicates if the habit exists or not, the habit_name table with the checks off, is not checked because the program was structured to ensure that this tables are always created, deleted and modified with the habit into the habits table, so it;s no need to search it.
def search_habit(habit_name):
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT * FROM habits WHERE habit_name = ?'''
    cursor.execute(query, (habit_name,))
    habit_info = cursor.fetchone()
    print(f"INFO FROM DATABASE: {habit_info}")#Print is just for testing purposes.Not necessary.
    if habit_info is None:
        return habit_name, False #Return habut_name is not usefull for anything, is just ot make the funciton more compatible into the habit class.
    else:
        return habit_info[3], True #habitinfo[3]==periodicity
    #I can have different returns because of th afterwards use of this functions, because I ensure certain conditions before execute it.



"""Habit check off table"""





def create_habit_checkoff_table(habit_name, today): 
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

    #First row is created with the creation date and the default checking value is 0.
    #This empty value that is filled with the creation date is important to later autocreate the dates between the creation date and the first check off.
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
        connect = sqlite3.connect(f"{db_name}")
        cursor = connect.cursor()
        query = f'''ALTER TABLE habit_{habit_name} RENAME TO habit_{new_habit_name}'''
        cursor.execute(query)
        connect.commit()
        connect.close()


#This fucntion is intended to ensure check-off date is after the creation date and not in the future.
def compare_creation_checkoff_dates(habit_name, check_off_date):
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT * FROM habits WHERE habit_name = ?'''
    cursor.execute(query,(habit_name,))
    search_result = cursor.fetchone() #Here no if statemnt to check the existence of something inside the table is created because when this table is created is always filled with the creation date, so always have someting to read, also thsi table never has deletions.
    creation_date = search_result[4] #In the table this caolumn is called event_date
    connect.close()

    #Tranform string dates to date objects
    creation_date = datetime.strptime(creation_date, "%Y-%m-%d").date()
    check_off_date = datetime.strptime(check_off_date, "%Y-%m-%d").date()
    today = datetime.today().date()

    #Check if the check-off date is valid. Not before the creation date nor in the future of today.
    while check_off_date < creation_date or check_off_date > today:
        if check_off_date < creation_date:
            print(f"The check-off date ({check_off_date}) is older than the creation date ({creation_date})!")
        elif check_off_date > today:
            print(f"The check-off date ({check_off_date}) is in the future. Today is {today}!")
        
        check_off_date = date_format(input("Introduce a valid check off date (YYYY-MM-DD): "))

    return check_off_date.strftime("%Y-%m-%d")


#Created to be executed into create_intermediate_dates_checkoff_table().
def get_last_value_checkoff_table(habit_name, check_off_date):
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    query = f'''SELECT * FROM habit_{habit_name} ORDER BY check_id DESC LIMIT 1'''
    cursor.execute(query)
    last_date = cursor.fetchone()
    last_date = last_date[1]#None is not possible because the existence of the habit is being checked beforehand in the funciton Habit.check_off() and the check off table is always creadted or deleted at the same time of the habit inot hte habits table.
    connect.commit()
    connect.close()
    return last_date



def create_intermediate_dates_checkoff_table(habit_name, check_off_date):
    last_date = get_last_value_checkoff_table(habit_name,check_off_date)
    
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    start_date = datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)
    check_off_date = datetime.strptime(check_off_date, "%Y-%m-%d")
    while start_date <= check_off_date:
        start = start_date.strftime("%Y-%m-%d") #Change the date to a object date to be able to use it in the query.
        query = f'''INSERT INTO habit_{habit_name} (event_date, checking) VALUES ( ?, ? )'''
        cursor.execute(query, (start, 0)) #With that we automaticaly assign 0 to the checking value to the intermediate dates btewwen the last check off until the selected day or today, depending on the user choice.
        start_date = start_date + timedelta(days=1)
    connect.commit()
    connect.close()
    return check_off_date #This is the new check off date that is going to be used in habits.py further.


def check_off(habit_name,check_off_date, periodicity):
    #First I build something that works with daily, and after with custom periodicity.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    check_off_date = datetime.strptime(check_off_date, "%Y-%m-%d")  # Convert string to a datetime object
    start_date = check_off_date - timedelta(days=periodicity-1)
    while start_date <= check_off_date:
        str_start_date = start_date.strftime("%Y-%m-%d")#I transform the date to a string to be able to use it in the query.
        query = f'''UPDATE habit_{habit_name} SET checking = 1 WHERE event_date = ?'''
        cursor.execute(query, (str_start_date,))
        start_date += timedelta(days=1)#Adds one day to the start day to complete all days in the inbetween period.
    connect.commit()#The commit statement could be inside the loop, but I prefer to have it outside to probably avoid longer times of execution.
    connect.close()


def show_check_off(habit_name, check_off_date, periodicity):
    #This function can be reused to see all the checks of the table wih some adjust.
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()
    check_off_date = datetime.strptime(check_off_date, "%Y-%m-%d")  # Convert string to a datetime object
    start_date = check_off_date - timedelta(days=periodicity-1)
    while start_date <= check_off_date:
        str_start_date = start_date.strftime("%Y-%m-%d")#I transform the date to a string to be able to use it in the query.
        query = f'''SELECT * FROM habit_{habit_name} WHERE event_date = ?'''
        search = list(cursor.execute(query, (str_start_date,)))
        check = search
        print(check)
        start_date = start_date + timedelta(days=1)


def search_checkoff_table(habit_name):
    connect = sqlite3.connect(f"{db_name}")
    cursor = connect.cursor()

    query = f'''SELECT name FROM sqlite_master WHERE type='table' AND name=?'''
    
    cursor.execute(query, (f"habit_{habit_name}",))
    table_exists = cursor.fetchone()
    connect.close()
    if table_exists is None:
        return False
    else:
        return True


def search_check_off(habit_name, check_off_date):
    #This fucntion only return the date of a successfull chech off(1), and if chech off is 0 returns an empty list.
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
