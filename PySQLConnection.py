
import pymysql
from data_validation import input_form
# --------------------------------------------------SEARCH BY NAME FUNCTIONS-------------------------------------------------


# Searches for ingredient by name or through specific (inp)food-id
# returns [food_id, food_name, cost_per_100]
def search_food_item(cursor, food_id):
    x = []
    if (food_id is None):
        x = search(cursor, "Enter a food item", "food_id, food_name, cost_per_100g", "food_item", "food_id")
    else:
        cursor.execute("select food_id, food_name, cost_per_100g from food_item where food_id = " + food_id)
        for i in cursor:
            x = i
    return x;


# Searches for recipe by name or through specific recipe-id
def search_recipe(cursor, recipe_id):
    x = []
    output_fields = "recipe_id, recipe_name"
    table = "recipe"
    if (recipe_id is None):
        x = search(cursor, "Enter a recipe", output_fields, table, "recipe_name", "recipe_id")
    else:
        cursor.execute("select " + output_fields + " from " + table + " where recipe_id = " + str(recipe_id))
        for i in cursor:
            x = i
    return x


# Searches for recipe by name or through specific recipe-id
def search_plan(cursor, plan_id):
    output_fields = "plan_id, plan_name"
    table = "plan"
    if (plan_id is None):
        x = search(cursor, "Enter a plan", output_fields, table, "plan_name", "plan_id")
        return(x)
    else:
        cursor.execute("select " + output_fields + " from " + table + " where plan_id = " + (plan_id))
        for i in cursor:
            return i
# -----------------------------------------------------NUTRIENT FUNCTIONS-----------------------------------------------
#--------------------------------------------------------------INGREDIENT FUNCTIONS--------------------------------------------------
def add_ingredient(cursor, recipe_id, food_id):
    if food_id is None:
        food_item = search_food_item(cursor, None)
        food_id = food_item[0]
    amount = input("How many grams(whole numbers only) of this item would you like to add?")
    query = ("insert into ingredient (food_id, recipe_id, amount_in_grams) values ("
             + "'" + str(food_id) + "',"
             + str(recipe_id) + ","
             + str(amount) + ")")
    cursor.execute(query)

def remove_ingredient(cursor, recipe_id):
    food_item = search_food_item(cursor, None)
    food_id = food_item[0]

def part_of_recipe(cursor, food_id, recipe_id):
    query = "select * from ingredient where food_id = " + str(food_id) + " and recipe_id = " + str(recipe_id)
    cursor.execute(query)
    if ((len(cursor)) == 0):
        return False
    else:
        return True
def alter_ingredient(cursor, recipe_id):
    food = search_food_item(cursor, None)
    food_id = food[0]
    if (part_of_recipe(cursor, food_id, recipe_id)):
        new_amt = input('What would you like to change the amount to (in grams)?')
        query = "update ingredient set amount_in_grams =  " + str(new_amt) + "where food_id = " + str(food_id) + "and recipe_id = " + str(recipe_id)
        cursor.execute(query)
    else:
        ans = input("Would you like to add this ingredient? [Y/N]")
        if (ans == "Y"):
            add_ingredient(cursor, recipe_id, food_id)

# ---------------------------------------------------------------RECIPE FUNCTIONS--------------------------------------------------------
def get_recipe_ingredients(cursor, recipe_id):
    ingredients = []
    cursor.execute("select food_id, amount_in_grams from ingredient where recipe_id = " + str(recipe_id))
    for i in cursor:
        ingredients.append(i)
    return ingredients

def nutritional_total_recipe(cursor, recipe_id):
    nutr_reqs = get_nutrients_to_track(cursor)
    food_items_in_recipe = get_recipe_ingredients(cursor, recipe_id)
    nutr_totals = []
    for nutrient in nutr_reqs:
        total = 0
        for food_info in food_items_in_recipe:
            amount = (get_nutrient_amount(cursor, food_info[0], nutrient[0]))
            total = total + amount
        # [nutrient id, nutrient name, total in recipe, units]
        nutr_totals.append([nutrient[0], nutrient[1], total, nutrient[3]])
    return nutr_totals

def add_recipe(cursor):
    name = input("What is the name of this recipe?")
    if not (input_form(name) == 0):
        print("That's not a valid recipe name. Try again.")
        add_recipe(cursor)
    else:
        cursor.execute('insert into recipe (recipe_name) values ( "' + name + ' ")')
        recipe_id = None
        # find recipe_id of new recipe
        cursor.execute("select recipe_id from recipe where (recipe_name = '" + name + "')")
        for i in cursor:
            recipe_id = i[0]
        while (input("Would you like to add an ingredient [Y/N]") == "Y"):
            add_ingredient(cursor, recipe_id, None)

