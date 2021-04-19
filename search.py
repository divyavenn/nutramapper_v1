import pymysql
from data_validation import input_form

# Searches for ingredient by name or by specific nid (if not, None), returns nutritional info
# cursor, nid/None -> [nutrient_id, nutrient_name, units]
def search_nutrient(cursor, nid):
    x = []
    if (nid == None):
        x = search(cursor, "Enter a nutrient", "nutrient_id, nutrient_name, units", "nutrient", "nutrient_name", "nutrient_id")
    else:
        cursor.execute("select nutrient_id, nutrient_name, units from nutrient where nutrient_id = " + nid)
        for i in cursor:
            x = i
    return x;


#Searches for a unique result using user input. performs data validation to avoid SQL errors
def search(cursor, dialogue, allCols, table, name_Col, id_Col):
    x = input(dialogue + "\n")
    form = input_form(x)
    if (form == -2):
        print("You did not not type anything")
        return search(cursor, dialogue, allCols, table, name_Col, id_Col)
    elif (form == -1):
        print("Invalid input")
        return search(cursor, dialogue, allCols, table, name_Col, id_Col)
    elif(form == 0):
        query = "select " + allCols + " from " + table + " where " + name_Col + " like '" + x + "%'"
        if (cursor.execute(query) == 1):
            for i in cursor:
                return i
        else:
            print("Not an exact match. Any similar matches are printed below:")
            for i in cursor:
                print(i)
            return search(cursor, dialogue, allCols, table, name_Col, id_Col)
    elif(form == 1):
        query = "select " + allCols + " from " + table + " where " + id_Col + " = " + x + ""
        if (cursor.execute(query) == 1):
            for i in cursor:
                return i
        else:
            print("Invalid ID. Try again.")
            return search(cursor, dialogue, allCols, table, name_Col, id_Col)
    else:
        return search(cursor, dialogue, allCols, table, name_Col, id_Col)


