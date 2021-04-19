from data_validation import qform_varchar, qform_num
from search import search_food_item, search_ingredient


#INGREDIENT: [food_id, recipe_id, amount_in_grams]

#returns if given ingredient already exists
# cursor, recipe_id, food_id -> boolean
def ingredient_exists(cursor, recipe_id, food_id):
    x = search_ingredient(cursor, recipe_id, food_id)
    if (len(x)) == 0:
        return False
    else:
        return True

#checks if ingredient exists;if not, adds it, if so gives option to update ingredient
#cursor, recipe id, food id -> None
def add_ingredient(cursor, recipe_id, food_id):
    if food_id is None:
        food_item = search_food_item(cursor, None)
        food_id = food_item[0]
    if (ingredient_exists(cursor, recipe_id, food_id)):
        print("This ingredient is already a part of the recipe.")
    else:
        amount = input("How many grams of this item does the recipe need?")
        query = ("insert into ingredient (food_id, recipe_id, amount_in_grams) values ("
             + qform_varchar(food_id) + ","
             + qform_num(recipe_id) + ","
             + qform_num(amount) + ")")
        cursor.execute(query)

#checks if ingredient exists;if not, does nothing, if so deletes it
#cursor, recipe id, food id/None -> None
def remove_ingredient(cursor, recipe_id, food_id):
    if food_id is None:
        food_item = search_food_item(cursor, None)
        food_id = food_item[0]
    if (ingredient_exists(cursor, recipe_id, food_id)):
        query = ("delete from ingredient where recipe_id = "  + qform_num(recipe_id) + "and food_id = " + qform_varchar(food_id))

#checks if ingerent exists; if so, alters the amount, if not gives option to add
#cursor, recipe id, food id/None -> None
def alter_ingredient(cursor, recipe_id, food_id):
    if food_id is None:
        food_item = search_food_item(cursor, None)
        food_id = food_item[0]
    if (ingredient_exists(cursor, food_id, recipe_id)):
        new_amt = input('What would you like to change the amount to (in grams)?')
        query = "update ingredient set amount_in_grams =  " + str(new_amt) + "where food_id = " + str(food_id) + "and recipe_id = " + str(recipe_id)
        cursor.execute(query)
    else:
        ans = input("Would you like to add this ingredient? [Y/N]")
        if (ans == "Y"):
            add_ingredient(cursor, recipe_id, food_id)


#pretty prints the ingredient
#cursor, recipe_id, food_id -> None
def print_ingredient(cursor, ingredient):
    food_id = ingredient[0]
    food_item = search_food_item(cursor, food_id)
    food_name = food_item[1]
    amount_in_grams = ingredient[1]
    print("\t " + food_name + ": \n \t \t" + str(amount_in_grams) + " grams")