from data_validation import input_form, qform_varchar, qform_num, input_name, input_number, input_yes
from search import search_recipe, search_meal
from print_methods import print_recipe

#MEAL [recipe_id, plan_id, num_servings]

def recipe_id_meal(meal):
    return meal[0]
def plan_id_meal(meal):
    return meal[1]
def num_servings_meal(meal):
    return meal[2]


#add meal if doesn't exists, if not, give option to update
#add_meal(cursor, plan_id, recipe_id/None)-> None
def add_meal(cursor, plan_id, recipe_id):
    from print_methods import print_recipe_list
    if recipe_id is None:
        print_recipe_list(cursor)
        recipe = search_recipe(cursor, None)
        if recipe is None:
            print("There are no recipes.")
            return None
        else:
            recipe_id = recipe[0]
    # cursor, recipe_id/None, plan_id/None -> [recipe_id, plan_id, num_servings]/None
    if (search_meal(cursor, recipe_id, plan_id) is None):
        amount = input_number("How many servings of this item would you like to add?")
        query = ("insert into meal (recipe_id, plan_id, num_servings) values ("
                 + qform_num(recipe_id) + ","
                 + qform_num(plan_id) + ","
                 + qform_num(amount) + ")")
        cursor.execute(query)
    else:
        print("This recipe is already a part of this plan")
        input("\n \n Press any key to continue.")

#remove meal if exists, if not do nothing
#remove_meal(cursor, plan_id, recipe_id/None)-> None
def remove_meal(cursor, plan_id, recipe_id):
    if recipe_id is None:
        recipe = search_recipe(cursor, None)
        if recipe is None:
            print("There are no recipes.")
            return None
        else:
            recipe_id = recipe[0]
    # cursor, recipe_id/None, plan_id/None -> [recipe_id, plan_id, num_servings]/None
    if not (search_meal(cursor, recipe_id, plan_id) is None):
        query = ("delete from meal where recipe_id =" + qform_num(recipe_id) + " and plan_id = " + qform_num(plan_id))
        cursor.execute(query)

#alter meal if exists, if not give option to add
#alter_meal(cursor, plan_id, recipe_id/None)-> None
def alter_meal(cursor, plan_id):
    recipe = search_recipe(cursor, None)
    if recipe is None:
        print("There are no recipes.")
        return None
    else:
        recipe_id = recipe[0]
    # cursor, recipe_id/None, plan_id/None -> [recipe_id, plan_id, num_servings]/None
    if (search_meal(cursor, recipe_id, plan_id) is None):
        if(input_yes("This recipe is not part of the plan. Would you like to add it?")):
            add_meal(cursor, plan_id, recipe_id)
    else:
        new_amt = input_number('What would you like to change the number of servings to?')
        query = "update meal set num_servings =  " + qform_num(new_amt) + "where recipe_id = " + qform_num(recipe_id) + "and plan_id = " + qform_num(plan_id)
        cursor.execute(query)
