from ingredient import print_ingredient, add_ingredient
from search import search_recipe, search_ingredient
from nutrient import get_nutrients_to_track, get_nutrient_amount
from data_validation import input_form,qform_varchar,qform_num

#adds up the total amounts for each nutrient of each food item in a recipe
#nutritional_total_recipe(cursor, recipe_id) -> [id, name, total_in_recipe, units]
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
            total = total + grams*amount_per_100_grams/100
        # [nutrient id, nutrient name, total in recipe, units]
        nutr_totals.append([nutrient[0], nutrient[1], total, nutrient[3]])
    return nutr_totals


# adds new recipe
# cursor -> None
def add_recipe(cursor):
    name = input("What is the name of this recipe?")
    if not (input_form(name) == 0):
        print("That's not a valid recipe name. Try again.")
        add_recipe(cursor)
    else:
        cursor.execute('insert into recipe (recipe_name) values ( "' + name + ' ")')
        recipe_id = None
        # find recipe_id of new recipe
        cursor.execute("select recipe_id from recipe where (recipe_name = '" + name + "')")
        for i in cursor:
            recipe_id = i[0]
        while (input("Would you like to add an ingredient [Y/N]") == "Y"):
            add_ingredient(cursor, recipe_id, None)

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
    cursor.execute(query)
    recipes = []
    for r in cursor:
        print(r[0])
        recipes.append(r)
    if (len(recipes) == 0):
        return False
    else:
        return True



# rename_recipe(cursor, recipe_id) -> None
def rename_recipe(cursor, recipe_id):
    new_name = input("Enter a new name for the recipe:")
    if not(input_form(new_name) == 0):
        print("That's not a valid recipe name. Try again.")
        rename_recipe(cursor, recipe_id)
    else:
        query = "update recipe set recipe_name = " + qform_num(new_name) + "where recipe_id = " + qform_num(recipe_id)
        cursor.execute(query)

# delete_recipe(cursor, recipe_id) -> None
def delete_recipe(cursor, recipe_id):
    query = "delete from recipe where recipe_id = " + qform_num(recipe_id)
    cursor.execute(query)

