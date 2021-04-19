from menu import main_menu
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='0926',
                             db='meal_plan',
                             charset='utf8mb4')

main_menu(connection)
connection.commit()
print("Closing connection to database...\n")
connection.close()
print("Goodbye!\n")





