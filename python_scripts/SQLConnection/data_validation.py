import string

#returns -2 for empty input, -1 for invalid input, 0 for name, 1 for id
def input_form(str):
    name = set(string.ascii_lowercase + string.ascii_uppercase + ',' + string.digits + '%' + '(' + ')' + '-' + ' ')
    id = set(string.digits + ".")
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

def cp_form(x):
    if x is None:
        return "%"
    else:
        return x


def input_name(str):
    name = input(str)
    while not(input_form(name) == 0):
        print("That's not a valid name. Try again.")
        return input_name(str)
    return name

def input_number(str):
    num = input(str)
    while not(input_form(num) == 1):
        print("That's not a valid number. Try again.")
        return input_number(str)
    return num

def input_number_not_zero(str):
    num = input_number(str)
    if (int(num) == 0):
        print("You cannot set this value to zero. Try again.")
        return input_number_not_zero(str)
    else:
        return num

def input_yes(str):
    affirmatives = set("yes" + "y" + "ok" + "okay" + "sure")
    negatives = set("no" + "n")
    ans = input(str + "[Y/N]")
    if ans.lower() in affirmatives:
        return True
    elif ans.lower() in negatives:
        return False
    else:
        print("Invalid input. Try again.")
        return input_yes(str)
