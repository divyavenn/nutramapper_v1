from print_methods import *
from nutrient import *
from recipe import *
from ingredient import *
from plan import *
from meal import *

def main_menu(connection):
    cls()
    options = ['View/Edit Tracked Nutrients',
               'View Information for a Food Item',
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

def nutrient_menu(connection):
    cursor = connection.cursor()
    print_nutrient_requ_list(cursor)
    if (input_yes("\n \n Would you like to change which nutrients are tracked \n or update the nutrient requirements?")):
        cls()
        options = ['Add Nutrient Requirement to Track',
                  'Update Nutrient Requirement',
                  'Remove Nutrient Requirement Tracked',
                  'Return to Main Menu']
        choice = make_menu(options)
        if (choice == 1):
            cls()
            add_nutrients_to_track(cursor, None)
            cursor.execute("commit")
            nutrient_menu(connection)
        elif (choice == 2):
            cls()
            update_nutrients_to_track(cursor, None)
            nutrient_menu(connection)
        elif (choice == 3):
            cls()
            remove_nutrients_to_track(cursor)
            nutrient_menu(connection)
        elif (choice == 4):
            main_menu(connection)
    else:
        main_menu(connection)

def food_item_menu(connection):
    cursor = connection.cursor()
    cls()
    #search_food_item(cursor, food_id/None) -> [food_id, food_name, cost_per_100]
    food = search_food_item(cursor, None)
    # get_nutrients_to_track(cursor) -> [nutrient_id, nutrient name, daily requirement, units]
    nutrients_to_track = get_nutrients_to_track(cursor)
    if (nutrients_to_track is not None):
        # print_tracked_nutr_food(cursor, food, tracked_nutrients) -> None
        print_tracked_nutr_food(cursor, food, nutrients_to_track)
    else:
        print("No nutrients are being tracked.")
    input("\n \n Press any key to return to the main menu.")
    main_menu(connection)

def recipe_menu(connection):
    cls()
    cursor = connection.cursor()
    options = ['View/Update Recipes',
              'Create New Recipe',
               'Return To Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        if (print_recipe_list(cursor)):
            if(input_yes("Would you like to update any recipes?")):
                recipe = search_recipe(cursor, None)
                recipe_update_menu(connection, recipe)
        else:
            input("\n \n Press any key to continue...")
        recipe_menu(connection)
    elif (choice == 2):
        cls()
        add_recipe(cursor)
        recipe_menu(connection)
    elif (choice == 3):
        main_menu(connection)


def recipe_update_menu(connection, recipe):
    cls()
    cursor = connection.cursor()
    recipe_id = recipe[0]
    recipe = search_recipe(cursor,recipe_id)
    if (recipe is None):
        print("This recipe doesn't exist anymore.")
        input("\n \n Press any key to continue...")
        recipe_menu(connection)
    if input_yes("Would you like to update this recipe?"):
        options = ['Alter Ingredient Quantity',
                   'Add Ingredient',
                   'Remove Ingredient',
                   'Rename Recipe',
                   'Delete Recipe',
                   'Return to Main Menu']
        choice = make_menu(options)
        if (choice == 1):
            alter_ingredient(cursor, recipe_id, None)
            recipe_update_menu(connection,recipe)
        elif(choice == 2):
            add_ingredient(cursor, recipe_id, None)
            recipe_update_menu(connection,recipe)
        elif(choice==3):
            remove_ingredient(cursor, recipe_id, None)
            recipe_update_menu(connection, recipe)
        elif (choice == 4):
            rename_recipe(cursor, recipe_id)
            recipe_update_menu(connection, recipe)
        elif (choice==5):
            delete_recipe(cursor, recipe_id)
            recipe_menu(connection)
        elif(choice==6):
            main_menu(connection)

def plan_update_menu(connection, plan):
    cursor = connection.cursor()
    cls()
    plan_id = plan[0]
    plan = search_plan(cursor, plan_id)
    if(plan is None):
        print("This plan doesn't exist anymore.")
        input("\n \n Press any key to continue...")
        plan_menu(connection)
    print_plan(cursor, plan)
    if input_yes("\n \n Would you like to update this plan?"):
        options = ['Add Recipe To Plan',
                   'Remove Recipe From Plan',
                   'Change Number of Days This Plan covers',
                   'Update Number of Servings of a Recipe',
                   'Rename Plan',
                   'Delete Plan',
                   'Return to Main Menu']
        choice = make_menu(options)
        if (choice == 1):
            cls()
            add_meal(cursor, plan_id, None)
            plan_update_menu(connection, plan)
        elif (choice == 2):
            cls()
            remove_meal(cursor, plan_id, None)
            plan_update_menu(connection, plan)
        elif (choice == 3):
            cls()
            change_plan_days(cursor, plan_id)
            plan_update_menu(connection, plan)
        elif (choice == 4):
            cls()
            alter_meal(cursor, plan_id)
            plan_update_menu(connection, plan)
        elif (choice == 5):
            cls()
            rename_plan(cursor, plan_id)
            plan_update_menu(connection, plan)
        elif (choice == 6):
            cls()
            remove_plan(cursor, plan_id)
            plan_menu(connection)
        elif (choice == 7):
            main_menu(connection)

def plan_menu(connection):
    cursor = connection.cursor()
    cls()
    choice = None
    if (choice is None):
        options = ['View/Update Meal Plan',
                   'Create New Meal Plan',
                   'Return To Main Menu']
        choice = make_menu(options)
    if (choice == 1):
        cls()
        if (print_plan_list(cursor) == False):
            if (input_yes("There aren't any meal plans. Would you like to add one?")):
                add_plan(cursor)
        else:
            plan = search_plan(cursor, None)
            plan_update_menu(connection, plan)
        plan_menu(connection)
    elif (choice == 2):
        cls()
        add_plan(cursor)
        plan_menu(connection)
    elif (choice == 3):
        main_menu(connection)


def make_menu(opt):
    loop = True
    while loop:
        print_menu(opt)
        x = input_number("Enter your choice " + str(1) + " to " + str(len(opt)))
        for i in range(1, len(opt ) + 1):
            if x == str(i):
                return i
        if x == str(0):
            loop = False
        else:
            print("Invalid option selection. \n")

