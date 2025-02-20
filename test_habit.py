import habit
import db
import analytics
from datetime import datetime




#Initalizing functions
h = habit.Habit("0","0",1,"2000-01-01") #class initialization
db.connection("test.db")
analytics.connection("test.db")
db.create_habits_table()





"""When testing, strings has to have underscores instead of spaces, cannot have special characters, periodicity has to be only an integer without any kind of space or extra character and creation_date has to strcitly follow (YYYY-MM-DD) to work properly, but regardless this limitations this are fixed into main.py and analytics, transforming the inputs and print statements to return values like looking to original one when inputed."""


"""Testing of habit class"""


def test_create():
    #Confirm the existence of the habit into the habits table
    h.create(habit_name="Test_name", description="Test_description", periodicity=1,creation_date="2025-01-01" )
    assert db.search_habit(habit_name="Test_name") == (1, True)
    #confirms the creation of it's own check off table
    assert db.search_checkoff_table(habit_name="Test_name") == (True)

def test_create_not_valid_input():
    #Confirm the existence of the habit into the habits table
    h.create(habit_name="Test name", description="Test description", periodicity=1,creation_date="2025-01-01" )
    

def test_modify():
    h.modify(habit_name="Test_name", new_habit_name="Modifyed_test_name", new_description="Modifyed test description")
    assert db.search_habit(habit_name="Test_name") == ("Test_name", False)
    assert db.search_habit(habit_name="Modifyed_test_name") == (1, True)
    #There is no need to search the description because always come along with the name, and name is more relevant because also affects the check_off_table
    assert db.search_checkoff_table(habit_name="Test_name") == (False)
    assert db.search_checkoff_table(habit_name="Modifyed_test_name") == (True)


def test_delete():
    h.delete(habit_name="Modifyed_test_name")
    assert db.search_habit(habit_name="Modifyed_test_name") == ("Modifyed_test_name", False)
    assert db.search_checkoff_table(habit_name="Modifyed_test_name") == (False)


def test_check_off_today():
    today = datetime.today().strftime("%Y-%m-%d")
    h.create(habit_name="Test_name", description="Test_description", periodicity=1,creation_date="2025-01-01" )
    h.check_off_today(habit_name="Test_name", periodicity=1)
    assert db.search_check_off(habit_name="Test_name",check_off_date=today) == [(today)]
    #I have to delete the habit and create again because check off today creates innecesary difficulties to test wehn trying to verify the struggle functions.
    h.delete(habit_name="Test_name")
    h.create(habit_name="Test_name", description="Test_description", periodicity=1,creation_date="2025-01-01" )

def test_check_off_date():
    h.check_off_date(habit_name="Test_name",check_off_date="2025-01-30", periodicity=1)
    assert db.search_check_off(habit_name="Test_name",check_off_date="2025-01-30") == ["2025-01-30"]
    assert db.search_check_off(habit_name="Test_name",check_off_date="2025-01-29") == [] #Ensure that not previosu days are being checked off, only the selected one




"""Testing of analytics module"""


def test_list():
    assert analytics.list_habits() == ['habit_name, description, periodicity, creation_date', ('Test_name', 'Test_description', 1, '2025-01-01')]

def test_same_period():
    assert analytics.same_period(1) == [('Test_name',)]

def test_longest_streak():
    #To ensure that it really compare between several habits, let's create another 2 habits(with different periodicities) and check off them today.
    h.create(habit_name="Test_name2", description="Test_description2", periodicity=2,creation_date="2025-01-01" )
    h.check_off_date(habit_name="Test_name2",check_off_date="2025-01-30", periodicity=2)
    h.create(habit_name="Test_name3", description="Test_description3", periodicity=3,creation_date="2025-01-01" )
    h.check_off_date(habit_name="Test_name3",check_off_date="2025-01-30", periodicity=3)
    assert analytics.overall_streak() == 3

def test_streak():
    assert analytics.streak(habit_name="Test_name") == 1
    assert analytics.streak(habit_name="Test_name2") == 2
    assert analytics.streak(habit_name="Test_name3") == 3

def test_longest_struggle():
    assert analytics.overall_struggle() == 29

def test_struggle():
    assert analytics.struggle(habit_name="Test_name") == 29
    assert analytics.struggle(habit_name="Test_name2") == 28
    assert analytics.struggle(habit_name="Test_name3") == 27
    db.erase("test.db")#finally I delete the db to not create incompatibility if the test is run more than once


