from datetime import datetime
import db

class Habit:

    def __init__(self, habit_name, description, frequency,creation_date):
        self.habit_name = habit_name
        self.description = description
        self.frequency = frequency
        self.creation_date = creation_date


    def create(self,habit_name, description, frequency,creation_date):

        db.insert_habit(habit_name, description, frequency,creation_date)
        db.create_habit_checkoff_table(habit_name, creation_date)#creation date is used as first date of the check off table with checking = 0 by default.
        return True


    def modify(self, habit_name, new_habit_name, new_description):
       
        #Modify the habits table
        db.rename_habit_in_habits_table(new_habit_name, new_description, habit_name)
       
        #Modify the name of the check off table
        db.rename_habit_checkoff_table(new_habit_name, habit_name)
        return True

    def delete(self,habit_name):

        db.delete_habit_in_habits_table(habit_name)
        db.delete_habit_checkoff_table(habit_name)
        return True


    def check_off_today(self,habit_name,frequency):

        today = datetime.today().strftime("%Y-%m-%d")
        check_off_date = today
        db.create_intermediate_dates_checkoff_table(habit_name, check_off_date)
        db.check_off(habit_name, check_off_date,frequency)
        db.show_check_off(habit_name,check_off_date,frequency)
        return True
    


    def check_off_date(self,habit_name,check_off_date,frequency):

        check_off_date = db.compare_creation_checkoff_dates(habit_name,check_off_date) #In case the user introduces a check off date posterior to the creation date, this is solved assking to rewirte it and through this function the new valid input is transmitted to the rest of habit class.
        db.create_intermediate_dates_checkoff_table(habit_name, check_off_date) 
        db.check_off(habit_name, check_off_date,frequency)
        db.show_check_off(habit_name,check_off_date,frequency)
        return True
    
