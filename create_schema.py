#!/usr/bin/python
"""Parses USDA flat files and converts them into an sqlite database"""

import os
import sys

if sys.version_info.major == 3:
    unicode = str
import json
import sqlite3
import argparse

database_name = 'meal_planner.db'
database = sqlite3.connect(database_name)

database.row_factory = sqlite3.Row
create_table_stmt = {}
create_table_stmt["food_des"] = '''DROP TABLE IF EXISTS food_des; CREATE TABLE food_des 
									(NDB_No text, FdGrp_Cd, Long_Desc, Shrt_Desc, ComName, ManufacName, Survey, 
									Ref_desc, Refuse integer, SciName, N_Factor real, Pro_Factor real, Fat_Factor real, CHO_Factor real);
									CREATE UNIQUE INDEX food_des_ndb_no_idx ON food_des (NDB_No)'''


def insert_row(self, cursor, datatype, fields):
    """Inserts a row of data into a specific table based on passed datatype"""

    # Generate insert parameters string
    insert_params = "(" + ",".join(['?' for x in fields]) + ")"
    query = "insert into " + datatype + " values " + insert_params, fields
    # Execute insert
    cursor.execute("insert into " + datatype + " values " + insert_params, fields)

    def refresh(self, filename, datatype):
        """Converts the passed file into database table. Drops the table and recreats it if it already exists."""

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


def main():


# Only execute if calling file directly
if __name__ == "__main__":
    main()
