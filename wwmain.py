from tkinter import *
import customtkinter as ctk
import datetype

#setting default appearance to light
ctk.set_appearance_mode('light')

#change appearance from dark to light and back using a button
def changeApp():
    if ctk.AppearanceModeTracker.appearance_mode == 1:
        ctk.set_appearance_mode('light')
    else:
        ctk.set_appearance_mode('dark')
        
class Money():
    def __init__(self, value, day, month, year, category):
        self.value = value
        self.day = day
        self.month = month
        self.year = year
        self.category = category
        
    def get_money_info(self):
        print(self.value, self.day, self.month, self.year, self.category)

#main class to show the window and manage it
class MainFrame(ctk.CTk):
    
    #initialize function for the class
    def __init__(self):
        self.income = []
        self.expen = []
        self.categ = []
        
        super().__init__()
        
        self.title(' WealthWise')
        self.geometry('1920x1080+0+0')
        
        img = PhotoImage(file="photo/logo.png")
        self.logo = ctk.CTkLabel(self, image=img, text= "")
        self.logo.place(relx = 0.3, rely = 0.1)

        # Create a username input field
        self.user_label = ctk.CTkLabel(self, text="Jméno:", font=("Arial", 20))
        self.user_label.place(relx=0.45, rely=0.4, anchor="e")
        self.user_entry = ctk.CTkEntry(self, font=("Arial", 20))
        self.user_entry.place(relx=0.5, rely=0.4, anchor="w")

        # Create a password input field
        self.pass_label = ctk.CTkLabel(self, text="Heslo:", font=("Arial", 20))
        self.pass_label.place(relx=0.45, rely=0.5, anchor="e")
        self.pass_entry = ctk.CTkEntry(self, font=("Arial", 20), show="*")
        self.pass_entry.place(relx=0.5, rely=0.5, anchor="w")

        # Create a login button
        self.login_button = ctk.CTkButton(self, text="Přihlásit", font=("Arial", 25), command = lambda: self.handle_login(self.user_entry, self.pass_entry))
        self.login_button.place(relx=0.5, rely=0.7, anchor="center")
    
    #function to handle login information
    def handle_login(self, username, password):
        if username.get() == "admin" and password.get() == "pass":
            self.user = 'admin'
            self.withdraw()
            self.open_window()
            
        else:
            error = ctk.CTkLabel(self, text="Jméno nebo heslo neexistuje", font=("Arial", 16), bg_color="red", text_color="white")
            error.place(relx=0.5, rely=0.9, anchor="center")
    
    #function to open a new window
    def open_window(self):
        win = ctk.CTkToplevel(self)
        win.geometry('1920x1080+0+0')
        win.title("WealthWise")
        
        buttonChange = ctk.CTkButton(win,  
                            text='Změnit vzhled',
                            command= lambda: changeApp(),
                            corner_radius= 0) 
        buttonChange.place(relx = 0, rely = 0.9)
        
        buttonIncome = ctk.CTkButton(win, text="Přidat příjem", command= lambda: self.add_income("příjem")) 
        buttonIncome.place(relx = 0, rely = 0)
        buttonExp = ctk.CTkButton(win, text= "Přidat výdaj", command= lambda: self.add_income("výdaj"))
        buttonExp.place(relx = 0, rely = 0.05)
        
        out_label = ctk.CTkLabel(win, text="Přihlášen: " + self.user, font=("Arial", 15))
        out_label.place(relx=0.92, rely=0.05, anchor="center")
        
        buttonLogOut = ctk.CTkButton(win, text="Odhlásit se", command= lambda: self.logout(win)) 
        buttonLogOut.place(relx = 0.87, rely = 0.1)
        
    def logout(self, win):
        self.user = None
        self.deiconify()
        win.withdraw()
        
    def add_income(self, type):
        window = ctk.CTkToplevel(self)
        window.geometry("400x300")
        window.title("Přidat " + type)
        
        textVal = ctk.CTkEntry(window, font=("Arial", 15), width=140, height=10)
        val_label = ctk.CTkLabel(window, text="Hodnota", font=("Arial", 15))
        textDay = ctk.CTkEntry(window, font=("Arial", 15), width=30, height=10)
        day_label = ctk.CTkLabel(window, text="Den / Měsíc / Rok", font=("Arial", 15))
        textMon = ctk.CTkEntry(window, font=("Arial", 15),width=30, height=10)
        textYea = ctk.CTkEntry(window, font=("Arial", 15), width=60, height=10)
        textCat = ctk.CTkEntry(window, font=("Arial", 15), width=140, height=10)
        cat_label = ctk.CTkLabel(window, text="Kategorie", font=("Arial", 15))
        
        textVal.place(relx = 0.55, rely = 0.1)
        textDay.place(relx = 0.55, rely = 0.2)
        textMon.place(relx = 0.65, rely = 0.2)
        textYea.place(relx = 0.75, rely = 0.2)
        textCat.place(relx = 0.55, rely = 0.3)
        
        val_label.place(relx = 0.2, rely = 0.1)
        day_label.place(relx = 0.2, rely = 0.2)
        cat_label.place(relx = 0.2, rely = 0.3)
        
        button = ctk.CTkButton(window, text="Submit", command= lambda: self.submit(window, type, textVal.get(), textDay.get(), textMon.get(), textYea.get(), textCat.get()))
        button.place(relx = 0.35, rely = 0.5)
        
    def submit(self, win, type, val, day, mon, yea, cat):
        try:
            val = int(val)
            day = int(day)
            mon = int(mon)
            yea = int(yea)
        except:
            error = ctk.CTkLabel(self, text="Invalid information", font=("Arial", 10), bg_color="red", text_color="white")
            error.place(relx = 0.5, rely = 0.9)
        else:
            if ((mon == 2 and day <= 28) or (mon in [4, 6, 9, 11] and day <= 30) or (mon in [1, 3, 5, 7, 8, 10, 12] and day <= 31)) and val > 0:
                if type == "příjem":
                    self.income.append(Money(val, day, mon, yea, cat))
                    print(self.income)
                    win.destroy()
                else:
                    self.expen.append(Money(val, day, mon, yea, cat))
                    print(self.expen)
                    win.destroy()

app = MainFrame()
app.mainloop()