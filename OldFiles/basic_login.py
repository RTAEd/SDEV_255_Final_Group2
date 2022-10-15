from tkinter import *
import sqlite3


# Add logic functions 
def login():
    #getting form data
    uname=username.get()
    pwd=password.get()


    if uname=='' or pwd=='':
        message.set("A field is empty. Please fill in all information.")
    else:

      conn = sqlite3.connect('pw_manager.db')
      cursor = conn.execute(f'SELECT * from app where app_user="{uname}" and app_pass="{pwd}"')
      
      if cursor.fetchone():
       message.set("Login success")
      else:
       message.set("Wrong username or password!!!")

# Form Functions
def Loginform():
    global login_screen

    login_screen = Tk()
    login_screen.title("Password Manager")
    login_screen.geometry("350x250")
    login_screen["bg"]="#1C2833"

    #declaring variable
    global message
    global username
    global password

    username = StringVar()
    password = StringVar()
    message = StringVar()
    

# def openNewWindow():

#     # Toplevel object which will
#     # be treated as a new window
#     newWindow = Toplevel(login_screen)
 
#     # sets the title of the
#     # Toplevel widget
#     newWindow.title("New Window")
 
#     # sets the geometry of toplevel
#     newWindow.geometry("200x200")
 
#     # A Label widget to show in toplevel
#     Label(newWindow,text ="This is a new window").place(x=50,y=50)



# Formatting onscreen widgets for login-screen
    Label(login_screen, text="Username * ",bg="#1C2833",fg="white",font=("Arial",12,"bold")).place(x=20,y=40)
    Entry(login_screen, textvariable=username,bg="#1C2833",fg="white",font=("Arial",12,"bold")).place(x=120,y=42)

    Label(login_screen, text="Password * ",bg="#1C2833",fg="white",font=("Arial",12,"bold")).place(x=20,y=80)
    Entry(login_screen, textvariable=password ,show="*",bg="#1C2833",fg="white",font=("Arial",12,"bold")).place(x=120,y=82)

    Label(login_screen, text="",textvariable=message,bg="#1C2833",fg="white",font=("Arial",12,"bold")).place(x=95,y=120)

    Button(login_screen, text="Login", width=10, height=1, command=login, bg="#0E6655",fg="white",font=("Arial",12,"bold")).place(x=125,y=170)
    # Button(login_screen, text="Login", width=10, height=1, command=lambda:[login, openNewWindow], bg="#0E6655",fg="white",font=("Arial",12,"bold")).place(x=125,y=170)
    # Button(login_screen, text="Login", width=10, height=1, command=openNewWindow, bg="#0E6655",fg="white",font=("Arial",12,"bold")).place(x=125,y=170)
    


    login_screen.mainloop()

#calling function Loginform
Loginform()

