from menu import main_menu
from print_methods import cls
from recipe import *

#returns connection
def try_connect():
    cls()
    u_name = input("Please enter your MySQL server username.")
    pword = input("Please enter your MySQL server password.")
    prt = input("If you have a specific port number in mind, type it in. \nIf not, press enter and we'll assume the default of 3306.")
    # returns -2 for empty input, -1 for invalid input, 0 for name, 1 for id
    if (input_form(prt) == -2):
        prt = 3306
    elif not (input_form(prt) == 1):
        print("Oops! Looks like you tried to input a port number that wasn't a number. Try again!")
        input("\n \n \n Press any key to continue...")
        return try_connect()
    try:
        connection = pymysql.connect(host='localhost',
                                     port=prt,
                                     user=u_name,
                                     password=pword,
                                     db='meal_plan',
                                     charset='utf8mb4')
        return connection
    except:
        print("Either your credentials weren't right or your server isn't running. Try again.")
        input("\n \n \n Press any key to continue...")
        return try_connect()

def intro():
    cls()
    print("Hi! This is a meal planning calculator that uses information \n"
          "from the most reliable and complete nutritional database out there,\n"
          "compiled by the USDA. You can decide what nutrient requirements\n"
          "you want to meet, save recipes, and test out meal plans. Search \n"
          "for nutrients, food items, recipes, and plans using either name or ID - \n"
          "and no need to worry about being exact! It's fast, simple, \n"
          "and intuitive. Just give it a go!")

    input("\n \n \n Press any key to continue...")
    cls()
    print("First, we need to connect to your SQL server. Make sure \n"
          "that both the USDA database and the meal plan database \n"
          "have been imported and that your server is running.")

    input("\n \n \n Press any key to continue...")

    connection = try_connect()
    cls()
    print("Connection successful! Ready to start?")

    input("\n \n \n Press any key to continue...")
    cls()
    return connection

#connection = intro()
connection = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     password='0926',
                                     db='meal_plan',
                                     charset='utf8mb4')

main_menu(connection)
print("Committing changes...\n")
connection.commit()
print("Closing connection to database...\n")
connection.close()
print("Goodbye!\n")





