

import pymysql

def search(cursor, dialogue, allCols, table, onCol):
    x = input(dialogue + "\n")
    query = "select " + allCols + " from " + table + " where " + onCol + " like '" + x + "%'"
    while not (cursor.execute(query) == 1):
        print("Not an exact match. Did you mean one of these?")
        for i in cursor:
            print(i)
        x = input(dialogue + "\n")
        query = "select " + allCols + " from " + table + " where " + onCol + " like '" + x + "%'"
    for i in cursor:
        return i

#Searches for ingredient by name or through specific food-id
def search_ingredient(cursor, food_id):
    x = []
    if (food_id == None)
        x = search(cursor, "Enter a food item", "food_id, food_name, cost_per_100g", "food_item", "food_name")
    else:
        cursor.execute("select food_id, food_name, cost_per_100g from food_item where food_id = " + food_id)
        for i in cursor:
            x = i
    return x;
#Searches for recipe by name or through specific recipe-id
def search_recipe(cursor, recipe_id):
    x = []
    output_fields = "recipe_id, recipe_name"
    table = "recipe"
    if (recipe_id == None)
        x = search(cursor, "Enter a recipe", output_fields, table, "recipe_name")
    else:
        cursor.execute("select " + output_fields + " from " + table + " where recipe_id = " + recipe_id)
        for i in cursor:
            x = i
    return x
#Searches for recipe by name or through specific recipe-id
def search_plan(cursor, plan_id):
    x = []
    output_fields = "plan_id, plan_name"
    table = "plan"
    if (plan_id == None)
        x = search(cursor, "Enter a plan", output_fields, table, "plan_name")
    else:
        cursor.execute("select " + output_fields + " from " + table + " where plan_id = " + recipe_id)
        for i in cursor:
            x = i
    return x;
# get nutrional data for food item
def get_nutrient_data(cursor, food_id, nutrient_id):
    cursor.execute("select nutrient_id, amt, food_id from nutrient_data where food_id = )" + food_id + " and nutrient_id = " + nutrient_id )
    x = []
    for i in cursor:
        x.append(i)
    return x

def get_recipe_ingredients(cursor, recipe_id)
    ingredients = []
    cursor.execute("select food_id, amount_in_grams, recipe_id from ingredient where recipe_id = " + recipe_id)
    for i in cursor:
        ingredients.append(i)
    return ingredients

def nutritional_total_recipe(cursor, recipe_id)
    nutr_reqs = get_nutrients_to_track(cursor)
    nutr_totals = []
    for nutrient in nutr_reqs:
        nutr_totals.append(get_nutrient_data(cursor, ))


#Searches for ingredient by name or by specific nid, returns nutritional data
def search_nutrient(cursor, nid):
    x = []
    if (nid == None):
        x = search(cursor, "Enter a nutrient", "nutrient_id, nutrient_name, units", "nutrient", "nutrient_name")
    else:
        cursor.execute("select nutrient_id, nutrient_name, units from nutrient where nutrient_id = " + nid)
        for i in cursor:
            x = i
    return x;

def get_nutrients_to_track(cursor):
    nutr_to_track = []
    cursor.execute('select n.nutrient_id, n.nutrient_name, d.requ, n.units from daily_nut_requ as d natural join nutrient as n')
    for i in cursor:
        nutr_to_track.append(i)
    return nutr_to_track

def is_part_of_nutrients_to_track(cursor, nutrient):
    nttList = get_nutrients_to_track(cursor)
    return (nutrient[0] in (i[0] for i in nttList))

def update_nutrients_to_track(cursor, nid):
    x = search_nutrient(cursor, nid)
    is_part = is_part_of_nutrients_to_track(cursor, x)
    #Nutrient is indeed part of list; can update
    if (is_part):
        r = input("How many " + x[2] + " would you like to consume daily, on average?")
        query = "update daily_nut_requ set requ = 13.5 where nutrient_id = '" + r + "'"
        cursor.execute(query)
        #Nutrient is not part of list; must add


def add_nutrients_to_track(cursor, nid):
    x = search_nutrient(cursor, nid)
    is_part = is_part_of_nutrients_to_track(cursor, x)
    if (is_part):
        print("That nutrient is already part of the daily requirements.\n")
        print(x)
        choice = input("Would you like to update it? [Y/N] \n")
        if (choice == 'Y'):
            update_nutrients_to_track(cursor, x[0])
    else:
        r = input("How many " + x[2] + " would you like to consume daily, on average?")
        cursor.execute("insert into daily_nut_requ (nutrient_id, requ) values (" + str(x[0]) + "," + str(r) + ")")
def remove_nutrients_to_track(cursor):
    nutr_to_track = get_nutrients_to_track(cursor)
    print(nutr_to_track)
    x = search_nutrient(cursor, None)
    is_part = is_part_of_nutrients_to_track(cursor, x)
    if (is_part):
        cursor.execute("delete from daily_nut_requ where nutrient_id = " + str(x[0]) + "")
    else:
        print("Nutrient is already not part of tracked requirements. \n")
#---------------------------------------------------------------------------------------------------------------------------------------
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
        for i in range(1, len(opt)+1):
            if x == str(i):
                return i
        if x == str(0):
            print("Goodbye! \n")
            loop = False  # This will make the while loop to end as not value of loop is set to False
        else:
            # Any integer inputs other than values 1-5 we print an error message
            print("Invalid option selection. \n")

def nutrient_menu(cursor):
    options = ['View Nutrient Requirements',
              'Add Nutrient Requirement to Track',
              'Update Nutrient Requirement',
              'Remove Nutrient Requirement Tracked',
              'Return to Main Menu']
    choice = make_menu(options)
    if (choice == 1):
        nutr_to_track = get_nutrients_to_track(cursor)
        print(nutr_to_track)
        nutrient_menu(cursor)
    elif (choice == 2):
        add_nutrients_to_track(cursor, None)
        nutrient_menu(cursor)
    elif (choice == 3):
        update_nutrients_to_track(cursor, None)
        nutrient_menu(cursor)
    elif (choice == 4):
        remove_nutrients_to_track(cursor)
        nutrient_menu(cursor)
    elif (choice == 5):
        main_menu(cursor)
def main_menu(cursor):
    options = ['View/Edit Tracked Nutrients',
               'View/Edit Ingredients',
               'View/Edit Recipes',
               'View/Edit Plans']
    choice = make_menu(options)
    if (choice == 1):
        nutrient_menu(cursor)
    elif (choice == 2):
        print("Ingr")
        ## You can add your code or functions here
    elif (choice == 3):
        print("Recipes")
        ## You can add your code or functions here
    elif (choice == 4):
        print("Plans")
#------------------------------------------------------------------------------------------------------------------------------------------i
print('Hi!')
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='0926',
                             db='meal_plan',
                             charset='utf8mb4')


cursor = connection.cursor()
nutrient_menu(cursor)
connection.commit()
print("Closing connection to database...\n")
cursor.close()
connection.close()
print("Goodbye!\n")




