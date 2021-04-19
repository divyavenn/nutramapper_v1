
from data_validation import input_form, input_name, input_number, input_yes, qform_num, qform_varchar
from search import q_get_tuple, q_get_list_of_tuples, q_get_value, search_meal, search_plan
from meal import add_meal
from nutrient import get_nutrients_to_track
from recipe import nutritional_total_recipe

#PLAN = [plan_id, plan_name, num_days]
def plan_id_plan(plan):
    return plan[0]
def plan_name_plan(plan):
    return plan[1]
def num_days_plan(plan):
    return plan[2]

#adds a new plan
#cursor -> None
def add_plan(cursor):
    name = input_name("What is the name of this plan?")
    days = input_number("How many days does this meal plan cover?")

    query = "insert into plan (plan_name, num_days) values ( " + qform_varchar(name) + "," + qform_num(days) + ")"
    cursor.execute(query)
    # find recipe_id of new plan
    query = "select plan_id from plan where (plan_name = " + qform_varchar(name) + ")"
    plan_id = q_get_value(cursor, query, 0)
    while (input_yes("Would you like to add a recipe?")):
        add_meal(cursor, plan_id, None)

#adds a new plan
#cursor -> None
def remove_plan(cursor, plan_id):
    query = "delete from plan where plan_id = " + qform_num(plan_id)
    cursor.execute(query)

#adds a new plan
#cursor -> None
def change_plan_days(cursor, plan_id):
    days = input_number("What number of days should this plan cover?")
    query = "update plan set num_days = " + qform_num(days) + "where plan_id = " + qform_num(plan_id)
    cursor.execute(query)

#adds a new plan
#cursor -> None
def rename_plan(cursor, plan_id):
    new_name = input_name("Enter a new name for the recipe")
    query = "update recipe set plan_name = " + qform_varchar(new_name )+ "where plan_id = " + qform_num(plan_id)
    cursor.execute(query)


def fulfills_nutritional_requs(cursor, plan_id):
    meals = search_meal(cursor, None, plan_id)
    plan = search_plan(cursor, plan_id)
    if not meals is None:
        daily_reqs = []
        #cursor -> [nutrient_id, nutrient name, daily requirement, units]
        nutrients = get_nutrients_to_track(cursor)
        for n in nutrients:
            daily_reqs.append(n[2])
        recipe_totals = []
        planwide_avg = []
        num_days = num_days_plan(plan_id)
        for m in meals:
            recipe_id = m[0]
            recipe_totals.append(nutritional_total_recipe(cursor, recipe_id))
        for i in range(0,len(daily_reqs)):
            sum = 0
            for r in recipe_totals:
                sum = sum + r[i]
            planwide_avg[i] = sum/num_days
            if planwide_avg[i] < daily_reqs[i]:
                diff = daily_reqs[i] - planwide_avg[i]
                print("You miss your goal for " + nutrients[i][2] + " by an average of: \n" + str(diff) + " " + nutrients[i][3] + " per day.")
            elif planwide_avg[i] > daily_reqs[i]:
                surplus = planwide_avg[i] - daily_reqs[i]
                print("You exceed your goal for " + nutrients[i][2] + " by an average of: \n" + str(surplus) + " " + nutrients[i][3] + " per day.")
