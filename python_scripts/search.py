import pymysql
from data_validation import qform_varchar, qform_num, cp_form
from data_validation import input_form


def q_get_tuple(cursor, query):
    cursor.execute(query)
    for i in cursor:
        return check_exists(i)
def q_get_list_of_tuples(cursor, query):
    list = []
    cursor.execute(query)
    for i in cursor:
        list.append(i)
    return check_exists(list)

def q_get_value(cursor, query, index):
    x = q_get_tuple(cursor, query)
    if (x is None):
        return None
    else:
        return x[index]

#cursor, "proc", (arg1, arg2, arg3,...) -> [a,b,c...]
def cp_get_tuple(cursor, proc, args):
    cursor.callproc(proc, args)
    for i in cursor:
        return check_exists(i)
# cursor, "proc", (arg1, arg2, arg3,...) -> [[a,b,c],[d,e,f]]
def cp_get_list_of_tuples(cursor, proc, args):
    list = []
    cursor.callproc(proc, args)
    for i in cursor:
        list.append(i)
    return check_exists(list)

def cp_get_value(cursor, proc, args, index):
    x = cp_get_tuple(cursor, proc, args)
    if (x is None):
        return None
    else:
        return x[index]

# Searches for ingredient by name or by specific nid (if not, None), returns nutritional info
# cursor, nutrient_id/None -> [nutrient_id, nutrient_name, units]
def search_nutrient(cursor, nid):
    from print_methods import print_nutrient
    x = []
    if (nid == None):
        x = search(cursor, "Enter a nutrient", "nutrient_id, nutrient_name, units", "nutrient", "nutrient_name", "nutrient_id")
    else:
        x = cp_get_tuple(cursor, 'search_nutrient', (nid,))
    return x

# Searches for ingredient by name or through specific food-id
# search_food_item(cursor, food_id/None) -> [food_id, food_name]
def search_food_item(cursor, food_id):
    x = []
    output_fields = "food_id, food_name"
    table = "food_item"
    if (food_id is None):
        x = search(cursor, "Enter a food item", output_fields, table, "food_name", "food_id")
    else:
        x = cp_get_tuple(cursor, 'search_food_item', (food_id,))
    return x


# Searches for recipe by name or through specific recipe_id
# cursor, recipe_id/None -> [recipe_id, recipe_name]
def search_recipe(cursor, recipe_id):
    from print_methods import print_recipe
    x = []
    output_fields = "recipe_id, recipe_name"
    table = "recipe"
    if (recipe_id is None):
        x = search(cursor, "Enter a recipe", output_fields, table, "recipe_name", "recipe_id")
    else:
        x = cp_get_tuple(cursor, 'search_recipe', (recipe_id,))
    return x


# Searches for plan by name or through specific plan_id
# cursor, plan_id/None -> [plan_id, plan_name, num_days]
def search_plan(cursor, plan_id):
    output_fields = "plan_id, plan_name, num_days"
    table = "plan"
    if (plan_id is None):
        x = search(cursor, "Enter a plan", output_fields, table, "plan_name", "plan_id")
    else:
        x = cp_get_tuple(cursor, 'search_plan', (plan_id,))
    return x

# Searches for ingredients by recipe_id and optionally food_id
# search_ingredient(cursor, food_id/None, recipe_id/None) -> [food_id, recipe_id, amount_in_grams]
def search_ingredient(cursor, food_id, recipe_id):
    fid = cp_form(food_id)
    rid = cp_form(recipe_id)
    proc = 'search_ingredient'
    args = (fid, rid)
    if food_id is not None and recipe_id is not None:
        return cp_get_tuple(cursor, proc, args)
    else:
        return cp_get_list_of_tuples(cursor, proc, args)

# Searches for nutrient data by food_id and optionally nutrient_id
# cursor, food_id/None, nutrient_id/None -> [nutrient id, amt, food_id]
def search_nutrient_data(cursor, food_id, nutrient_id):
    fid = cp_form(food_id)
    nid = cp_form(nutrient_id)
    proc = 'search_nutrient_data'
    args = (fid, nid)
    if food_id is not None and nutrient_id is not None:
        return cp_get_tuple(cursor, proc, args)
    else:
        return cp_get_list_of_tuples(cursor, proc, args)

# Returns none if there are no meals
#cursor, recipe_id/None, plan_id/None -> [recipe_id, plan_id, num_servings]/None
def search_meal(cursor, recipe_id, plan_id):
    rid = cp_form(recipe_id)
    pid = cp_form(plan_id)
    proc = 'search_meal'
    args = (pid, rid)
    if recipe_id is not None and plan_id is not None:
        return cp_get_tuple(cursor, proc, args)
    else:
        return cp_get_list_of_tuples(cursor, proc, args)

#Searches for a unique result using user input. performs data validation to avoid SQL errors
#cursor, instructions to user, all cols to retrieve, table, name_column, id column -> all cols to retrieve
def search(cursor, dialogue, allCols, table, name_Col, id_Col):
    x = input(dialogue + "\n")
    form = input_form(x)
    if (form == -2):
        print("You did not not type anything")
        return search(cursor, dialogue, allCols, table, name_Col, id_Col)
    elif (form == -1):
        print("Invalid input")
        return search(cursor, dialogue, allCols, table, name_Col, id_Col)
    elif(form == 0):
        query = "select " + allCols + " from " + table + " where " + name_Col + " like '%" + x + "%'"
        if (cursor.execute(query) == 1):
            for i in cursor:
                return i
        else:
            print("Not an exact match. Any similar matches are printed below:")
            for i in cursor:
                print(i)
            return search(cursor, dialogue, allCols, table, name_Col, id_Col)
    elif(form == 1):
        query = "select " + allCols + " from " + table + " where " + id_Col + " = " + x + ""
        if (cursor.execute(query) == 1):
            for i in cursor:
                return i
        else:
            print("Invalid ID. Try again.")
            return search(cursor, dialogue, allCols, table, name_Col, id_Col)
    else:
        return search(cursor, dialogue, allCols, table, name_Col, id_Col)


#returns list if empty, returns None if not empty
def check_exists(list):
    if (len(list) == 0):
        return None
    else:
        return list

