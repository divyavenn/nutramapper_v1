
from search import *
from data_validation import qform_num
import os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" * 100)

# pretty-prints single nutrient
# [nutrient_id, nutrient_name, units] -> None
def print_nutrient(n):
    print("[ID " + str(n[0]) + "] : " + n[1] + " measured in " + n[2])

#pretty prints single nutritional data
#[nutrient id, amt, food_id] -> None
def print_nutrient_food_data(cursor, data):
    if data is not None:
        nutrient = search_nutrient(cursor, data[0])
        if nutrient is not None:
            name = nutrient[1]
            print("[ID " + str(data[0]) + "]" + name + " : " + str(data[1]))

# pretty-prints single nutrient requirements
# [nutrient_id, nutrient name, daily requirement, units] -> None
def print_nutrient_requ(n):
    print("[ID " + str(n[0]) + "] : " + n[1] + " has a daily requirement of " + str(n[2]) + " " + n[3])



#pretty prints the ingredient
#cursor, [food_id, recipe_id, amount_in_grams]-> None
def print_ingredient(cursor, ingredient):
    food_id = ingredient[0]
    food_item = search_food_item(cursor, food_id)
    if food_item is not None:
        food_name = food_item[1]
        amount_in_grams = ingredient[2]
        print("\t " + food_name + ": \n \t \t" + str(amount_in_grams) + " grams")


#prints all the tracked nutritional data for a food item
# print_tracked_nutr_food(cursor, food, tracked_nutrients) -> None
def print_tracked_nutr_food(cursor, food, tracked_nutrients):
    food_id = food[0]
    food_name = food[1]
    print("Per 100 grams, " + food_name + " has:")
    for n in tracked_nutrients:
        data = search_nutrient_data(cursor, food_id, n[0])
        if data is not None:
            print_nutrient_food_data(cursor, data)

#pretty prints recipe
#print_recipe(cursor, recipe_id) -> None
def print_recipe(cursor, recipe):
    from recipe import nutritional_total_recipe
    recipe_id = recipe[0]
    name = recipe[1]
    ingredients = search_ingredient(cursor, None, recipe_id)
    print(name)
    print("-" * 64)
    if ingredients is not None:
        for i in ingredients:
            print_ingredient(cursor, i)
        nutr_totals = nutritional_total_recipe(cursor, recipe_id)
        for i in nutr_totals:
            print(i[1] + ": " + str(i[2]) + " " + i[3])
    else:
        print("**This recipe has no ingredients**")
    print("-"*64)


#prints recipe list and returns if there are any recipes
# cursor -> boolean
def print_recipe_list(cursor):
    cls()
    print("RECIPE INDEX")
    print("-" * 64)
    query = "select recipe_name from recipe"
    recipes = q_get_list_of_tuples(cursor, query)
    if (recipes is None):
        print("You have no recipes yet.")
        return False
    else:
        for r in recipes:
            print("\t " + str(r[0]))
        print("-" * 64)
        print("\n \n")
        return True


# prints meals prettily
# print_meal(cursor, meal) -> None
def print_meal(cursor, meal):
    from meal import recipe_id_meal
    recipe_id = recipe_id_meal(meal)
    query = "select recipe_name from recipe where recipe_id = " + qform_num(recipe_id)
    recipe_name = q_get_value(cursor, query, 0)
    print(str(meal[2]) + " servings of " + recipe_name)



def print_plan(cursor, plan):
    from plan import fulfills_nutritional_requs
    plan_id = plan[0]
    # cursor, plan_id/None -> [plan_id, plan_name, num_days]
    meals = search_meal(cursor, None, plan_id)
    if meals is not None:
        print("Plan " + str(plan[1]) + " covers " + str(plan[2]) + " days and has: \n")
        print("-" * 64)
        for m in meals:
            print_meal(cursor, m)
        print("-"*64)
        fulfills_nutritional_requs(cursor, plan_id)
    else:
        print("This plan has no meals yet!")

def print_plan_list(cursor):
    cls()
    from plan import plan_name_plan
    print("PLAN LIST")
    print("-" * 64)
    query = "select * from plan"
    plans = q_get_list_of_tuples(cursor, query)
    if (plans is None):
        return False
    else:
        for p in plans:
            print("\t " + plan_name_plan(p))
        print("-"*64)
        print("\n \n")
        return True

def print_menu(options):
    print(30 * "-" + "MENU" + 30 * "-" + "")
    i = 1
    for opt in options:
        opt_stmt = str(i) + ":" + opt + ""
        print(opt_stmt)
        i = i + 1
    print(64 * "-" + "")
    print("**Type 0 to end program and commit all changes.")
    print("\n \n \n")