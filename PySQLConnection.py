
import cryptography
import pymysql
import importlib

def search(cursor, dialogue, allCols, table, onCol):
    x = input(dialogue + "\n")
    query = "select " + allCols + " from " + table + " where " + onCol + " like '" + x + "%'"
    while not (cursor.execute(query) == 1):
        print("Not an exact match. Did you mean one of these?")
        for i in cursor:
            print(i)
        x = input(dialogue + "\n")
        query = "select " + allCols + " from " + table + " where " + onCol + " like '" + x + "%'"
    for i in cursor:
        return i



#Searches for ingredient by name, returns nutritonal data
def find_ingredient(cursor):
    x = search(cursor, "Enter a food item", "food_id, food_name", "food_item", "food_name")
    return x[0]


#------------------------------------------------------------------------------------------------------------------------------------------i
print('Hi!')
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='0926',
                             db='meal_plan',
                             charset='utf8mb4')


cursor = connection.cursor()
x = find_ingredient(cursor)
print(x)
print("Closing connection to database...\n")
cursor.close()
connection.close()
print("Goodbye!\n")




