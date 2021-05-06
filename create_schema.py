import os
import sys
import sqlite3

database_name = 'meal_planner.db'
db = sqlite3.connect(database_name)

cursor = db.cursor()

cursor.execute("attach database 'usda.db' as usda")
cursor.execute("drop table if exists nutrient")
cursor.execute("create table nutrient(nutrient_id, nutrient_name, units)")
cursor.execute("select Nutr_No, nutrdesc, units from usda.nutr_def")
for i in cursor:
    print(i)
    cursor.execute("insert into nutrient(nutrient_id, nutrient_name, units) values ('" + str(i[0]) + "','" + str(i[1]) + "','" + str(i[2]) + "')")
cursor.execute("select * from nutrient")
for i in cursor:
    print(i)
def insert_row(self, cursor, datatype, fields):
    # Generate insert parameters string
    insert_params = "(" + ",".join(['?' for x in fields]) + ")"
    query = "insert into " + datatype + " values " + insert_params, fields
    # Execute insert
    cursor.execute("insert into " + datatype + " values " + insert_params, fields)

def refresh(self, filename, datatype):
    # Init database cursor
    cursor = self.database.cursor()

    # Refresh the table definition
    self.create_table(cursor, datatype)

    # Print out which file we are working on
    sys.stdout.write("Parsing " + filename + '...')
    sys.stdout.flush()

    # Iterate through each line of the file
    with open(filename, 'rU') as f:
        for line in f:
            # Break up fields using carets, remove whitespace and tilda text field surrounders
            # We also need to decode the text from the Windows cp1252 encoding used by the USDA files
            fields = [unicode(field.strip().strip('~')) for field in line.split('^')]
            # Insert row into database
            self.insert_row(cursor, datatype, fields)

    # Commit changes to file
    self.database.commit()

    # Done message
    print("Done")

def create_table(self, cursor, datatype):
    """Creates a new table in the database based on the datatype. Drops existing table if there is one."""

    # Create new table
    cursor.executescript(self.create_table_stmt[datatype])

