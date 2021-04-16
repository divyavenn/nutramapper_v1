import queries
import cryptography
import pymysql

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




