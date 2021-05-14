from menu import main_menu
from print_methods import cls
from recipe import *
import sqlite3
#returns connection
def try_connect():
    cls()
    try:
        connection = sqlite3.connect("../meal_planner.db"
        return connection
    except:
        print("Could not connect to database file.")
        input("\n \n \n Press any key to continue...")

def intro():
    cls()
    connection = try_connect()
    print("Connection successful! Ready to start?")
    input("\n \n \n Press any key to continue...")
    cls()
    return connection

#connection = intro()
connection = intro()
main_menu(connection)
print("Committing changes...\n")
connection.commit()
print("Closing connection to database...\n")
connection.close()
print("Goodbye!\n")





