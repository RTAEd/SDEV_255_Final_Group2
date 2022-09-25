import sqlite3
import os
import time

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
        os.system('clear')
        print("\nInvalid input detected. Please enter a valid choice.")
        return validate(choice, option)
  return int(choice)

#Fuction to let user login into the app
def login_account():
  print("Login to Password Manager\n")
  user_input = input("USERNAME: ")
  pw_input = input("PASSWORD: ")
  os.system('clear')
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
              os.system('clear')
              return updatePassword()
            else:  
              os.system('clear')
              return selectWebsite(my_account.account_id)
    except:
        os.system('clear')
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
    os.system('clear')
    print(f"NOTICE: {my_account.account_name} has not added any new accounts.")
    time.sleep(3)
    os.system('clear')
    choice = 1
    return welcome(choice)
  #check the choice input by comparing the rows from the queries
  else:  
    try:
        choice = int(input("\nEnter Choice: "))
        assert row >= choice >= 0
        if choice == 0:
          os.system('clear')
          return welcome(choice)
        else:  
          web = ans[choice-1]
          #save information 
          for column in web:
            info.web_id = web[0]
            info.site_name = web[1]
            info.url = web[2]
    except:
        os.system('clear')
        print("\nInvalid input detected. Please enter a valid choice.")
        return selectWebsite(account_id)
  os.system('clear')
  return viewInfo(info.web_id)

#welcomes the user to the main menu. Allow options to view/add accounts
def welcome(choice):
  print(f"Welcome Back, {my_account.account_name}!\n".center(100))
  print("------------------------------------------------------------\n".center(100))
  #Give the user options
  choice = validate(choice, True)
  while (True):
    if choice == 1:
      os.system('clear')
      selectWebsite(my_account.account_id)
      break
    elif choice == 2:
      os.system('clear')
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
          os.system('clear')
          return welcome(choice)
        elif choice == 2:
          # You can insert return password generator function here
          return print("This is where the function to generate password will be")
        else:
          os.system('clear')
          return welcome(choice)
  except:
          os.system('clear')
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
  os.system('clear')
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
  print(f"Welcome to Group 4 Password Manager!\n".center(100))
  print("------------------------------------------------------------\n".center(100))
  #Give the user options
  choice = validate(choice, False)
  while (True):
    if choice == 1:
      os.system('clear')
      login_account()
      break
    elif choice == 2:
      os.system('clear')
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
os.system('clear')
print("Exiting...")
