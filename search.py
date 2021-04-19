import pymysql
from data_validation import qform_varchar, qform_num
from data_validation import input_form


def q_get_tuple(cursor, query):
    cursor.execute(query)
    for i in cursor:
        return i
def q_get_list_of_tuples(cursor, query):
    list = []
    for i in cursor:
        list.append(i)
    return list

# Searches for ingredient by name or by specific nid (if not, None), returns nutritional info
# cursor, nutrient_id/None -> [nutrient_id, nutrient_name, units]
def search_nutrient(cursor, nid):
    x = []
    if (nid == None):
        x = search(cursor, "Enter a nutrient", "nutrient_id, nutrient_name, units", "nutrient", "nutrient_name", "nutrient_id")
    else:
        query = "select nutrient_id, nutrient_name, units from nutrient where nutrient_id = " + qform_varchar(nid)
        x = q_get_tuple(cursor, query)
    return x

# Searches for ingredient by name or through specific food-id
# cursor, food_id/None -> [food_id, food_name, cost_per_100]
def search_food_item(cursor, food_id):
    x = []
    if (food_id is None):
        x = search(cursor, "Enter a food item", "food_id, food_name, cost_per_100g", "food_item", "food_id")
    else:
        query = "select food_id, food_name, cost_per_100g from food_item where food_id = " + qform_varchar(food_id)
        x = q_get_tuple(cursor, query)
    return x


# Searches for recipe by name or through specific recipe_id
# cursor, recipe_id/None -> [recipe_id, recipe_name]
def search_recipe(cursor, recipe_id):
    x = []
    output_fields = "recipe_id, recipe_name"
    table = "recipe"
    if (recipe_id is None):
        x = search(cursor, "Enter a recipe", output_fields, table, "recipe_name", "recipe_id")
    else:
        query = "select " + output_fields + " from " + table + " where recipe_id = " + qform_num(recipe_id)
        x = q_get_tuple(cursor, query)
    return x


# Searches for plan by name or through specific plan_id
# cursor, plan_id/None -> [plan_id, plan_name]
def search_plan(cursor, plan_id):
    output_fields = "plan_id, plan_name"
    table = "plan"
    if (plan_id is None):
        x = search(cursor, "Enter a plan", output_fields, table, "plan_name", "plan_id")
        return x
    else:
        query = "select " + output_fields + " from " + table + " where plan_id = " + qform_num(plan_id)
        return q_get_tuple(cursor, query)

# Searches for ingredients by recipe_id and optionally food_id
# search_ingredient(cursor, food_id/None, recipe_id/None) -> [food_id, recipe_id, amount_in_grams]
def search_ingredient(cursor, food_id, recipe_id):
    query = ""
    if food_id is None and recipe_id is not None:
        query = "select food_id, recipe_id, amount_in_grams from ingredient where recipe_id = " + qform_num(recipe_id)
        return q_get_list_of_tuples(cursor, query)
    elif food_id is not None and recipe_id is None:
        query = "select food_id, recipe_id, amount_in_grams from ingredient where food_id = " + qform_num(food_id)
        return q_get_list_of_tuples(cursor, query)
    elif food_id is not None and recipe_id is not None:
        query = "select food_id, recipe_id, amount_in_grams from ingredient where food_id = " + qform_varchar(food_id) + " and recipe_id = " + qform_num(recipe_id)
        return q_get_tuple(cursor, query)


# Searches for nutrient data by food_id and optionally nutrient_id
# cursor, food_id/None, nutrient_id/None -> [nutrient id, amt, food_id]
def search_nutrient_data(cursor, food_id, nutrient_id):
    if food_id is not None and nutrient_id is None:
        query = "select nutrient_id, amt, food_id from nutrient_data where food_id = " + qform_varchar(food_id)
        return q_get_list_of_tuples(cursor, query)
    elif food_id is None and nutrient_id is not None:
        query = "select nutrient_id, amt, food_id from nutrient_data where nutrient_id = " + qform_varchar(nutrient_id)
        return q_get_list_of_tuples(cursor, query)
    elif food_id is not None and nutrient_id is not None:
        query = "select nutrient_id, amt, food_id from nutrient_data where food_id = " + qform_varchar(food_id) + " and nutrient_id = " + qform_varchar(nutrient_id) + ""
        return q_get_tuple(cursor, query)

#cursor, recipe_id/None, plan_id/None -> [recipe_id, plan_id, num_servings]
def search_meal(cursor, recipe_id, plan_id):
    output_fields = "recipe_id, plan_id, num_servings"
    table = "meal"
    if recipe_id is not None and plan_id is None:
        query = "select " + output_fields + " from " + table + " where recipe_id = " + qform_varchar(recipe_id)
        return q_get_list_of_tuples(cursor, query)
    elif recipe_id is None and plan_id is not None:
        query = query = "select " + output_fields + " from " + table + " where plan_id = " + qform_varchar(plan_id)
        return q_get_list_of_tuples(cursor, query)
    elif recipe_id  is not None and plan_id is not None:
        query = query = "select " + output_fields + " from " + table + " where recipe_id = " + qform_varchar(recipe_id) + " and plan_id = " + qform_varchar(plan_id) + ""
        return q_get_tuple(cursor, query)

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
        query = "select " + allCols + " from " + table + " where " + name_Col + " like '" + x + "%'"
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


