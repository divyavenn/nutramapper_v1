from ingredient import add_ingredient
from search import search_recipe, search_ingredient, q_get_value, q_get_tuple, q_get_list_of_tuples
from nutrient import get_nutrients_to_track, get_nutrient_amount
from data_validation import input_form, qform_varchar, qform_num, input_name, input_number, input_yes
import decimal

#adds up the total amounts for each nutrient of each food item in a recipe
#nutritional_total_recipe(cursor, recipe_id) -> [nutrient_id, nutrient_name, total_in_recipe, units]
def nutritional_total_recipe(cursor, recipe_id):
    nutr_reqs = get_nutrients_to_track(cursor)
    #search_ingredient(cursor, food_id/None, recipe_id/None) -> [food_id, recipe_id, amount_in_grams]
    ingredients = search_ingredient(cursor, None, recipe_id)
    nutr_totals = []
    for nutrient in nutr_reqs:
        total = 0
        for n in ingredients:
            food_id = n[0]
            grams = n[2]
            # get_nutrient_amount(cursor, food_id, nutrient_id/None) -> [nutrient id, amt, food_id]
            amount_per_100_grams = (get_nutrient_amount(cursor, food_id, nutrient[0]))
            total = total + decimal.Decimal(grams) * decimal.Decimal(amount_per_100_grams)/100
        # [nutrient id, nutrient name, total in recipe, units]
        nutr_totals.append([nutrient[0], nutrient[1], total, nutrient[3]])
    return nutr_totals


# adds new recipe
# cursor -> None
def add_recipe(cursor):
    name = input_name("What is the name of this recipe?")
    query = "insert into recipe (recipe_name) values (" + qform_varchar(name) + ")"
    cursor.execute(query)
    recipe_id = None
     # find recipe_id of new recipe
    query = ("select recipe_id from recipe where (recipe_name = " + qform_varchar(name) + ")")
    recipe_id = q_get_value(cursor, query, 0)
    while (input("Would you like to add an ingredient [Y/N]") == "Y"):
         add_ingredient(cursor, recipe_id, None)


# rename_recipe(cursor, recipe_id) -> None
def rename_recipe(cursor, recipe_id):
    new_name = input_name("What is the name of this recipe?")
    query = "update recipe set recipe_name = " + qform_num(new_name) + "where recipe_id = " + qform_num(recipe_id)
    cursor.execute(query)

# delete_recipe(cursor, recipe_id) -> None
def delete_recipe(cursor, recipe_id):
    query = "delete from recipe where recipe_id = " + qform_num(recipe_id)
    cursor.execute(query)

