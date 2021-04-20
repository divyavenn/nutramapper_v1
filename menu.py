from print_methods import *
from nutrient import *
from recipe import *
from ingredient import *
from plan import *
from meal import *

def main_menu(cursor):
    cls()
    options = ['View/Edit Tracked Nutrients',
               'View Information for a Food Item',
               'View/Edit Recipes',
               'View/Edit Plans']
    choice = make_menu(options)
    if (choice == 1):
        nutrient_menu(cursor)
    elif (choice == 2):
        food_item_menu(cursor)
    elif (choice == 3):
        recipe_menu(cursor)
    elif (choice == 4):
        plan_menu(cursor)

def nutrient_menu(cursor):
    cls()
    options = ['View Nutrient Requirements',
              'Add Nutrient Requirement to Track',
              'Update Nutrient Requirement',
              'Remove Nutrient Requirement Tracked',
              'Return to Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        cls()
        nutr_to_track = get_nutrients_to_track(cursor)
        if (nutr_to_track is not None):
            print("Nutrients requirements being monitored: \n")
            for n in nutr_to_track:
                print_nutrient_requ(n)
        else:
            print("No nutrients are currently being tracked.")
        input("\n \n Press any key to continue.")
        nutrient_menu(cursor)
    elif (choice == 2):
        cls()
        add_nutrients_to_track(cursor, None)
        cursor.execute("commit")
        nutrient_menu(cursor)
    elif (choice == 3):
        cls()
        update_nutrients_to_track(cursor, None)
        nutrient_menu(cursor)
    elif (choice == 4):
        cls()
        remove_nutrients_to_track(cursor)
        nutrient_menu(cursor)
    elif (choice == 5):
        main_menu(cursor)

def food_item_menu(cursor):
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
    main_menu(cursor)

def recipe_menu(cursor):
    cls()
    options = ['View/Update Recipes',
              'Create New Recipe',
               'Return To Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        if (print_recipe_list(cursor)):
            recipe = search_recipe(cursor, None)
            recipe_update_menu(cursor, recipe)
        recipe_menu(cursor)
    elif (choice == 2):
        cls()
        add_recipe(cursor)
        recipe_menu(cursor)
    elif (choice == 3):
        main_menu(cursor)


def recipe_update_menu(cursor, recipe):
    recipe_id = recipe[0]
    cls()
    print_recipe(cursor, recipe)
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
            recipe_update_menu(cursor,recipe)
        elif(choice == 2):
            add_ingredient(cursor, recipe_id, None)
            recipe_update_menu(cursor,recipe)
        elif(choice==3):
            remove_ingredient(cursor, recipe_id, None)
            recipe_update_menu(cursor, recipe)
        elif (choice == 4):
            rename_recipe(cursor, recipe_id)
            recipe_update_menu(cursor, recipe)
        elif (choice==5):
            delete_recipe(cursor, recipe_id)
            recipe_menu(cursor)
        elif(choice==6):
            main_menu(cursor)

def plan_update_menu(cursor, plan):
    plan_id = plan[0]
    cls()
    print_plan(cursor, plan)
    if input_yes("Would you like to update this plan?"):
        options = ['Add Recipe To Plan',
                   'Remove Recipe From Plan',
                   'Change Number of Days This Plan covers',
                   'Update Number of Servings of a Recipe',
                   'Rename Plan',
                   'Delete Plan',
                   'Return to Main Menu']
        choice = make_menu(options)
        if (choice == 1):
            add_meal(cursor, plan_id, None)
            plan_update_menu(cursor, plan)
        elif (choice == 2):
            remove_meal(cursor, plan_id, None)
            plan_update_menu(cursor, plan)
        elif (choice == 3):
            change_plan_days(cursor, plan_id)
            plan_update_menu(cursor, plan)
        elif (choice == 4):
            alter_meal(cursor, plan_id)
            plan_update_menu(cursor, plan)
        elif (choice == 5):
            rename_plan(cursor, plan_id)
            plan_update_menu(cursor, plan)
        elif (choice == 6):
            remove_plan(cursor, plan_id)
            plan_menu(cursor)
        elif (choice == 7):
            main_menu(cursor)

def plan_menu(cursor):
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
            plan_update_menu(cursor, plan)
        plan_menu(cursor)
    elif (choice == 2):
        cls()
        add_plan(cursor)
        plan_menu(cursor)
    elif (choice == 3):
        main_menu(cursor)


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

