import habit
import db
import analytics


#Initalizing functions
h = habit.Habit("0","0",1,"2000-01-01") #assignation of habit class to a variable
db.connection("main.db")
analytics.connection("main.db")
db.create_habits_table()


"""Habits creation"""


h.create(habit_name="Walk", description="Walk_at_least_for_30_minutes", frequency=1,creation_date="2025-01-01" )
h.create(habit_name="Sterching_session", description="One_hour", frequency=3,creation_date="2025-01-01" )
h.create(habit_name="House_cleaning", description="", frequency=7,creation_date="2025-01-01" ) #Description can be empty
h.create(habit_name="Personal_accounting", description="Update_excel_worksheet", frequency=15,creation_date="2025-01-01" )
h.create(habit_name="Weekend_getaway", description="Go_to_beach_house", frequency=30,creation_date="2025-01-01" )


"""Checks off"""

"""It's imprtant to notice that if an habit of for instance 7 days is checked off at 2025-01-04, only 4 days will be checked off, because cehcks are not computed before creation_date"""
#Walk. Streak 8
h.check_off_date(habit_name="Walk", check_off_date="2025-01-01", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-02", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-03", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-04", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-05", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-06", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-07", frequency=1)

h.check_off_date(habit_name="Walk", check_off_date="2025-01-10", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-11", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-12", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-13", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-14", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-15", frequency=1)

h.check_off_date(habit_name="Walk", check_off_date="2025-01-18", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-19", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-20", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-21", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-22", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-23", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-24", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-25", frequency=1)

h.check_off_date(habit_name="Walk", check_off_date="2025-01-28", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-29", frequency=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-30", frequency=1)


#Streching saession. Streak 13
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-01", frequency=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-04", frequency=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-07", frequency=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-10", frequency=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-13", frequency=3)

h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-19", frequency=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-22", frequency=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-25", frequency=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-28", frequency=3)


#House cleaning. Streak 14
h.check_off_date(habit_name="House_cleaning", check_off_date="2025-01-07", frequency=7)
h.check_off_date(habit_name="House_cleaning", check_off_date="2025-01-14", frequency=7)

h.check_off_date(habit_name="House_cleaning", check_off_date="2025-01-28", frequency=7)


#Personal accounting. Streak 15
h.check_off_date(habit_name="Personal_accounting", check_off_date="2025-01-05", frequency=15)
h.check_off_date(habit_name="Personal_accounting", check_off_date="2025-01-15", frequency=15)

#Weekend getaway. Streak 23
h.check_off_date(habit_name="Weekend_getaway", check_off_date="2025-01-23", frequency=30)
