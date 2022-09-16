import random


# Class Password():

# List of lower-case elements for password
lower_case_lellers_list = [
    'a','b','c','d','e','f',
    'g','h','i','j','k','l',
    'm','n','o','p','q','r',
    's','t','u','v','w','x',
    'y','z']
# List of upper-case elements for password
upper_case_letter_list = [
    'A','B','C','D','E','F',
    'G','H','I','J','K','L',
    'M','N','O','P','Q','R',
    'S','T','U','V','W','X',
    'Y','Z']
# List of number elements for password
numbers_list = ['0','1','2','3','4','5','6','7','8','9']

# List of symbol elements for password: Excludes quotes and slashes
symbols_list = [
    '~','`','!','@','#','$',
    '%','^','&','*','(',')',
    '_','-','+','=','{','}',
    '[',']','|',':',';','<',
    '>','.','?']

# Combined list of elemnts for remaining characters after specified elements are added
remaining_chars = list(
    lower_case_lellers_list +
    upper_case_letter_list +
    numbers_list +
    symbols_list)

# Request user input for definition of password
def generate_user_input():
    get_length = int(input("How long would you like the password to be?: "))
    get_lower = int(input("Please enter the minimum number of lower-case letters. Enter '0' if you do not wish to include this element: "))
    get_upper = int(input("Please enter the minimum number of upper-case letters: Enter '0' if you do not wish to include this element: "))
    get_nums = int(input("Please enter the minimum number of numbers?: Enter '0' if you do not wish to include this element: "))
    get_symbols = int(input("Please enter the minimum number of special symbols?: Enter '0' if you do not wish to include this element: "))

    passFormat = {'length': get_length, 'lower':get_lower, 'upper':get_upper, 'numbers':get_nums, 'symbols':get_symbols}

    return passFormat


# Takes the output of the previous function as an argument and creates the password
def passGen(passFormat):
    password_elements = []
    
    # Fulfill the user required characters first 
    for i in range (passFormat['lower']):
        password_elements.append(random.choice(lower_case_lellers_list))
    for i in range (passFormat['upper']):
        password_elements.append(random.choice(upper_case_letter_list))
    for i in range (passFormat['numbers']):
        password_elements.append(random.choice(numbers_list))
    for i in range (passFormat['symbols']):
        password_elements.append(random.choice(symbols_list))

    # Full list of characters to fill in based on the user requirements if not over max
    while len(password_elements) < (passFormat['length']):
            password_elements.append(random.choice(remaining_chars))          
        
    random.shuffle(password_elements)
    password = "".join(password_elements)

    return password
        


# KEEP
print(passGen(generate_user_input()))

#TODO: Convert the password generatot to a class
#TODO: Update the generator to be able to to eliminate and element (will need to update the remainin_chars list correctly to match.)