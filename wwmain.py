from tkinter import *
import customtkinter as ctk

#setting default appearance to dark
ctk.set_appearance_mode('dark')

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
        new_window = Toplevel(self)
        new_window.title("Welcome")

    #function to handle login information
    def handle_login(self, username, password):
        if username.get() == "admin" and password.get() == "password":
            self.open_window()
            self.destroy()
        else:
            error_label = Label(self, text="Invalid login credentials", font=("Arial", 16), bg="#ffffff", fg="#ff0000")
            error_label.place(relx=0.5, rely=0.9, anchor="center")
    
    #initialize function for the class
    def __init__(self):
        super().__init__()
        self.title(' WealthWise')
        self.geometry('1920x1080+0+0')
        
        
        self.buttonChange = ctk.CTkButton(self,  
                            text='Change appearance',
                            command= lambda: changeApp(app),
                            corner_radius= 0) 
        self.buttonChange.place(relx = 0, rely = 0.9)
        
        background_image = PhotoImage(file="photo/logo.png")
        background_label = Label(self, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a username input field
        self.username_label = Label(self, text="Username", font=("Arial", 16), bg="#ffffff", fg="#000000")
        self.username_label.place(relx=0.45, rely=0.4, anchor="e")
        self.username_entry = Entry(self, font=("Arial", 16))
        self.username_entry.place(relx=0.5, rely=0.4, anchor="w")

        # Create a password input field
        self.password_label = Label(self, text="Password", font=("Arial", 16), bg="#ffffff", fg="#000000")
        self.password_label.place(relx=0.45, rely=0.5, anchor="e")
        self.password_entry = Entry(self, font=("Arial", 16), show="*")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="w")

        # Create a login button
        self.login_button = Button(self, text="Login", font=("Arial", 16), bg="#000000", fg="#ffffff", command = lambda: self.handle_login(self.username_entry, self.password_entry))
        self.login_button.place(relx=0.5, rely=0.7, anchor="center")

app = MainFrame()
app.mainloop()




