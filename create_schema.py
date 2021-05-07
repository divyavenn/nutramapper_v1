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
def create_table(cursor, table_name, fields, from_table_name, from_table_fields):
    cursor.execute("drop table if exists " + table_name)
    query = "create table " + table_name + " (" + t2str(fields) + ")"
    print(query)
    cursor.execute(query)
    if (from_table_name is not None):
        # populate nutrient with relevant data
        query = "select " + t2str(from_table_fields) + " from " + from_table_name
        print(from_table_fields)
        print(query)
        cursor.execute(query)
        subcursor = connection.cursor()
        for i in cursor:
            query = "insert into nutrient ("
            for j in range(0, len(fields)):
                if j == len(fields) - 1:
                    query = query + fields[j].split()[0]
                else:
                    query = query + fields[j].split()[0] + ", "
            query = query + ") values " + q_list(i)
            print(query)
            subcursor.execute(query)

database_name = 'meal_planner.db'
connection = sqlite3.connect(database_name)

cursor = connection.cursor()

#link usda database
cursor.execute("attach database 'usda/usda.db' as usda")

#create table nutrient
create_table(cursor,
             "nutrient",
             ("nutrient_id text primary key not null", "nutrient_name text not null", "units text not null"),
             "usda.nutr_def",
             ("Nutr_No", "nutrdesc", "units"))



connection.commit()
connection.close()


