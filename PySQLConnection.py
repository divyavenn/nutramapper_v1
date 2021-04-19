

# --------------------------------------------------------------MENU FUNCTIONS--------------------------------------------------------------------

def food_item_menu(connection):
    cursor = connection.cursor()
    options = ['View Information For a Food Item',
              'Update Cost Of Food Item',
              'Return to Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        connection.commit()
        food_item_menu(connection)
    elif (choice == 2):
        connection.commit()
        food_item_menu(connection)
    elif (choice == 3):
        main_menu(connection)


def recipe_update_menu(connection, recipe_id):
    cursor = connection.cursor
    x = input("Would you like to update this recipe? [Y/N]")
    if (x == "Y"):
        options = ['Alter Ingredient Quantity',
                   'Add Ingredient',
                   'Remove Ingredient',
                   'Rename Recipe',
                   'Delete Recipe',
                   'Return to Main Menu']
        choice = make_menu(options)
        if (choice == 1):
            alter_ingredient(cursor, recipe_id)
            connection.commit()
            recipe_update_menu(connection)
        elif(choice == 2):
            add_ingredient(cursor, recipe_id, None)
            connection.commit()
            recipe_update_menu(connection)
        elif(choice==3):
            remove_ingredient(cursor, recipe_id)
            connection.commit()
            recipe_update_menu(connection)
        elif (choice == 4):
            rename_recipe(cursor, recipe_id)
            connection.commit()
        elif (choice==5):
            delete_recipe(cursor, recipe_id)
            connection.commit()
        elif(choice==6):
            main_menu(connection)
def recipe_menu(connection):
    cursor = connection.cursor()
    options = ['View/Update Recipes',
              'Create New Recipe',
               'Return To Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        if (view_recipe_list(cursor) == False):
            if (input("There aren't any recipes. Would you like to add one? [Y/N]") == "Y"):
                add_recipe(cursor)
                connection.commit()
        else:
            recipe = search_recipe(cursor ,None)
            view_recipe(cursor, recipe[0])
            recipe_update_menu(connection, recipe[0])
            connection.commit()
        recipe_menu(connection)
    elif (choice == 2):
        print('create new recipe')
        add_recipe(cursor)
        connection.commit()
        recipe_menu(connection)
    elif (choice == 3):
        main_menu(connection)

def plan_update_menu(cursor, plan_id):
    options = ['Add Meal',
               'Remove Meal',
               'Alter number of servings',
               'Rename Plan',
               'Delete Plan',
               'Return to Main Menu']

def plan_menu(cursor, choice):
    if (choice is None):
        options = ['View/Update Meal Plan',
              'Create New Meal Plan',
               'Return To Main Menu']
        choice = make_menu(options)
    if (choice == 1):
        if (view_plan_list(cursor) == False):
            if (input("There aren't any meal plans. Would you like to add one? [Y/N]") == "Y"):
                add_plan(cursor)
        else:
            plan = search_plan(cursor, None)
            view_plan(cursor, plan[0])
            plan_update_menu(cursor, plan[0])
            connection.commit()
        plan_menu(cursor, None)
    elif (choice == 2):
        add_plan(cursor)
        plan_menu(cursor, None)
    elif (choice == 3):
        main_menu(cursor)




# -----------------------------------------------------------------MAIN--------------------------------------------------------------------

"""connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='0926',
                             db='meal_plan',
                             charset='utf8mb4')"""

#main_menu(connection)
#connection.commit()
#print("Closing connection to database...\n")
#connection.close()
#print("Goodbye!\n")





