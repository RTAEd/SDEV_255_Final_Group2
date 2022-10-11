import tkinter as tk
from PIL import ImageTk, Image, ImageSequence
import sqlite3
import time
from tkinter import messagebox

#Once I figure things out, I will move stuff around


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


def fetch_db(username_input, password_input):
    connection = sqlite3.connect("data/pw_manager.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM app WHERE app_user = '" + username_input + "' AND app_pass = '" + password_input + "'")
    #check number of rows
    empty = cursor.fetchone()
    #check number of attempts. No attempts = exit program
    if empty is None:
        print("ouch")
    else:

        #fetch the account id and name
        cursor.execute("SELECT * FROM app WHERE app_user = '" + username_input + "' AND app_pass = '" + password_input + "'")
        ans = cursor.fetchall()
        for i in ans:
            my_account.account_id = i[0]
            my_account.account_name = i[3]
        print("Welcome, " + my_account.account_name) 
    connection.close()


#initiallize app
root = tk.Tk()
#the option for resizing the window will cause issues, so I will disable it for now.
root.resizable(False, False) 
root.title("Secret Key Shield")
root.eval("tk::PlaceWindow . center")

bg_color = "#002435"

def load_frame1():
    frame1.pack_propagate(False)
    #fram1 widget
    logo_img = ImageTk.PhotoImage(file = "assets/sks_logo.png")
    logo_widget = tk.Label(frame1, image = logo_img, bg = "#002435")
    logo_widget.image = logo_img
    logo_widget.pack()

    #tk.Label(frame1, text = "Login", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    # email/username label
    username = tk.Label(frame1,text="USERNAME: ", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    #username.grid(row=1, column=0)


    # username_input box
    username_input = tk.Entry(frame1,width=35)
    username_input.pack()
    username_input.focus()
    username_input.bind("<Return>", lambda funct1: password_input.focus())
    
    # password: label
    password = tk.Label(frame1,text="PASSWORD: ", bg = bg_color, fg = "white", font=("TkMenuFont", 14) ).pack()
    

    # password_input box
    password_input = tk.Entry(frame1,width=35)
    password_input.pack()
    password_input.bind("<Return>", (lambda event: fetch_db(username_input.get(), password_input.get())))
   

    #button (need to add frame3)
    tk.Button(frame1, text="New User", font = ("TkHeadingFont", 10), bg="#28393a", fg="white", cursor = "hand2", activebackground = "#badee2", activeforeground = "black", command = lambda:load_frame2()).pack(pady=20)


def load_frame2():
    fetch_db()


    


frame1 = tk.Frame(root, width=640, height=600, bg="#002435")
frame2 = tk.Frame(root, bg="#002435")


for frame in (frame1,frame2):
    frame.grid(row=0, column=0)
opening()
load_frame1()




# run app
root.mainloop()