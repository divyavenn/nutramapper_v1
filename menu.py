from print_methods import *
from data_validation import *
from nutrient import *
from recipe import *
from search import *
from ingredient import *
from plan import *
def main_menu(cursor):
    options = ['View/Edit Tracked Nutrients',
               'View/Edit Food Items',
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
    options = ['View Nutrient Requirements',
              'Add Nutrient Requirement to Track',
              'Update Nutrient Requirement',
              'Remove Nutrient Requirement Tracked',
              'Return to Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        nutr_to_track = get_nutrients_to_track(cursor)
        print("Nutrients requirements being monitored: \n")
        for n in nutr_to_track:
            print_nutrient_requ(n)
        nutrient_menu(cursor)
    elif (choice == 2):
        add_nutrients_to_track(cursor, None)
        cursor.execute("commit")
        nutrient_menu(cursor)
    elif (choice == 3):
        update_nutrients_to_track(cursor, None)
        nutrient_menu(cursor)
    elif (choice == 4):
        remove_nutrients_to_track(cursor)
        nutrient_menu(cursor)
    elif (choice == 5):
        main_menu(cursor)

def food_item_menu(cursor):
    options = ['View Information For a Food Item',
              'Return to Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        #search_food_item(cursor, food_id/None) -> [food_id, food_name, cost_per_100]
        food = search_food_item(cursor, None)
        print_tracked_nutr_food(cursor, food[0])
        food_item_menu(cursor)
    elif (choice == 2):
        main_menu(cursor)

def recipe_menu(cursor):
    options = ['View/Update Recipes',
              'Create New Recipe',
               'Return To Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        if (print_recipe_list()):
            recipe = search_recipe(cursor, None)
            print_recipe(cursor, recipe[0])
            recipe_update_menu(cursor, recipe[0])
        recipe_menu(cursor)
    elif (choice == 2):
        add_recipe(cursor)
        recipe_menu(cursor)
    elif (choice == 3):
        main_menu(cursor)


def recipe_update_menu(cursor, recipe_id):
    if input_yes("Would you like to update this recipe?"):
        options = ['Alter Ingredient Quantity',
                   'Add Ingredient',
                   'Remove Ingredient',
                   'Rename Recipe',
                   'Delete Recipe',
                   'Return to Main Menu']
        choice = make_menu(options)
        if (choice == 1):
            alter_ingredient(cursor, recipe_id)
            recipe_update_menu(cursor)
        elif(choice == 2):
            add_ingredient(cursor, recipe_id, None)
            recipe_update_menu(cursor)
        elif(choice==3):
            remove_ingredient(cursor, recipe_id)
            recipe_update_menu(cursor)
        elif (choice == 4):
            rename_recipe(cursor, recipe_id)
        elif (choice==5):
            delete_recipe(cursor, recipe_id)
        elif(choice==6):
            main_menu(cursor)

def plan_update_menu(cursor, plan_id):
    options = ['Add Meal',
               'Remove Meal',
               'Update number of servings',
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
        if (print_plan_list(cursor) == False):
            if (input_yes("There aren't any meal plans. Would you like to add one?")):
                add_plan(cursor)
        else:
            plan = search_plan(cursor, None)
            print_plan(cursor, plan[0])
            plan_update_menu(cursor, plan[0])
        plan_menu(cursor, None)
    elif (choice == 2):
        add_plan(cursor)
        plan_menu(cursor, None)
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

