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

    #button (need to add frame0)
    tk.Button(frame1, text="New User", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:fetch_db("dtran", "manaGer%360!")).pack(pady=20)

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
    tk.Button(frame2, text="Add Login Information", font = ("TkHeadingFont", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame1()).pack(pady=2, fill = "both")
    tk.Button(frame2, text="Logout", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame1()).pack(pady=50)


#Vwebsites screen
def load_frame3():
    clearscreen(frame2)
    frame2.tkraise()
    logo_img = ImageTk.PhotoImage(file = "assets/sks_logo.png")
    logo_widget = tk.Label(frame2, image = logo_img, bg = "#002435")
    logo_widget.image = logo_img
    logo_widget.pack()
    tk.Label(frame2, text = "My Websites", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    tk.Label(frame2, text = "Choose a website to view:\n", bg = bg_color, fg = "white", font=("TkMenuFont", 10) ).pack()
    list()
    #for i in websites:
        #tk.Button(frame2, text=i, font = ("TkHeadingFont", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame1()).pack(pady=2, fill = "both")
    tk.Button(frame2, text="Return", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame2()).pack(pady=50)

#List all websites associated with the user    
def list():
    count = 1
    cursor.execute(f"SELECT * FROM website WHERE account_id = {my_account.account_id}")
    ans = cursor.fetchall()
    for i in ans:
        tk.Button(frame2, text=f"{i[2]}", font = ("TkHeadingFont", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:viewInfo(i[0],i[1])).pack(pady=2, fill = "both")
        #count+=1
    row = len(ans)
    #For newly created user, there are no website. So it will return to the welcome menu
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
    cursor.execute(f"SELECT * FROM login WHERE web_id = {info.web_id}")
    ans = cursor.fetchall()
    for i in ans:
      info.log_id = i[0]
      info.email = i[1]
      info.username = i[2]
      info.pw = i[3]
    tk.Label(frame2, text = f"Login Information - {info.site_name}", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    tk.Label(frame2, text = f"\n[USERNAME: {info.username}]\n[PASSWORD: {info.pw}] \n[Associated Email: {info.email}]\n", bg = "black", fg = "white", font=("TkMenuFont", 12) ).pack(pady =5, fill = "both")
    tk.Button(frame2, text="Update Password", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:updatePassword()).pack(pady=20)
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
    
    # password: label
    password = tk.Label(frame2,text="New Password: ", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    
    # password_input box
    password_input = tk.Entry(frame2,width=35)
    password_input.pack()
    password_input.focus()
    password_input.bind("<Return>", (lambda event: change(password_input.get())))

    #button to generate new password
    tk.Button(frame2, text="Generate", font = ("Parisienne Small", 30), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:viewInfo(info.web_id, info.site_name)).pack(pady=20)
    
    tk.Button(frame2, text="Cancel Change", font = ("undefeated", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:viewInfo(info.web_id, info.site_name)).pack(pady=2)

#Someone do this function: checks the inputs if it's not 
def change(new_password):
    if new_password == "":
        messagebox.showinfo(title="Listen Up", message="no empty fields allowed")

    else:

        print(info.log_id)
        cursor.execute(f'''UPDATE login SET password = "{new_password}" WHERE log_id = "{info.log_id}";''')
        connection.commit()
        load_frame2()





frame1 = tk.Frame(root, width=640, height=600, bg="#002435")
frame2 = tk.Frame(root, bg="#002435")
#frame3 = tk.Frame(root, bg="black")


for frame in (frame1,frame2):
    frame.grid(row=0, column=0, sticky = "nesw")
opening()
load_frame1()




# run app
root.mainloop()
