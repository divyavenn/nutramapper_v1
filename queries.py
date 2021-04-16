import pymysql
import cryptography

#Searches for ingredient by name, returns nutritonal data
def find_ingredient(cursor):
    foodList = []
    cursor.execute("select food_name from food_item limit 5")
    for x in cursor:
        foodList.append(str(x[0]).lower())
    print(foodList)

    food = input("Enter an ingredient name. \n")
    while not (food in foodList):
        food = input("Not a valid ingredient. Try again. \n")
    stmt = "select food_id, food_name from food_item where food_name = '" + food + "'"
    cursor.execute(stmt)

    nut_id = ''
    for x in cursor:
        nut_id = (x[0])
    return(nut_id)