from menu import main_menu
from print_methods import cls
import pymysql
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='0926',
                             db='meal_plan',
                             charset='utf8mb4')
cursor = connection.cursor()

cls()
print("Hi! This is a meal planning calculator that uses information \n "
      "from the most reliable and complete nutritional database out there,\n"
      " compiled by the USDA. You can decide what nutrient requirements\n"
      "you want to meet, save recipes, and test out meal plans. Search \n"
      "for nutrients, food items, recipes, and plans using either name or ID - \n"
      "and no need to worry about being exact! It's fast, simple, \n"
      "and intuitive. Just give it a go! \n \n \n")

input("Press any key to continue...")
cls()
main_menu(cursor)
connection.commit()
cursor.close()
print("Closing connection to database...\n")
connection.close()
print("Goodbye!\n")





