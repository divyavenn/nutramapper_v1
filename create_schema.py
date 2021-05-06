import os
import sys
import sqlite3

def q_str(x):
    return "'" + str(x) + "'"

def q_list(x):
    ans = "("
    for i in range(0, len(x)):
        if (i == len(x) - 1):
            ans = ans + q_str(x[i]) + ")"
        else:
            ans = ans + q_str(x[i]) + ","
    return ans

#creates a table in meal_planner, optionally from another table
# create_table(cursor:cursor, table_name:str, fields:tuple_str, from_table_name:str/None, from_table_fields:tuple_str/None)
def create_table(cursor, table_name, fields, from_table_name, from_table_fields):
    cursor.execute("drop table if exists " + table_name)
    cursor.execute("create table " + table_name + q_list(fields))
    if (from_table_name is not None):
        cursor.execute("select " + q_list(from_table_fields) + " from " + from_table_name")
        subcursor = connection.cursor()
        for i in cursor:
            subcursor.execute("insert into nutrient(nutrient_id, nutrient_name, units) values " + q_list(i))

database_name = 'meal_planner.db'
connection = sqlite3.connect(database_name)

cursor = connection.cursor()

#link usda database
cursor.execute("attach database 'usda/usda.db' as usda")

#create table nutrient
cursor.execute("drop table if exists nutrient")
cursor.execute('''create table nutrient
(nutrient_id text primary key not null, 
nutrient_name text not null, 
units text not null)''')

#populate nutrient with relevant data from usda.nutr_def
cursor.execute("select Nutr_No, nutrdesc, units from usda.nutr_def")
subcursor = connection.cursor()
for i in cursor:
    subcursor.execute("insert into nutrient(nutrient_id, nutrient_name, units) values " + q_list(i))



connection.commit()
connection.close()


