
from data_validation import *
from search import *
from print_methods import print_nutrient, print_nutrient_requ, cls


#NUTRIENT DATA: [nutrient id, amt, food_id]
#DAILY_REQS: [nutrient_id, nutrient name, daily requirement, units]
#NUTRIENT: [nutrient_id, nutrient_name, units]

# gets amount of nutrient in food item
# cursor, food_id, nutrient_id/None -> [nutrient id, amt, food_id]
def get_nutrient_amount(cursor, food_id, nutrient_id):
    #cursor, food_id, nutrient_id/None -> [nutrient id, amt, food_id]
    x = search_nutrient_data(cursor, food_id, nutrient_id)
    if (x is None):
        return 0
    else:
        return x[1]

#cursor, nutrient_id -> [nutrient_id, nutrient name, daily requirement, units]
def get_daily_req(cursor, nutrient_id):
    return cp_get_tuple(cursor, 'search_daily_requ', (nutrient_id,))

#gets the list of nutrients that are being tracked along with DV
# get_nutrients_to_track(cursor) -> [nutrient_id, nutrient name, daily requirement, units]
def get_nutrients_to_track(cursor):
    return cp_get_list_of_tuples(cursor, 'get_nutrients_to_track', ())

#returns if given nutrient is being tracked
# cursor, nutrient -> boolean
def is_part_of_nutrients_to_track(cursor, nutrient):
    nttList = get_nutrients_to_track(cursor)
    if nttList is not None:
        return (nutrient[0] in (i[0] for i in nttList))
    else:
        return False

# updates requirement of nutrient with option to add
# cursor, nid -> None
def update_nutrients_to_track(cursor, nid):
    x = search_nutrient(cursor, nid)
    if x is None:
        print("Nutrient does not exist.")
        return None
    else:
        is_part = is_part_of_nutrients_to_track(cursor, x)
        # Nutrient is indeed part of list; can update
        if (is_part):
            r = input_number("How many " + x[2] + " would you like to consume daily, on average?")
            query = "update daily_nut_requ set requ = " + qform_num(r) + " where nutrient_id = " + qform_varchar(x[0])
            cursor.execute(query)
        else:
            cls()
            print("That nutrient is not part of the daily requirements.\n")
            print_nutrient(x)
            if input_yes("Would you like to add it?"):
                add_nutrients_to_track(cursor, x[0])
            # Nutrient is not part of list; must add


#Adds given nutrient to
#cursor, nid -> None
def add_nutrients_to_track(cursor, nid):
    # cursor, food_id/None, nutrient_id/None -> [nutrient id, amt, food_id]
    n = search_nutrient(cursor, nid)
    if n is None:
        print("Nutrient does not exist.")
        return None
    else:
        is_part = is_part_of_nutrients_to_track(cursor, n)
        if (is_part):
            cls()
            print("That nutrient is already part of the daily requirements.\n")
            daily_requ = get_daily_req(cursor, n[0])
            print_nutrient_requ(daily_requ)
            if input_yes("Would you like to update it?"):
                update_nutrients_to_track(cursor, n[0])
        else:
            r = input_number("How many " + n[2] + " would you like to consume daily, on average?")
            cursor.callproc('add_nutrients_to_track', (n[0], r))


def remove_nutrients_to_track(cursor):
    nutr_to_track = get_nutrients_to_track(cursor)
    if nutr_to_track is not None:
        for n in nutr_to_track:
            print_nutrient_requ(n)
        x = search_nutrient(cursor, None)
        if x is not None:
            if is_part_of_nutrients_to_track(cursor, x):
                cursor.callproc('remove_nutrients_to_track', (x[0],))
            else:
                print("Nutrient is not part of tracked requirements. \n")
        else:
            print("Nutrient does not exist.")
    else:
        print("Nutrient is not part of tracked requirements. \n")
