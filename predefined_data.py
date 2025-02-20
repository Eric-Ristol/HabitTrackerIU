import habit
import db
import analytics


#Initalizing functions
h = habit.Habit("0","0",1,"2000-01-01") #class initialization
db.connection("main.db")
analytics.connection("main.db")
db.create_habits_table()


"""Habits creation"""


h.create(habit_name="Walk", description="Walk_at_least_for_30_minutes", periodicity=1,creation_date="2025-01-01" )
h.create(habit_name="Sterching_session", description="One_hour", periodicity=3,creation_date="2025-01-01" )
h.create(habit_name="House_cleaning", description="", periodicity=7,creation_date="2025-01-01" )
h.create(habit_name="Personal_accounting", description="Update_excel_worksheet", periodicity=15,creation_date="2025-01-01" )
h.create(habit_name="Weekend_getaway", description="Go_to_beach_house", periodicity=30,creation_date="2025-01-01" )


"""Checks off"""

"""It's imprtant to notice that if an habit of for instance 7 days is checked off at 2025-01-04, only 4 days will be checked off, because cehcks are not computed before creation_date"""
#Walk. Streak 8
h.check_off_date(habit_name="Walk", check_off_date="2025-01-01", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-02", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-03", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-04", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-05", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-06", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-07", periodicity=1)

h.check_off_date(habit_name="Walk", check_off_date="2025-01-10", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-11", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-12", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-13", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-14", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-15", periodicity=1)

h.check_off_date(habit_name="Walk", check_off_date="2025-01-18", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-19", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-20", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-21", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-22", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-23", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-24", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-25", periodicity=1)

h.check_off_date(habit_name="Walk", check_off_date="2025-01-28", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-29", periodicity=1)
h.check_off_date(habit_name="Walk", check_off_date="2025-01-30", periodicity=1)


#Streching saession. Streak 13
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-01", periodicity=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-04", periodicity=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-07", periodicity=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-10", periodicity=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-13", periodicity=3)

h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-19", periodicity=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-22", periodicity=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-25", periodicity=3)
h.check_off_date(habit_name="Sterching_session", check_off_date="2025-01-28", periodicity=3)


#House cleaning. Streak 14
h.check_off_date(habit_name="House_cleaning", check_off_date="2025-01-07", periodicity=7)
h.check_off_date(habit_name="House_cleaning", check_off_date="2025-01-14", periodicity=7)

h.check_off_date(habit_name="House_cleaning", check_off_date="2025-01-28", periodicity=7)


#Personal accounting. Streak 15
h.check_off_date(habit_name="Personal_accounting", check_off_date="2025-01-05", periodicity=15)
h.check_off_date(habit_name="Personal_accounting", check_off_date="2025-01-15", periodicity=15)

#Weekend getaway. Streak 23
h.check_off_date(habit_name="Weekend_getaway", check_off_date="2025-01-23", periodicity=30)

