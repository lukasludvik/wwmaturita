from tkinter import *
import customtkinter as ctk

#setting default appearance to light
ctk.set_appearance_mode('light')

#change appearance from dark to light and back using a button
def changeApp():
    if ctk.AppearanceModeTracker.appearance_mode == 1:
        ctk.set_appearance_mode('light')
    else:
        ctk.set_appearance_mode('dark')
        
#main class to show the window and manage it
class MainFrame(ctk.CTk):
    
    #function to open a new window
    def open_window(self):
        self.win = ctk.CTkToplevel(self)
        self.win.geometry('1920x1080+0+0')
        self.win.title("WealthWise")
        
        self.buttonChange = ctk.CTkButton(self.win,  
                            text='Change appearance',
                            command= lambda: changeApp(),
                            corner_radius= 0) 
        self.buttonChange.place(relx = 0, rely = 0.9)
        
        self.buttonIncome = ctk.CTkButton(self.win, text="Přidat příjem") 
        self.buttonIncome.place(relx = 0, rely = 0)
        self.buttonExp = ctk.CTkButton(self.win, text= "Přidat výdaj")
        self.buttonExp.place(relx = 0, rely = 0.1)

    #function to handle login information
    def handle_login(self, username, password):
        if username.get() == "admin" and password.get() == "pass":
            self.open_window()
        else:
            error_label = ctk.CTkLabel(self, text="Invalid login credentials", font=("Arial", 16))
            error_label.place(relx=0.5, rely=0.95, anchor="center")
    
    #initialize function for the class
    def __init__(self):
        super().__init__()
        self.title(' WealthWise')
        self.geometry('1920x1080+0+0')
        
        bg_img = PhotoImage(file="photo/logo.png")
        self.logo = ctk.CTkLabel(self, image=bg_img, text= "")
        self.logo.place(relx = 0.3, rely = 0.1)

        # Create a username input field
        self.username_label = ctk.CTkLabel(self, text="Username", font=("Arial", 20))
        self.username_label.place(relx=0.45, rely=0.4, anchor="e")
        self.username_entry = ctk.CTkEntry(self, font=("Arial", 20))
        self.username_entry.place(relx=0.5, rely=0.4, anchor="w")

        # Create a password input field
        self.password_label = ctk.CTkLabel(self, text="Password", font=("Arial", 20))
        self.password_label.place(relx=0.45, rely=0.5, anchor="e")
        self.password_entry = ctk.CTkEntry(self, font=("Arial", 20), show="*")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="w")

        # Create a login button
        self.login_button = ctk.CTkButton(self, text="Login", font=("Arial", 25), command = lambda: self.handle_login(self.username_entry, self.password_entry))
        self.login_button.place(relx=0.5, rely=0.7, anchor="center")

app = MainFrame()
app.mainloop()