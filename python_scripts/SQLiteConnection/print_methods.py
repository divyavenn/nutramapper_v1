
from search import *
from data_validation import qform_num, cp_form
import os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" * 100)

# pretty-prints single nutrient
# [nutrient_id, nutrient_name, units] -> None
def print_nutrient(n):
    print("[ID " + str(n[0]) + "] : " + n[1] + " measured in " + n[2])

#pretty prints single nutritional data
#[nutrient id, food_id, amt] -> None
def print_nutrient_food_data(cursor, data):
    if data is not None:
        nutrient = search_nutrient(cursor, data[0])
        if nutrient is not None:
            name = nutrient[1]
            units = nutrient[2]
            print("[ID " + str(data[0]) + "]" + name + " : " + str(data[2]) + " " + units)

# pretty-prints single nutrient requirements
# [nutrient_id, nutrient name, daily requirement, units] -> None
def print_nutrient_requ(n):
    print("[ID " + str(n[0]) + "] : " + n[1] + " has a daily requirement of " + str(n[2]) + " " + n[3])

# pretty-prints single nutrient requirements
# cursor -> none
def print_nutrient_requ_list(cursor):
    from nutrient import get_nutrients_to_track
    cls()
    nutr_to_track = get_nutrients_to_track(cursor)
    if (nutr_to_track is not None):
        print("NUTRIENTS TRACKED")
        print("-"*64)
        for n in nutr_to_track:
            print_nutrient_requ(n)
    else:
        print("-" * 64)
        print("**No nutrients are currently being tracked.**")
    print("-" * 64)




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
    cls()
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
    from recipe import nutritional_total_recipe, total_grams
    recipe_id = recipe[0]
    name = recipe[1]
    ingredients = search_ingredient(cursor, None, recipe_id)
    print(name)
    print("-" * 64)
    if ingredients is not None:
        for i in ingredients:
            print_ingredient(cursor, i)
        # nutritional_total_recipe(cursor, recipe_id) -> [nutrient_id, nutrient_name, total_in_recipe, units]
        nutr_totals = nutritional_total_recipe(cursor, recipe_id)
        print("-" * 64)
        for i in nutr_totals:
            print(i[1] + ": " + str(round(i[2],2)) + " " + i[3])
        grams = total_grams(cursor, recipe_id)
        print("This recipe makes 100")
    else:
        print("**This recipe has no ingredients**")
    print("-"*64)


#prints recipe list and returns if there are any recipes
# cursor -> boolean
def print_recipe_list(cursor):
    cls()
    print("RECIPE INDEX")
    print("-" * 64)
    recipes = cp_get_list_of_tuples(cursor, 'search_recipe', (cp_form(None),))
    if (recipes is None):
        print("You have no recipes yet.")
        return False
    else:
        for r in recipes:
            print("\t " + str(r[1]))
        print("-" * 64)
        print("\n \n")
        return True


# prints meals prettily
# print_meal(cursor, meal) -> None
def print_meal(cursor, meal):
    from meal import recipe_id_meal
    from search import search_recipe
    recipe_id = recipe_id_meal(meal)
    recipe = search_recipe(cursor, recipe_id)
    print(str(meal[2]) + " servings of " + recipe[1])



def print_plan(cursor, plan):
    from plan import fulfills_nutritional_requs
    plan_id = plan[0]
    # cursor, plan_id/None -> [plan_id, plan_name, num_days]
    meals = search_meal(cursor, None, plan_id)
    if meals is not None:
        print("Plan " + plan[1] + " covers " + str(plan[2]) + " days and has: \n")
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
    plans = cp_get_list_of_tuples(cursor, 'search_plan',  (cp_form(None),))
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