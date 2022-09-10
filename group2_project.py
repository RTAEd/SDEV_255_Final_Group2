# class to define password object elements
class Password:
    lower_case_lellers_list = [
        'a','b','c','d','e','f',
        'g','h','i','j','k','l',
        'm','n','o','p','q','r',
        's','t','u','v','w','x',
        'y','z']

    upper_case_letter_list = [
        'A','B','C','D','E','F'
        'G','H','I','J','K','L'
        'M','N','O','P','Q','R',
        'S','T','U','V','W','X',
        'Y','Z']

    numbers_list = [0,1,2,3,4,5,6,7,8,9]

    # Excludes quotes and slashes
    symbols_list = [
        '~','`','!','@','#','$',
        '%','^','&','*','(',')',
        '_','-','+','=','{','}',
        '[',']','|',':',';','<',
        '>','.','?']
    # Initializa and assign attributes
    def __init__(self, password_len = 8, ... ) -> None:
        self.password_len = password_len
        ...
        pass
    pass

# Accept input from user which will define password format
def generate_user_input():
    pass

# Generate a Password object
def generate_password():
    pass

# Format and render output for generated password
def generate_output():
    pass