class Password():

    def __init__(self): 
    # List of lower-case elements for password
        self.lower_case_lellers_list = [
            'a','b','c','d','e','f',
            'g','h','i','j','k','l',
            'm','n','o','p','q','r',
            's','t','u','v','w','x',
            'y','z']
        # List of upper-case elements for password
        self.upper_case_letter_list = [
            'A','B','C','D','E','F',
            'G','H','I','J','K','L',
            'M','N','O','P','Q','R',
            'S','T','U','V','W','X',
            'Y','Z']
        # List of number elements for password
        self.numbers_list = ['0','1','2','3','4','5','6','7','8','9']

        # List of symbol elements for password: Excludes quotes and slashes
        self.symbols_list = [
            '~','`','!','@','#','$',
            '%','^','&','*','(',')',
            '_','-','+','=','{','}',
            '[',']','|',':',';','<',
            '>','.','?']

        # Combined list of elemnts for remaining characters after specified elements are added
        self.remaining_chars = list(
                self.lower_case_lellers_list +
                self.upper_case_letter_list +
                self.numbers_list +
                self.symbols_list)

        self.get_length = 8
        self.get_lower = 0
        self.get_upper = 0
        self.get_nums = 0
        self.get_symbols = 0
        self.passSpecs = {}
        self.password_elements = []

        # Request user input for definition of password
    @classmethod
    def generate_user_input(self):
            self.get_length = abs(int(input("Please enter the minimum length for your password?: ")))
            self.get_lower = abs(int(input("Please enter the minimum number of lower-case letters. Enter '0' if you do not wish to include this element: ")))
            self.get_upper = abs(int(input("Please enter the minimum number of upper-case letters: Enter '0' if you do not wish to include this element: ")))
            self.get_nums = abs(int(input("Please enter the minimum number of numbers?: Enter '0' if you do not wish to include this element: ")))
            self.get_symbols = abs(int(input("Please enter the minimum number of special symbols?: Enter '0' if you do not wish to include this element: ")))

            passSpecs = {'length': self.get_length, 'lower':self.get_lower, 'upper':self.get_upper, 'numbers':self.get_nums, 'symbols':self.get_symbols}

            return passSpecs


        # Takes the output of the previous function as an argument and creates the password
    @classmethod  
    def passGen(self,passSpecs):
            import random
            self.password_elements = []
            
            # Fulfill the user required characters first 
            for i in range (passSpecs['lower']):
                self.password_elements.append(random.choice(self.lower_case_lellers_list))
            for i in range (passSpecs['upper']):
                self.password_elements.append(random.choice(self.upper_case_letter_list))
            for i in range (passSpecs['numbers']):
                self.password_elements.append(random.choice(self.numbers_list))
            for i in range (passSpecs['symbols']):
                self.password_elements.append(random.choice(self.symbols_list))

            # Full list of characters to fill in based on the user requirements if not over max
            while len(self.password_elements) < (passSpecs['length']):
                    self.password_elements.append(random.choice(self.remaining_chars))          
                
            random.shuffle(self.password_elements)
            password = "".join(self.password_elements)

            return password
    

# KEEP(
print(Password.passGen(Password.generate_user_input()))
