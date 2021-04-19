from search import search_food_item, search_ingredient, search_recipe, search_nutrient, search_nutrient_data,q_get_tuple, q_get_list_of_tuples, search_meal
from recipe import nutritional_total_recipe
from meal import recipe_id_meal
from data_validation import qform_varchar, qform_num
from plan import plan_name_plan, fulfills_nutritional_requs
from nutrient import get_nutrients_to_track

# pretty-prints single nutrient
# [nutrient_id, nutrient_name, units] -> None
def print_nutrient(n):
    print("[ID " + str(n[0]) + "] : " + n[1] + " measured in " + n[2])

#pretty prints single nutritional data
#[nutrient id, amt, food_id] -> None
def print_nutrient_food_data(cursor, data):
    nutrient = search_nutrient(cursor, data[0])
    name = nutrient[1]
    print("[ID " + str(data[0]) + "]" + name + " : " + str(data[1]) + " " + data[2])

# pretty-prints single nutrient requirements
# [nutrient_id, nutrient name, daily requirement, units] -> None
def print_nutrient_requ(n):
    print("[ID " + str(n[0]) + "] : " + n[1] + " has a daily requirement of " + str(n[2]) + " " + n[3])

#prints all the tracked nutritional data for a food item
# food_item -> None
def print_tracked_nutr_food(cursor, food_id):
    # get_nutrients_to_track(cursor) -> [nutrient_id, nutrient name, daily requirement, units]
    tracked_nutrients = get_nutrients_to_track(cursor)
    # search_food_item(cursor, food_id / None) -> [food_id, food_name, cost_per_100]
    food = search_food_item(cursor, food_id)
    food_name = food[1]
    print("Per 100 grams, " + food_name + " has:")
    for n in tracked_nutrients:
        data = search_nutrient_data(cursor, food_id, n[0])
        print_nutrient_food_data(cursor, data)

#pretty prints the ingredient
#cursor, recipe_id, food_id -> None
def print_ingredient(cursor, ingredient):
    food_id = ingredient[0]
    food_item = search_food_item(cursor, food_id)
    food_name = food_item[1]
    amount_in_grams = ingredient[1]
    print("\t " + food_name + ": \n \t \t" + str(amount_in_grams) + " grams")


#pretty prints recipe
#print_recipe(cursor, recipe_id) -> None
def print_recipe(cursor, recipe_id):
    recipe = search_recipe(cursor, recipe_id)
    recipe_id = recipe[0]
    name = recipe[1]
    ingredients = search_ingredient(cursor, None, recipe_id)
    print(name)
    for i in ingredients:
        print_ingredient(cursor, i)
    print("Nutritional Info:")
    nutr_totals = nutritional_total_recipe(cursor, recipe_id)
    for i in nutr_totals:
        print(i[1] + ": " + str(i[2]) + " " + i[3])


#prints recipe list and returns if there are any recipes
# cursor -> boolean
def print_recipe_list(cursor):
    print("RECIPE INDEX")
    query = "select recipe_name from recipe"
    recipes = q_get_list_of_tuples(cursor, query)
    if (recipes is None):
        return False
    else:
        for r in recipes:
            print_recipe(cursor, r)
        return True


# prints meals prettily
# print_meal(cursor, meal) -> None
def print_meal(cursor, meal):
    recipe_id = recipe_id_meal(meal)
    query = "select recipe_name from recipe where recipe_id = " + qform_num(recipe_id)
    recipe_name = q_get_tuple(cursor, query)
    print(str(meal[2]) + " servings of " + recipe_name)



def print_plan(cursor, plan_id):
    meals = search_meal(cursor, None, plan_id)
    if meals is not None:
        print("This plan has: \n")
        for m in meals:
            print_meal(cursor, m)
        fulfills_nutritional_reqs(cursor, plan_id)
    else:
        print("This plan has no meals yet!")

def print_plan_list(cursor):
    print("PLAN LIST")
    query = "select * from plan"
    plans = q_get_list_of_tuples(cursor, query)
    if (plans is None):
        return False
    else:
        for p in plans:
            print(plan_name_plan(p))
        return True

def print_menu(options):
    print(30 * "-" + "MENU" + 30 * "-" + "")
    i = 1
    for opt in options:
        opt_stmt = str(i) + ":" + opt + ""
        print(opt_stmt)
        i = i + 1
    print(67 * "-" + "")
    print("**Type 0 to end program.")