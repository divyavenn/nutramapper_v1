import os
import sys
import sqlite3

def q_str(x):
    return '"' + str(x) + '"'

def q_list(x):
    ans = "("
    for i in range(0, len(x)):
        if (i == len(x) - 1):
            ans = ans + q_str(x[i]) + ")"
        else:
            ans = ans + q_str(x[i]) + ","
    return ans

def t2str(x):
    ans = ""
    for i in range(0, len(x)):
        if (i == len(x) - 1):
            ans = ans + str(x[i]) + ""
        else:
            ans = ans + str(x[i]) + ","
    return ans
#creates a table in meal_planner, optionally from another table
# create_table(cursor:cursor, table_name:str, fields:tuple_str, from_table_name:str/None, from_table_fields:tuple_str/None)
def create_table(cursor, table_name, fields, constraints, from_table_name, from_table_fields):
    cursor.execute("drop table if exists " + table_name)
    query = "create table " + table_name + " (" + t2str(fields)
    if constraints is not None:
        query = query + ", " + constraints
    query = query + ")"
    cursor.execute(query)
    if (from_table_name is not None):
        # populate nutrient with relevant data
        query = "select " + t2str(from_table_fields) + " from " + from_table_name
        cursor.execute(query)
        subcursor = connection.cursor()
        for i in cursor:
            query = "insert into " + table_name + " ("
            for j in range(0, len(fields)):
                if j == len(fields) - 1:
                    query = query + fields[j].split()[0]
                else:
                    query = query + fields[j].split()[0] + ", "
            query = query + ") values " + q_list(i)
            subcursor.execute(query)

database_name = 'meal_planner.db'
connection = sqlite3.connect(database_name)

cursor = connection.cursor()

#link usda database
cursor.execute("attach database 'usda/usda.db' as usda")


#create table nutrient
print("Creating table nutrient...")
create_table(cursor,
             "nutrient",
             ("nutrient_id text not null", "nutrient_name text not null", "units text not null"),
             "primary key (nutrient_id)",
             "usda.nutr_def",
             ("Nutr_No", "nutrdesc", "units"))

print("Done!")
print("Creating table nutrient_data...")
#create nutrient_data
create_table(cursor,
             "nutrient_data",
             ("nutrient_id text", "food_id text", "amt real"),
             '''primary key (nutrient_id, food_id),
             foreign key (food_id) references food_item(food_id) on delete restrict on update cascade,
             foreign key (nutrient_id) references nutrient(nutrient_id) on delete restrict on update cascade''',
             "usda.nut_data",
             ("Nutr_No", "ndb_no", "nutr_val"))

print("Done!")
print("Creating table food_item...")
#create food_item
create_table(cursor,
             "food_item",
             ("food_id text", "food_name text"),
             "primary key (food_id)",
             "usda.food_des",
             ("ndb_no", "Long_Desc"))

print("Done!")
print("Creating table daily_nut_requ...")

#create daily_nut_requ
create_table(cursor,
             "daily_nut_requ",
             ("nutrient_id text not null", "requ real not null"),
             '''primary key (nutrient_id),
             foreign key (nutrient_id) references nutrient(nutrient_id) on delete restrict on update cascade
             ''',
             None,
             None)
print("Done!")
print("Creating table plan...")
#create plan
create_table(cursor,
             "plan",
             ("plan_id int not null", "plan_name text not null", "num_days real not null"),
             '''primary key (plan_id)''',
             None,
             None)

print("Done!")
print("Creating table recipe...")

#create recipe
create_table(cursor,
             "recipe",
             ("recipe_id int not null", "recipe_name text not null"),
             '''primary key (recipe_id)''',
             None,
             None)

print("Done!")
print("Creating table ingredient...")

#create ingredient
create_table(cursor,
             "ingredient",
             ("food_id text not null", "recipe_id int not null", "amount_in_grams real not null"),
             '''primary key (food_id, recipe_id),
             foreign key (food_id) references food_item(food_id) on delete restrict on update cascade,
             foreign key (recipe_id) references recipe(recipe_id) on delete cascade on update cascade''',
             None,
             None)

print("Done!")
print("Creating table meal...")

#create meal
create_table(cursor,
             "meal",
             ("plan_id int not null", "recipe_id int not null", "num_servings real not null"),
             '''primary key (plan_id, recipe_id),
             foreign key (plan_id) references plan(plan_id) on delete cascade on update cascade,
             foreign key (recipe_id) references recipe(recipe_id) on delete cascade on update cascade''',
             None,
             None)
print("Done!")


connection.commit()
connection.close()


