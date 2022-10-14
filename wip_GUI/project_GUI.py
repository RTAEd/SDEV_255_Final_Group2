import tkinter as tk
from PIL import ImageTk, Image, ImageSequence
import sqlite3
import time
from tkinter import messagebox
import pyglet
import random

#add fonts
pyglet.font.add_file("fonts/undefeated.ttf")
pyglet.font.add_file("fonts/Parisienne-Small.ttf")
pyglet.font.add_file("fonts/KRV.ttf")

#Once I figure things out, I will move stuff around
connection = sqlite3.connect("data/pw_manager.db")
cursor = connection.cursor()

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
'''''
def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    [password_list.append(random.choice(letters)) for _ in range(nr_letters)]
    [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]
    [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = "".join(password_list)


    password_input.delete(0,END)
    password_input.insert(0,str(password))
'''
#ANyone want to work on the password gen?
""" 
def add():
    keys = ["username", "password"]

    if password_input.get() == "":
        messagebox.showinfo(title="Listen Up", message="no empty fields allowed")

    else:

        value_entry = [username_input.get(), password_input.get()]
        entry_dict = {key: value for (key, value) in zip(keys, value_entry)}

        if messagebox.askyesno(title="please Confirm", message=f"{entry_dict}\n it this okay?"):
            username_input.delete(0, END)
            password_input.delete(0, END)

            with open("data.txt", "a") as data_file:
                data_file.write(f"{str(entry_dict)},\n")
"""


#clear screen
def clearscreen(frame):
    for screen in frame.winfo_children():
        screen.destroy()

#play the opening sequence for D(doris)R(ryan)K(kyle) Studios (dark studios just sounds cooler than group 2)
def opening():
    global group2_logo
    group2_logo = Image.open("assets/group2_logo.gif")
    player = tk.Label(root)
    player.place(x=-1, y=100)
    for group2_logo in ImageSequence.Iterator(group2_logo):
        group2_logo = ImageTk.PhotoImage(group2_logo)
        player.config(image = group2_logo)
        root.update()
        time.sleep(.05)
    player.destroy()


#Check the user's input. Also check the number of login attempts
def fetch_db(username_input, password_input):
    cursor.execute("SELECT * FROM app WHERE app_user = '" + username_input + "' AND app_pass = '" + password_input + "'")
    #check number of rows
    empty = cursor.fetchone()
    #check number of attempts. 
    if empty is None:
        my_account.attempt = my_account.attempt-1
        messagebox.showinfo(title="Login Failed", message=f"Invalid Username or Password\n  Try Again ({my_account.attempt} attempts left)")
        #Auto close app when all attempts are used
        if my_account.attempt == 0:
            root.destroy()
        else:
            clearscreen(frame1)
            load_frame1()
    else:
        #fetch the account information
        #reset attempts when successfully login
        my_account.attempt = 3
        cursor.execute("SELECT * FROM app WHERE app_user = '" + username_input + "' AND app_pass = '" + password_input + "'")
        ans = cursor.fetchall()
        for i in ans:
            my_account.app_user = i[1]
            my_account.app_pw = i[2]
            my_account.account_id = i[0]
            my_account.account_name = i[3]
        load_frame2()
    


#initiallize app
root = tk.Tk()
#the option for resizing the window will cause issues, so I will disable it for now.
root.resizable(False, False) 
root.title("Secret Key Shield")
root.eval("tk::PlaceWindow . center")
bg_color = "#002435"

