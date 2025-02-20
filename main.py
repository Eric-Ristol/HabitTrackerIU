import habit
import db
import analytics
from datetime import datetime

"""Build functions to ensure correct inputs"""


def empty(value):
    #This function ensures that the user does not enter an empty value, eliminates innecesary spaces, and avoids the user to introduce special characters.
    #In case of just inncesary spaces, the function eliminates them, and don't ask the suer to write the sentence again
    while True:
        check = value.strip()
        if all(char.isalnum() or char.isspace() for char in check) and check:
            return check
        print("This value is empty, or has special characters. Please enter valid value.")
        value = input("Try again: ")


def date_format(date):
    #Date _format is intended to force the user to introduce a date in the format YYYY-MM-DD, also avoids the user to introduce a date with spaces.
    #There is no need to execute date_format with empty().
    while True:
        try:
            date.strip()
            return datetime.strptime(date, "%Y-%m-%d").date()#Note: the .date() transforms the datetime object with date and time to only date
        except ValueError:
            date = input("Your date does not follow (YYYY-MM-DD). Try again:")




def main():
    #Initalizing functions
    db.connection("main.db")
    analytics.connection("main.db")
    db.create_habits_table()
    h = habit.Habit(0,0,1,"0000-00-00")

    #I should forece somehow the user to create a habit before any other action, becasuse otherwise the habit object is not defined and due to that is not possoble do any action.
    while True:
        print("\nHabit Tracker CLI")
        print("\n1. Create a new habit")
        print("2. Modify an existing habit")
        print("3. Delete habit")
        print("4. Check off habit")
        print("5. Analytics module")
        print("\n6. Exit")
        choice = empty(input("\nEnter your choice (1-6): "))



        if choice == "1":
            print("\nCreating a new habit...")

            habit_name = empty(input("Enter the habit name(no special characters, numbers allowed): "))
            habit_name = habit_name.replace(" ", "_")
            habit_name, success = db.search_habit(habit_name) #The retunr of habit_name is not usefull.
            if success:
                print("This habit already exist!")
                continue
            description = empty(input("Enter the habit description(no special characters, numbers allowed): "))
            description = description.replace(" ", "_")
            while True: #Check if the input value is an integer or not, and if not asks again until an intger is introduced.
                try:
                    periodicity = int(input("Enter the periodicity (in days): "))
                    if periodicity < 1:
                        print("The periodicity has to be greater than 0!")
                        return int(empty(str(periodicity)))#I have to transform the value into a string to manage it with the empty function because .strip is not possible with integers.Finally I transform it again into an INTEGER because the database only manages INTEGER in the periodicicty value.
                    break
                except ValueError:
                    print("This value has to be an integer!")
            
            today = datetime.today().strftime("%Y-%m-%d")
            custom_date = str(date_format(input("Enter the creation date (YYYY-MM-DD): "))) #For testing reasons, usually self.creation_date = today
            creation_date = custom_date
            
            if h.create(habit_name, description, periodicity,creation_date):
                habit_name = habit_name.replace("_", " ")
                print(f"Habit '{habit_name}' created successfully!")
    


        elif choice == "2":
            print("\nModifying an existing habit...")

            habit_name = empty(input("Enter the name of the habit you want to modify: "))
            habit_name = habit_name.replace(" ", "_")
            #Look for the existence of the habit.
            search_result, success = db.search_habit(habit_name) #In this case periodicity is not used, but I have to creaste the variable because the function return 2 values, one is periodicity and the other is a boolean.
            if not success:
                print("This habit does not exist!")
                continue #If the habit is not found, the rest of the function is not executed.
            
            #Assignation of new values for th habit
            new_habit_name = input("What is the new name of the habit(no special characters, numbers allowed): ")
            new_habit_name = new_habit_name.replace(" ", "_")
            new_description = input("What is the new description of the habit(no special characters, numbers allowed): ")
            new_description = new_description.replace(" ", "_")

            if h.modify(habit_name,new_habit_name,new_description):
                habit_name = habit_name.replace("_", " ")
                print(f"Habit '{habit_name}' modified successfully!")



        elif choice == "3":
            print("\nDeleting a habit...")

            habit_name = empty(input("Enter the name of the habit you want to delete: "))
            habit_name = habit_name.replace(" ", "_")
            #Look for the existence of the habit.
            search_result, success = db.search_habit(habit_name)
            if not success:
                print("This habit does not exist!")
                continue #If the habit is not found, the rest of the function is not executed.
            if h.delete(habit_name):
                habit_name = habit_name.replace("_", " ")
                print(f"Habit '{habit_name}' deleted successfully!")



        elif choice == "4":
            print("\nChecking off...")

            habit_name = empty(input("Enter the name of the habit you want to check off: "))
            habit_name = habit_name.replace(" ", "_")
            #Look for the existence of the habit and get the periodicty of the habit.
            periodicity, success = db.search_habit(habit_name)
            if not success:
                print("This habit does not exist!")
                """habit_name = empty(input("Enter the name of the habit you want to check off(no special characters, numbers allowed): "))"""#This is an optional functionality that can be added but I don't like bacause it makes impossible to go out if you don;t remember some habit name, but still I think it's a good to keep it in case I want to improve that creating som ekind of sub menu to choose if search again or if directly create what was written.
                continue #If the habit is not found, the rest of the function is not executed.

            #Think if create a loop here to not expulsae the user outsuide the submenu
            #Sub menu to choose if check off today or any other date in the past.
            print("\nChoose if you want to check off today or any other date in the past.")
            print("1. Check off today")
            print("2. Check off any other date")
            decision = empty(input("Enter your choice (1-2): "))

            if decision == "1":
                if  h.check_off_today(habit_name,periodicity):
                    habit_name = habit_name.replace("_", " ")
                    print(f"Habit '{habit_name}' checked off successfully!")
            
            elif decision == "2":
                check_off_date = str(date_format(input("Enter the date you want to check off (YYYY-MM-DD): ")))# I need to convert it to string because date_format returns a dattime object
                if h.check_off_date(habit_name,check_off_date,periodicity):
                    habit_name = habit_name.replace("_", " ")
                    print(f"Habit '{habit_name}' checked off at {check_off_date} successfully!")

            else:
                print("Invalid choice. Please enter a number between 1 and 2.")
                return

        elif choice == "5":
            analytics.module()
            
        elif choice == "6":
            print("Exiting the Habit Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()