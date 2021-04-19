from data_validation import input_form, qform_varchar, qform_num
from search import search_recipe, q_get_tuple, q_get_list_of_tuples
from recipe import print_recipe

#MEAL [recipe_id, plan_id, num_servings]

def recipe_id_meal(meal):
    return meal[0]
def plan_id_meal(meal):
    return meal[1]
def num_servings_meal(meal):
    return meal[2]
# Adds no
#add_meal(cursor, plan_id, recipe_id)-> None
def add_meal(cursor, plan_id, recipe_id):
    if recipe_id is None:
        recipe = search_recipe(cursor, None)
        print_recipe(recipe)
        recipe_id = recipe[0]
    amount = input("How many servings of this item would you like to add?")
    if(input_form(amount)==1):
        query = ("insert into meal (recipe_id, plan_id, num_servings) values ("
                 + qform_num(recipe_id) + ","
                + qform_num(plan_id) + ","
                + qform_num(amount) + ")")
        cursor.execute(query)
    else:
        print("Please enter a numeric input:")
        add_meal(cursor, plan_id, recipe_id)

