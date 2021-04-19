

# --------------------------------------------------------------MENU FUNCTIONS--------------------------------------------------------------------
def print_menu(options):
    print(30 * "-" + "MENU" + 30 * "-" + "")
    i = 1
    for opt in options:
        opt_stmt = str(i) + ":" + opt + ""
        print(opt_stmt)
        i = i + 1
    print(67 * "-" + "")
    print("**Type 0 to end program.")
def make_menu(opt):
    loop = True
    while loop:
        print_menu(opt)
        x = input("Enter your choice " + str(1) + " to " + str(len(opt)))
        for i in range(1, len(opt ) +1):
            if x == str(i):
                return i
        if x == str(0):
            loop = False  # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-5 we print an error message
            print("Invalid option selection. \n")

def nutrient_menu(connection):
    cursor = connection.cursor()
    options = ['View Nutrient Requirements',
              'Add Nutrient Requirement to Track',
              'Update Nutrient Requirement',
              'Remove Nutrient Requirement Tracked',
              'Return to Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        nutr_to_track = get_nutrients_to_track(cursor)
        print("Nutrients that are currently being tracked: \n")
        print_nutrient_info(nutr_to_track)
        nutrient_menu(connection)
    elif (choice == 2):
        add_nutrients_to_track(cursor, None)
        cursor.execute("commit")
        nutrient_menu(connection)
    elif (choice == 3):
        update_nutrients_to_track(cursor, None)
        connection.commit()
        nutrient_menu(connection)
    elif (choice == 4):
        remove_nutrients_to_track(cursor)
        connection.commit()
        nutrient_menu(connection)
    elif (choice == 5):
        main_menu(connection)

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

def main_menu(connection):
    cursor = connection.cursor()
    options = ['View/Edit Tracked Nutrients',
               'View/Edit Ingredients',
               'View/Edit Recipes',
               'View/Edit Plans']
    choice = make_menu(options)
    if (choice == 1):
        nutrient_menu(connection)
    elif (choice == 2):
        food_item_menu(connection)
    elif (choice == 3):
        recipe_menu(connection)
    elif (choice == 4):
        plan_menu(connection)


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





