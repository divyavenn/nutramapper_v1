
import pymysql
from data_validation import input_form


#---------------------------------------------------------------PLAN FUNCTIONS--------------------------------------------------------

def add_plan(cursor):
    name = get_name("What is the name of this plan?")
    days = get_days("How many days does this meal plan cover?")

    cursor.execute('insert into plan (plan_name, num_days) values ( "' + name + "', " + str(days) + ")")
    plan_id = None
    # find recipe_id of new plan
    cursor.execute("select plan_id from plan where (plan_name = '" + name + "')")
    for i in cursor:
        plan_id = i[0]
    while (input("Would you like to add a recipe [Y/N]") == "Y"):
        add_meal(cursor, plan_id, None)
def remove_plan(cursor, plan_id):
    query = "delete from plan where plan_id = " + str(plan_id)
    cursor.execute(query)


def change_plan_days(cursor, plan_id):
    days = get_days("What number of days should his plan cover?")
    query = "update plan set num_days = " + str(days) + "where plan_id = " + str(plan_id)

def rename_plan(cursor, plan_id):
    new_name = input("Enter a new name for the recipe:")
    if not(input_form(new_name) == 0):
        print("That's not a valid plan name. Try again.")
        rename_plan(cursor, plan_id)
    else:
        query = "update recipe set plan_name = " + "'" + new_name + "'" + "where plan_id = " + str(plan_id)
        cursor.execute(query)


def view_plan_list(cursor):
    print("PLAN LIST")
    query = "select plan_name from plan"
    cursor.execute(query)
    plans = []
    for p in cursor:
        print(p[0])
        plans.append(p)
    if (len(plans) == 0):
        return False
    else:
        return True


def view_plan(cursor, plan_id):
    meals = get_meals_in_plan(cursor, plan-id)
    if not meals is None:
        print("This plan has: \n")
        for m in meals:
            print_meal(cursor, m)
    fulfills_nutritional_reqs(cursor, plan_id)

def get_num_days(cursor, plan_id):
    query = "select num_days from plan where plan_id = " + str(plan_id)
    cursor.execute(query)
    for i in cursor:
        return i[0]

def fulfills_nutritional_reqs(cursor, plan_id):
    meals = get_meals_in_plan()
    if not meals is None:
        daily_reqs = []
        nutrients = get_nutrients_to_track(cursor)
        for n in nutrients:
            daily_reqs.append(n[2])
        recipe_totals = []
        planwide_avg = []
        num_days = get_num_days(cursor, plan_id)
        for m in meals:
            recipe_id = m[0]
            recipe_totals.append(nutritional_total_recipe(cursor, recipe_id))
        for i in range(0,len(daily_reqs)):
            sum = 0
            for r in recipe_totals:
                sum = sum + r[i]
            planwide_avg[i] = sum/num_days
            if planwide_avg[i] < daily_reqs[i]:
                diff = daily_reqs[i] - planwide_avg[i]
                print("You miss your goal for " + nutrients[i][2] + " by an average of: \n" + str(diff) + " " + nutrients[i][3] + " per day.")
            elif planwide_avg[i] > daily_reqs[i]:
                surplus = planwide_avg[i] - daily_reqs[i]
                print("You exceed your goal for " + nutrients[i][2] + " by an average of: \n" + str(surplus) + " " + nutrients[i][3] + " per day.")


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





