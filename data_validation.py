import string
#returns -2 for empty input, -1 for invalid input, 0 for name, 1 for id
def input_form(str):
    name = set(string.ascii_lowercase + string.ascii_uppercase + ',' + string.digits + '%' + '(' + ')' + '-' + ' ')
    id = set(string.digits)
    if len(str) == 0:
        return -2
    elif all(letter in id for letter in str):
        return 1
    elif all(letter in name for letter in str):
        return 0
    else:
        return -1

#returns value of a variable that holds varchar data formatted for a query
def qform_varchar(x):
    return " '" + str(x) + "'"

#returns value of a variable that holds numerical data formatted for a query
def qform_num(x):
    return " '" + str(x) + "'"