#The login screen
def load_frame1():
    clearscreen(frame1)
    clearscreen(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    #fram1 widget
    logo_img = ImageTk.PhotoImage(file = "assets/sks_logo.png")
    logo_widget = tk.Label(frame1, image = logo_img, bg = "#002435")
    logo_widget.image = logo_img
    logo_widget.pack()

    username = tk.Label(frame1,text="USERNAME: ", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    # username_input box
    username_input = tk.Entry(frame1,width=35)
    username_input.pack()
    username_input.focus()
    username_input.bind("<Return>", lambda funct1: password_input.focus())
    
    # password: label
    password = tk.Label(frame1,text="PASSWORD: ", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    
    # password_input box
    password_input = tk.Entry(frame1,width=35,show="*")
    password_input.pack()
    password_input.bind("<Return>", (lambda event: fetch_db(username_input.get(), password_input.get())))

    #button to add a new user
    tk.Button(frame1, text="New User", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:newUser()).pack(pady=20)

#Welcome Screen - give options to user to wither view or add login information
def load_frame2():
    clearscreen(frame1)
    clearscreen(frame2)
    frame2.tkraise()
    logo_img = ImageTk.PhotoImage(file = "assets/sks_logo.png")
    logo_widget = tk.Label(frame2, image = logo_img, bg = "#002435")
    logo_widget.image = logo_img
    logo_widget.pack()
    tk.Label(frame2, text = f"Welcome back, {my_account.account_name}!", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    tk.Label(frame2, text = "Please choose an option:\n", bg = bg_color, fg = "white", font=("TkMenuFont", 10) ).pack()
    tk.Button(frame2, text="View Login Information", font = ("TkHeadingFont", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame3()).pack(pady=2, fill = "both")
    tk.Button(frame2, text="Add Login Information", font = ("TkHeadingFont", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:addInfo()).pack(pady=2, fill = "both")
    tk.Button(frame2, text="Logout", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame1()).pack(pady=50)


#View websites screen
def load_frame3():
    clearscreen(frame2)
    frame2.tkraise()
    logo_img = ImageTk.PhotoImage(file = "assets/sks_logo.png")
    logo_widget = tk.Label(frame2, image = logo_img, bg = "#002435")
    logo_widget.image = logo_img
    logo_widget.pack()
    tk.Label(frame2, text = "My Websites", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    tk.Label(frame2, text = "Choose a website to view:\n", bg = bg_color, fg = "white", font=("TkMenuFont", 10) ).pack()
    #shows the list of websites as buttons
    list()
    #return to the previous screen
    tk.Button(frame2, text="Return", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame2()).pack(pady=50)

#List all websites associated with the user    
def list():
    count = 1
    cursor.execute(f"SELECT * FROM website WHERE account_id = {my_account.account_id}")
    ans = cursor.fetchall()
    for i in ans:
        tk.Button(frame2, text=f"{i[2]}", font = ("TkHeadingFont", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda i=i:viewInfo(i[0],i[1])).pack(pady=2, fill = "both")
    row = len(ans)
    #For newly created user, there are no website. The app will let the user know.
    if row == 0:
        tk.Label(frame2, text = f"NOTICE: {my_account.account_name} has not added any new accounts.", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
   
 
#Views the login information for the chosen website
def viewInfo(web_id, site_name):
    clearscreen(frame2)
    frame2.tkraise()
    logo_img = ImageTk.PhotoImage(file = "assets/sks_logo.png")
    logo_widget = tk.Label(frame2, image = logo_img, bg = "#002435")
    logo_widget.image = logo_img
    logo_widget.pack()
    info.web_id = web_id
    info.site_name = site_name
   
    #grab the account information for the chosen website
    cursor.execute(f"SELECT * FROM login WHERE web_id = {info.web_id}")
    ans = cursor.fetchall()
    for i in ans:
      info.log_id = i[0]
      info.email = i[1]
      info.username = i[2]
      info.pw = i[3]
    #display information
    tk.Label(frame2, text = f"Login Information - {info.site_name}", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    tk.Label(frame2, text = f"\n[USERNAME: {info.username}]\n[PASSWORD: {info.pw}] \n[Associated Email: {info.email}]\n", bg = "black", fg = "white", font=("TkMenuFont", 12) ).pack(pady =5, fill = "both")
    #Option to update password
    tk.Button(frame2, text="Update Password", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:updatePassword()).pack(pady=20)
    #Option to return to the website list screen
    tk.Button(frame2, text="Return", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame3()).pack()

#The password update screen
def updatePassword():
    clearscreen(frame2)
    frame2.tkraise()

    logo_img = ImageTk.PhotoImage(file = "assets/sks_logo.png")
    logo_widget = tk.Label(frame2, image = logo_img, bg = "#002435")
    logo_widget.image = logo_img
    logo_widget.pack()
    tk.Label(frame2,text=f"Enter or Generate a new Password", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    tk.Label(frame2,text=f"Press the 'Enter' key to confirm the change", bg = bg_color, fg = "white", font=("TkMenuFont", 10) ).pack()

    username = tk.Label(frame2,text=f"\nOld Password: {info.pw}", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    #User will input their new password here
    password = tk.Label(frame2,text="New Password: ", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    
    # password_input box
    password_input = tk.Entry(frame2,width=35)
    password_input.pack()
    password_input.focus()
    password_input.bind("<Return>", (lambda event: change(password_input.get())))

    #button to generate new password
    tk.Button(frame2, text="Generate", font = ("Parisienne Small", 30), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:viewInfo(info.web_id, info.site_name)).pack(pady=20)
    #button to cancel the update
    tk.Button(frame2, text="Cancel Change", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:viewInfo(info.web_id, info.site_name)).pack(pady=2)

#check for empty entries and updates the passwords
def change(new_password):
    if new_password == "":
        messagebox.showinfo(title="Listen Up", message="no empty fields allowed")
    else:
        cursor.execute(f'''UPDATE login SET password = "{new_password}" WHERE log_id = "{info.log_id}";''')
        connection.commit()
        viewInfo(info.web_id, info.site_name)

#The Screen to add more website/account information
def addInfo():
    clearscreen(frame2)
    frame2.tkraise()
    frame2.pack_propagate(False)
 
    logo_img = ImageTk.PhotoImage(file = "assets/sks_logo.png")
    logo_widget = tk.Label(frame2, image = logo_img, bg = "#002435")
    logo_widget.image = logo_img
    logo_widget.pack()

    #make a new log_id for the new entry
    cursor.execute("SELECT max(log_id) FROM login ")
    ans = cursor.fetchall()
    for i in ans:
        info.log_id = int(i[0]) +1
    cursor.execute("SELECT max(web_id) FROM website ")
    ans = cursor.fetchall()
    for i in ans:
        info.web_id = int(i[0]) +1

    tk.Label(frame2,text="Adding a New Account", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    tk.Label(frame2,text="Please enter the following information:\n", bg = bg_color, fg = "white", font=("TkMenuFont", 10) ).pack()

    # username_input box
    tk.Label(frame2,text="Website Name", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    websitename = tk.Entry(frame2,width=50)
    websitename.pack()
    websitename.focus()
    websitename.bind("<Return>", lambda funct1: url.focus())

    tk.Label(frame2,text="Website URL", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    url = tk.Entry(frame2,width=50)
    url.pack()
    url.bind("<Return>", lambda funct1: email.focus())

    tk.Label(frame2,text="My Associated Email Address", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    email = tk.Entry(frame2,width=50)
    email.pack()
    email.bind("<Return>", lambda funct1: username.focus())

    tk.Label(frame2,text="My Username", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    username = tk.Entry(frame2,width=50)
    username.pack()
    username.bind("<Return>", lambda funct1: password.focus())

    tk.Label(frame2,text="My Password", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    password = tk.Entry(frame2,width=50)
    password.pack()
    password.bind("<Return>", (lambda event: add(info.log_id,info.web_id,websitename.get(),url.get(),email.get(),username.get(),password.get())))

    #button to go back
    tk.Button(frame2, text="Cancel", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame2()).pack(pady=20)


#Checks for empty inputs and updates the new website and its login informations
def add(log_id,web_id,site,url,email,username,password):
    if site == "" or url == "" or email == "" or username == "" or password == "":
        messagebox.showinfo(title="Listen Up", message="no empty fields allowed")

    else:
        #insert the additional information to our database
        cursor.execute(f'INSERT INTO website(web_id, site_name, url, account_id) VALUES ({web_id}, "{site}", "{url}",{my_account.account_id})')
        #commit changes
        connection.commit()
        cursor.execute(f'INSERT INTO login(log_id, email, username, password, web_id) VALUES ({log_id}, "{email}", "{username}", "{password}", {web_id})')
        connection.commit()
        load_frame2()

#New User Screen
def newUser():
    clearscreen(frame2)
    frame2.tkraise()
    frame2.pack_propagate(False)
 
    logo_img = ImageTk.PhotoImage(file = "assets/sks_logo.png")
    logo_widget = tk.Label(frame2, image = logo_img, bg = "#002435")
    logo_widget.image = logo_img
    logo_widget.pack()

    #make a new account_id for the new user
    cursor.execute("SELECT max(account_id) FROM app ")
    ans = cursor.fetchall()
    for i in ans:
        my_account.account_id = int(i[0]) +1

    tk.Label(frame2,text="Adding a New SKS User", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    tk.Label(frame2,text="Create your SKS account:\n", bg = bg_color, fg = "white", font=("TkMenuFont", 10) ).pack()
 
    tk.Label(frame2,text="Fullname", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    name = tk.Entry(frame2,width=50)
    name.pack()
    name.focus()
    name.bind("<Return>", lambda funct1: username.focus())

    # username_input box
    tk.Label(frame2,text="Username", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    username = tk.Entry(frame2,width=50)
    username.pack()
    username.bind("<Return>", lambda funct1: password.focus())

    tk.Label(frame2,text="Password", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    password = tk.Entry(frame2,width=50)
    password.pack()
    password.bind("<Return>", lambda funct1: confirm.focus())

    tk.Label(frame2,text="Re-enter your Password to Confirm", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    confirm = tk.Entry(frame2,width=50)
    confirm.pack()
    confirm.bind("<Return>", (lambda event: add_User(my_account.account_id,name.get(),username.get(),password.get(),confirm.get())))

    #button to cancel
    tk.Button(frame2, text="Cancel", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame1()).pack(pady=20)

#Checks for empty inputs and updates the new website and its login informations
def add_User(account_id,name,username,password,confirm):
    if name == "" or username == "" or password == "" or confirm == "":
        messagebox.showinfo(title="Listen Up", message="no empty fields allowed")
    elif password != confirm:
        messagebox.showinfo(title="Listen Up", message="Your password doesn't match!")
    else:
        #Add new user to the database
        cursor.execute(f'INSERT INTO app(account_id, app_user, app_pass, account_name) VALUES ({account_id}, "{username}", "{password}", "{name}")')
        connection.commit()
        messagebox.showinfo(title="SKS Account Created", message="Your SKS account was successfully created. Go login!")
        load_frame1()

frame1 = tk.Frame(root, width=640, height=600, bg="#002435")
frame2 = tk.Frame(root, bg="#002435")
#frame3 = tk.Frame(root, bg="black")


for frame in (frame1,frame2):
    frame.grid(row=0, column=0, sticky = "nesw")
opening()
load_frame1()




# run app
root.mainloop()