def view_recipe(cursor, recipe_id):
    recipe = search_recipe(cursor, recipe_id)
    recipe_id = recipe[0]
    ingredients = get_recipe_ingredients(cursor, recipe_id)
    name = recipe[1]
    print(name)
    for i in ingredients:
        food_item = search_food_item(cursor, i[0])
        food_name = food_item[1]
        amount_in_grams = i[1]
        print("\t " + food_name + ": \n \t \t" + str(amount_in_grams) + " grams")

    print("Nutritional Info:")
    nutr_totals = nutritional_total_recipe(cursor, recipe_id)
    for i in nutr_totals:
        print(i[1] + ": " + str(i[2]) + " " + i[3])

def view_recipe_list(cursor):
    print("RECIPE INDEX")
    query = "select recipe_name from recipe"
    cursor.execute(query)
    recipes = []
    for r in cursor:
        print(r[0])
        recipes.append(r)
    if (len(recipes) == 0):
        return False
    else:
        return True
def rename_recipe(cursor, recipe_id):
    new_name = input("Enter a new name for the recipe:")
    if not(input_form(new_name) == 0):
        print("That's not a valid recipe name. Try again.")
        rename_recipe(cursor, recipe_id)
    else:
        query = "update recipe set recipe_name = " + "'" + new_name + "'" + "where recipe_id = " + str(recipe_id)
        cursor.execute(query)


def delete_recipe(cursor, recipe_id):
    query = "delete from recipe where recipe_id = " + str(recipe_id)
    cursor.execute(query)


#---------------------------------------------------------------PLAN FUNCTIONS--------------------------------------------------------
def get_name(str):
    name = input(str)
    while not(input_form(name) == 0):
        print("That's not a valid name. Try again.")
        return get_name(str)
    return name
def get_days(str):
    days = input(str)
    while not(input_form(name) == 1):
        print("That's not a valid number. Try again.")
        return get_days(str)
    return days
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
def add_meal(cursor, plan_id, recipe_id):
    if recipe_id is None:
        recipe_item = search_recipe(cursor, None)
        print(recipe_item)
        recipe_id = recipe_item[0]
    amount = input("How many servings of this item would you like to add?")
    if(input_form(amount)==1):
        query = ("insert into meal (recipe_id, plan_id, num_servings) values ("
                 + str(recipe_id) + ","
                + str(plan_id) + ","
                + str(amount) + ")")
        cursor.execute(query)
    else:
        print("Please enter a numeric input:")
        add_meal(cursor, plan_id, recipe_id)

def change_plan_days(cursor, plan_id):
    days = get_days("What number of days should his plan cover?")
    query = "update plan set num_days = " + str(days) + "where plan_id = " + str(plan_id)

def remove_meal(cursor, plan_id, recipe_id):
    if recipe_id is None:
        recipe_item = search_recipe(cursor, None)
        recipe_id = recipe_item[0]
    query = ("delete from meal where recipe_id =" + str(recipe_id) + " and plan_id = " + str(plan_id))
    cursor.execute(query)
def rename_plan(cursor, plan_id):
    new_name = input("Enter a new name for the recipe:")
    if not(input_form(new_name) == 0):
        print("That's not a valid plan name. Try again.")
        rename_plan(cursor, plan_id)
    else:
        query = "update recipe set plan_name = " + "'" + new_name + "'" + "where plan_id = " + str(plan_id)
        cursor.execute(query)

def part_of_plan(cursor,recipe_id, plan_id):
    query = "select * from meal where recipe_id = " + str(recipe_id) + " and plan_id = " + str(plan_id)
    cursor.execute(query)
    if ((len(cursor)) == 0):
        return False
    else:
        return True
def alter_meal(cursor, plan_id):
    recipe = search_recipe(cursor, None)
    recipe_id = recipe[0]
    if (part_of_plan(cursor, recipe_id, plan_id)):
        new_amt = input('What would you like to change the number of servings to?')
        query = "update meal set num_servings =  " + str(new_amt) + "where recipe_id = " + str(recipe_id) + "and plan_id = " + str(plan_id)
        cursor.execute(query)
    else:
        ans = input("Would you like to add this recipe to the plan? [Y/N]")
        if (ans == "Y"):
            add_meal(cursor, plan_id, recipe_id)


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

def print_meal(cursor, meal):
    cursor.execute("select recipe_name from recipe where recipe_id = " + str(meal[1]))
    recipe_name = ""
    for i in cursor:
        recipe_name = i[0]

    print(str(meal[2]) + " servings of " + recipe_name)

def get_meals_in_plan(cursor, plan_id):
    meals = []
    query = "select * from meal where plan_id = " + str(plan_id)
    cursor.execute(query)
    for i in cursor:
        meals.append(i)
    if (len(meals) == 0):
        print("There aren't any meals in this plan.")
        return None
    return meals
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





