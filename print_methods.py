from search import search_food_item, search_ingredient, search_recipe, q_get_tuple, q_get_list_of_tuples, search_meal
from recipe import nutritional_total_recipe
from meal import recipe_id_meal
from data_validation import qform_varchar, qform_num
from plan import plan_name_plan, fulfills_nutritional_reqs

# pretty-prints single nutrient
# [nutrient_id, nutrient_name, units] -> None
def print_nutrient(n):
    print("[ID " + str(n[0]) + "] : " + n[1] + " measured in " + n[2])

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