from print_methods import print_menu, print_nutrient_requ
from data_validation import input_number
from nutrient import add_nutrients_to_track, remove_nutrients_to_track, update_nutrients_to_track, get_nutrients_to_track
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

