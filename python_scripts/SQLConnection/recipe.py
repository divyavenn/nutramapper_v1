from ingredient import add_ingredient
from search import *
from nutrient import get_nutrients_to_track, get_nutrient_amount
from data_validation import *
import decimal


#finds the total grams in the recipe
#total_grams(cursor, recipe_id) -> grams
def total_grams(cursor, recipe_id):
    total = 0
    # search_ingredient(cursor, food_id/None, recipe_id/None) -> [food_id, recipe_id, amount_in_grams]
    ingredients = search_ingredient(cursor, None, recipe_id)
    if ingredients is not None:
        for n in ingredients:
            grams = n[2]
            total = total + grams
    return total
#adds up the total amounts for each nutrient of each food item in a recipe
#nutritional_total_recipe(cursor, recipe_id) -> [nutrient_id, nutrient_name, total_in_recipe, units]
def nutritional_total_recipe(cursor, recipe_id):
    nutr_reqs = get_nutrients_to_track(cursor)
    nutr_totals = []
    if (nutr_reqs is not None):
        #search_ingredient(cursor, food_id/None, recipe_id/None) -> [food_id, recipe_id, amount_in_grams]
        ingredients = search_ingredient(cursor, None, recipe_id)
        for nutrient in nutr_reqs:
            total = 0
            if ingredients is not None:
                for n in ingredients:
                    food_id = n[0]
                    grams = n[2]
                    # get_nutrient_amount(cursor, food_id, nutrient_id/None) -> [nutrient id, amt, food_id]
                    amount_per_100_grams = (get_nutrient_amount(cursor, food_id, nutrient[0]))
                    total = total + decimal.Decimal(grams) * decimal.Decimal(amount_per_100_grams)/100
                #[nutrient id, nutrient name, total in recipe, units]
            nutr_totals.append([nutrient[0], nutrient[1], total, nutrient[3]])
    return nutr_totals


# adds new recipe
# cursor -> None
def add_recipe(cursor):
    name = input_name("What is the name of this recipe?")
    recipe_id = 0
    recipe_id = cp_get_value(cursor, 'insert_recipe', (name, recipe_id), 0)
    while (input_yes("Would you like to add an ingredient")):
         add_ingredient(cursor, recipe_id, None)


# rename_recipe(cursor, recipe_id) -> None
def rename_recipe(cursor, recipe_id):
    new_name = input_name("What is the new name of this recipe?")
    query = "update recipe set recipe_name = " + qform_num(new_name) + "where recipe_id = " + qform_num(recipe_id)
    cursor.execute(query)

# delete_recipe(cursor, recipe_id) -> None
def delete_recipe(cursor, recipe_id):
    args = (recipe_id,)
    proc = 'remove_recipe'
    if (search_meal(cursor, recipe_id, None)) is not None:
        if(input_yes("Are you sure? This will delete the recipe from one or more meal plans.")):
            cursor.callproc(proc, args)
    else:
        cursor.callproc(proc, args)
