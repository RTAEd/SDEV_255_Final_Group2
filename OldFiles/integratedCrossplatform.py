import sqlite3
import os
import time

class Password():

    def __init__(self): 
    # List of lower-case elements for password
        self.lower_case_letters_list = [
            'a','b','c','d','e','f',
            'g','h','i','j','k','l',
            'm','n','o','p','q','r',
            's','t','u','v','w','x',
            'y','z']
        # List of upper-case elements for password
        self.upper_case_letters_list = [
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
        # An empty list to contain elements of the remaining number of characters in the password
        self.remaining_chars = list()

        # Initiate other class variables
        self.get_length = 8
        self.get_lower = 0
        self.get_upper = 0
        self.get_nums = 0
        self.get_symbols = 0
        self.passSpecs = {}
        self.password_elements = []
#Define object for Password class
characters = Password()        


# Request user input for definition of password
def generate_user_input():
            print("PASSWORD GENERATOR\n".center(100))
            print("------------------------------------------------------------\n".center(100))
            pw_length()
            print()
            passSpecs = {'length': characters.get_length, 'lower':characters.get_lower, 'upper':characters.get_upper, 'numbers':characters.get_nums, 'symbols':characters.get_symbols}

            return passSpecs

def pw_length():
      try:
            characters.get_length = abs(int(input("Enter the preferred length of your password? (Enter '0' to cancel): ")))
            if characters.get_length == 0:
                clear()
                return updatePassword()
            else:
                return num_lowercase(characters.get_length)
      except:
        print("\nInvalid Input Detected. Try Again.\n")  
        return pw_length()
        
def num_lowercase(length):
      try:
            characters.get_lower = abs(int(input("Enter the minimum number of lower-case letters. (Enter '0' to skip): ")))
            assert (length - characters.get_lower) >= 0
            length = length - characters.get_lower
            return num_uppercase(length)
      except:
        if (length - characters.get_lower) < 0:
            print("\nThere's not enough password space remaining for this number of lower-case letters!\n")
        else:
            print("\nInvalid Input Detected. Try Again.\n")
        return num_lowercase(length)
        
def num_uppercase(length):
      try:
            characters.get_upper = abs(int(input("Enter the minimum number of upper-case letters. (Enter '0' to skip): ")))
            assert (length - characters.get_upper) >= 0
            length = length - characters.get_upper
            return num_numbers(length)
      except:
        if (length - characters.get_upper) < 0:
            print("\nThere's not enough password space remaining for this number of upper-case letters!\n")
        else:
            print("\nInvalid Input Detected. Try Again.\n")  
        return num_uppercase(length)
        
def num_numbers(length):
      try:
            characters.get_nums = abs(int(input("Enter the minimum number of numbers. (Enter '0' to skip): ")))
            assert (length - characters.get_nums) >= 0
            length = length - characters.get_nums
            return num_symbol(length)
      except:
        if (length - characters.get_nums) < 0:
            print("\nThere's not enough password space remaining for this number of numbers!\n")
        else:
            print("\nInvalid Input Detected. Try Again.\n")  
        return num_numbers(length)
        
def num_symbol(length):
      try:
            characters.get_symbols = abs(int(input("Enter the minimum number of symbols. (Enter '0' to skip): ")))
            assert (length - characters.get_symbols) >= 0
            assert (length != characters.get_length)
      except:
        if (length - characters.get_symbols) < 0:
            print("\nThere's not enough password space remaining for this number of symbols!\n")  
        elif (length == characters.get_length):
            print("\nYou didn't specify what characters to be generated for your password! Returning to the password option menu...\n")
            time.sleep(3)
            clear()
            return welcome(1) #change to menu
        else:
            print("\nInvalid Input Detected. Try Again.\n")  
        return num_symbol(length)



#  Pass the dictionary to the function will generate a password
def passGen(passSpecs):
            import random
            characters.password_elements = []
     
            
            # Fulfill the user required characters first 
            for i in range (passSpecs['lower']):
                if (passSpecs['lower']) > 0:
                    characters.password_elements.append(random.choice(characters.lower_case_letters_list))
                    characters.remaining_chars.extend(characters.lower_case_letters_list)
                else:
                    pass
            for i in range (passSpecs['upper']):
                if (passSpecs['upper']) > 0:
                    characters.password_elements.append(random.choice(characters.upper_case_letters_list))
                    characters.remaining_chars.extend(characters.upper_case_letters_list)
                else:
                    pass
            for i in range (passSpecs['numbers']):
                if (passSpecs['numbers']) > 0:
                    characters.password_elements.append(random.choice(characters.numbers_list))
                    characters.remaining_chars.extend(characters.numbers_list)
                else:
                    pass
            for i in range (passSpecs['symbols']):
                if (passSpecs['symbols']) > 0:
                    characters.password_elements.append(random.choice(characters.symbols_list))
                    characters.remaining_chars.extend(characters.symbols_list)
                else:
                    pass

            # Full list of characters to fill in based on the user requirements if not over max
            while len(characters.password_elements) < (passSpecs['length']):
                    characters.password_elements.append(random.choice(characters.remaining_chars))          
                
            random.shuffle(characters.password_elements)
            password = "".join(characters.password_elements)
            
  
            return password
    

# Generate the password

#Connecting to a database and preparing queries
database = sqlite3.connect("pw_manager.db")
cursor = database.cursor()

#Store login information
class app_login:
  def _init_(self, account_id, app_user, app_pw, account_name, attempt):
    self.account_id = account_id #primary key
    self.app_user = app_user
    self.app_pw = app_pw
    self.account_name = account_name
    self.attempt = attempt

#Store website information
class websites():
  def _init_self(self, web_id, site_name, url):
    self.web_id = web_id #primary key
    self.site_name = site_name
    self.url = url
    super().__init__()  

#password manager
class manager(websites):
  def _init_(self, log_id, email, username, pw):
    self.log_id = log_id
    self.email = email
    self.username = username
    self.pw = pw


#object that store user account information for this app
my_account = app_login()
#password manager object
info = manager()
#initialize choice option
choice = 1
#record max number of login attempt to access the app
my_account.attempt = 3



def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    
#print menu for whatever options
def print_menu(script):
  if script == True:
    print("Please choose an option (enter 0 to logout): \n")
    print("[1] View login information\n")
    print("[2] Add login information\n")
  else:
    print("Please choose an option (enter 0 to quit): \n")
    print("[1] Login\n")
    print("[2] New User\n")
#validate the choice inputs
def validate(choice, option): 
  choice = 0
  print_menu(option);
  try:
        choice = int(input("Enter Choice: "))
        assert 2 >= choice >= 0
  except:
        clear()
        print("\nInvalid input detected. Please enter a valid choice.")
        return validate(choice, option)
  return int(choice)

#Fuction to let user login into the app
def login_account():
  print("Login to Password Manager\n")
  user_input = input("USERNAME: ")
  pw_input = input("PASSWORD: ")
  clear()
  cursor.execute("SELECT * FROM app WHERE app_user = '" + user_input + "' AND app_pass = '" + pw_input + "'")

  #check number of rows
  empty = cursor.fetchone()
  #check number of attempts. No attempts = exit program
  if empty is None:
    my_account.attempt -=1
    if my_account.attempt == 0:
      print("Too many failed attempts! Exiting program...")
      exit()
    print(f"Login unsuccessful. Please try again! ({my_account.attempt} attempts left)\n")
    login_account()
  else:
    #fetch the account id and name
    cursor.execute("SELECT * FROM app WHERE app_user = '" + user_input + "' AND app_pass = '" + pw_input + "'")
    ans = cursor.fetchall()
    for i in ans:
      my_account.account_id = i[0]
      my_account.account_name = i[3] 
    return welcome(choice)

#Reveal password and username for chosen website
def viewInfo(web_id):
  cursor.execute(f"SELECT username, password FROM login WHERE web_id = {info.web_id}")
  #check number of rows
  empty = cursor.fetchone()
  if empty is None:
    #Go to login function
    print("Empty")
  else:
    cursor.execute(f"SELECT * FROM login WHERE web_id = {info.web_id}")
    ans = cursor.fetchall()
    print(f"LOGIN INFORMATION - {info.site_name}\n".center(100))
    print("------------------------------------------------------------\n".center(100))
    for i in ans:
      print(f"[USERNAME: {i[2]}]\n[PASSWORD: {i[3]}] \n[Associated Email: {i[1]}]")
      info.log_id = i[0]
      info.email = i[1]
      info.username = i[2]
      info.pw = i[3]
    print("\n\n[1] Update Password\n[2] Return")
    try:
            choice = int(input("\nEnter Choice: "))
            assert 1 <= choice <= 2
            if choice == 1:
              clear()
              return updatePassword()
            else:  
              clear()
              return selectWebsite(my_account.account_id)
    except:
        clear()
        return viewInfo(info.web_id)
  


#function that allows the user to pick which account information they want to see
def selectWebsite(account_id):
  count = 1
  #fetch all websites associated with the user's account id
  cursor.execute(f"SELECT * FROM website WHERE account_id = {my_account.account_id}")
  ans = cursor.fetchall()
  print("Which account would you like to view (Enter '0' to return to the main menu)\n")
  for i in ans:
    print(f"[{count}] {i[2]}")
    count+=1
  row = len(ans)
  #For newly created user, there are no website. So it will return to the welcome menu
  if row == 0:
    clear()
    print(f"NOTICE: {my_account.account_name} has not added any new accounts.")
    time.sleep(3)
    clear()
    choice = 1
    return welcome(choice)
  #check the choice input by comparing the rows from the queries
  else:  
    try:
        choice = int(input("\nEnter Choice: "))
        assert row >= choice >= 0
        if choice == 0:
          clear()
          return welcome(choice)
        else:  
          web = ans[choice-1]
          #save information 
          for column in web:
            info.web_id = web[0]
            info.site_name = web[1]
            info.url = web[2]
    except:
        clear()
        print("\nInvalid input detected. Please enter a valid choice.")
        return selectWebsite(account_id)
  clear()
  return viewInfo(info.web_id)

#welcomes the user to the main menu. Allow options to view/add accounts
def welcome(choice):
  print(f"Welcome Back, {my_account.account_name}!\n".center(100))
  print("------------------------------------------------------------\n".center(100))
  #Give the user options
  choice = validate(choice, True)
  while (True):
    if choice == 1:
      clear()
      selectWebsite(my_account.account_id)
      break
    elif choice == 2:
      clear()
      addNewAccount()
      break
    elif choice == 0:
      break
    else:
      print("This is not a valid choice.\n\n")
      False
    choice = validate(choice, True);

#function to change current password for chosen site
def updatePassword():
  print(f"Updating Password for {info.site_name} Account\n".center(100))
  print("------------------------------------------------------------\n".center(100))
  try:
        choice = int(input("Choose an option (Enter '0' to return to the main menu):\n\n[1] Enter new password\n[2] Generate new password\n\nEnter Choice: "))
        assert (0 <= choice <= 2)

        if choice == 1:
          print(f"\nOLD PASSWORD: {info.pw}")
          new_password = input("NEW PASSWORD: ")
          cursor.execute(f'''UPDATE login SET password = "{new_password}" WHERE log_id = "{info.log_id}";''')
          database.commit()
          clear()
          return welcome(choice)
        elif choice == 2:
          new_password = passGen(generate_user_input()) 
          print(f"NEW PASSWORD: {new_password}")
          cursor.execute(f'''UPDATE login SET password = "{new_password}" WHERE log_id = "{info.log_id}";''')
          database.commit()
          time.sleep(3)
          clear()
          return welcome(choice)
       
        else:
          clear()
          return welcome(choice)
  except:
          clear()
          return updatePassword()

#function to add new account
def addNewAccount():
  choice = 1
  print(f"Adding a New Account\n".center(100))
  print("------------------------------------------------------------\n".center(100))
  #make a new log_id for the new entry
  cursor.execute("SELECT max(log_id) FROM login ")
  ans = cursor.fetchall()
  for i in ans:
    info.log_id = int(i[0]) +1
  cursor.execute("SELECT max(web_id) FROM website ")
  ans = cursor.fetchall()
  for i in ans:
    info.web_id = int(i[0]) +1
  #User will input the following information here. Information will be stored  
  info.site_name = input("Please enter the website's name: ")
  info.url = input("Please enter the website's URL: ")
  info.email = input("Please enter the Email you used to sign up: ")
  info.username = input("Please enter your Username for this site: ")
  info.pw = input("Please enter your Password for this site: ")
  #insert the additional information to our database
  cursor.execute(f'INSERT INTO website(web_id, site_name, url, account_id) VALUES ({info.web_id}, "{info.site_name}", "{info.url}",{my_account.account_id})')
  #commit changes
  database.commit()
  cursor.execute(f'INSERT INTO login(log_id, email, username, password, web_id) VALUES ({info.log_id}, "{info.email}", "{info.username}", "{info.pw}", {info.web_id})')
  database.commit()
  clear()
  return welcome(choice)

#Add new User for the app
def newUser():
  print(f"Creating a New User\n".center(100))
  print("------------------------------------------------------------\n".center(100))
  #make a new account_id for the new user
  cursor.execute("SELECT max(account_id) FROM app ")
  ans = cursor.fetchall()
  for i in ans:
    my_account.account_id = int(i[0]) +1
  #User will input the following information
  my_account.account_name = input("Enter your Name: ")
  my_account.app_user = input("Username: ") 
  my_account.app_pw = input("Password: ")
  pass2 = input("Re-enter your Password: ")
  #Checks if password is correct. If not, cancel
  if my_account.app_pw != pass2:
    print("Password does not match. Account creation failed.")
    return start(choice)
  else:
    #Add new user to the database
    cursor.execute(f'INSERT INTO app(account_id, app_user, app_pass, account_name) VALUES ({my_account.account_id}, "{my_account.app_user}", "{my_account.app_pw}", "{my_account.account_name}")')
    database.commit()
    return start(choice)

#The beginning of the program
def start(choice):
  print(f"Welcome to Group 2 Password Manager!\n".center(100))
  print("------------------------------------------------------------\n".center(100))
  #Give the user options
  choice = validate(choice, False)
  while (True):
    if choice == 1:
      clear()
      login_account()
      break
    elif choice == 2:
      clear()
      newUser()
      break
    elif choice == 0:
      break
    else:
      print("This is not a valid choice.\n\n")
      False
    choice = validate(choice, False);

#call start function
start(choice)


#Close the database and end the app program
database.close()
clear()
print("Exiting...")