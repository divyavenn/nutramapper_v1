
from data_validation import qform_varchar, qform_num
from search import search_nutrient, search_nutrient_data


#NUTRIENT DATA: [nutrient id, amt, food_id]
#DAILY_REQS: [nutrient_id, nutrient name, daily requirement, units]
#NUTRIENT: [nutrient_id, nutrient_name, units]

# gets amount of nutrient in food item
# cursor, food_id, nutrient_id/None -> [nutrient id, amt, food_id]
def get_nutrient_amount(cursor, food_id, nutrient_id):
    #cursor, food_id, nutrient_id/None -> [nutrient id, amt, food_id]
    x = search_nutrient_data(cursor, food_id, nutrient_id)
    if (len(x) == 0):
        return 0
    else:
        return x[1]

# pretty-prints single nutrient
# [nutrient_id, nutrient_name, units] -> None
def print_nutrient(n):
    print("[ID " + str(n[0]) + "] : " + n[1] + " measured in " + n[2])


# pretty-prints single nutrient requirements
# [nutrient_id, nutrient name, daily requirement, units] -> None
def print_nutrient_requ(n):
    print("[ID " + str(n[0]) + "] : " + n[1] + " has a daily requirement of " + str(n[2]) + " " + n[3])

#gets the list of nutrients that are being tracked along with DV
# cursor -> [nutrient_id, nutrient name, daily requirement, units]
def get_nutrients_to_track(cursor):
    nutr_to_track = []
    cursor.execute('select n.nutrient_id, n.nutrient_name, d.requ, n.units from daily_nut_requ as d natural join nutrient as n')
    for i in cursor:
        nutr_to_track.append(i)
    return nutr_to_track

#returns if given nutrient is being tracked
# cursor, nutrient -> boolean
def is_part_of_nutrients_to_track(cursor, nutrient):
    nttList = get_nutrients_to_track(cursor)
    return (nutrient[0] in (i[0] for i in nttList))

# updates requirement of nutrient with option to add
# cursor, nid -> None
def update_nutrients_to_track(cursor, nid):
    x = search_nutrient(cursor, nid)
    is_part = is_part_of_nutrients_to_track(cursor, x)
    # Nutrient is indeed part of list; can update
    if (is_part):
        r = input("How many " + x[2] + " would you like to consume daily, on average?")
        query = "update daily_nut_requ set requ = " + qform_num(r) + " where nutrient_id = " + qform_varchar(nid)
        cursor.execute(query)
    else:
        print("That nutrient is not part of the daily requirements.\n")
        print_nutrient(x)
        choice = input("Would you like to add it? [Y/N] \n")
        if (choice == 'Y'):
            add_nutrients_to_track(cursor, x[0])
        # Nutrient is not part of list; must add


#Adds given nutrient to
#cursor, nid -> None
def add_nutrients_to_track(cursor, nid):
    n = search_nutrient(cursor, nid)
    is_part = is_part_of_nutrients_to_track(cursor, n)
    if (is_part):
        print("That nutrient is already part of the daily requirements.\n")
        print_nutrient_requ(n)
        choice = input("Would you like to update it? [Y/N] \n")
        if (choice == 'Y'):
            update_nutrients_to_track(cursor, n[0])
    else:
        r = input("How many " + n[2] + " would you like to consume daily, on average?")
        cursor.execute("insert into daily_nut_requ (nutrient_id, requ) values (" + qform_varchar(n[0]) + "," + qform_num(r) + ")")


def remove_nutrients_to_track(cursor):
    nutr_to_track = get_nutrients_to_track(cursor)
    for n in nutr_to_track:
        print_nutrient_requ(n)
    x = search_nutrient(cursor, None)
    if is_part_of_nutrients_to_track(cursor, x):
        cursor.execute("delete from daily_nut_requ where nutrient_id = " + qform_varchar(x[0]) + "")
    else:
        print("Nutrient is not part of tracked requirements. \n")
