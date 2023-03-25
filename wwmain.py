import customtkinter as ctk
from tkinter import * 
from PIL import Image
import hashlib
import os

#My files
import users.accountMaker as ac
import finder as find

# Change appearance from dark to light and back using a button
ctk.set_appearance_mode('light')
def changeApp():
    if ctk.AppearanceModeTracker.appearance_mode == 1:
        ctk.set_appearance_mode('light')
    else:
        ctk.set_appearance_mode('dark')
        
class Money():
    def __init__(self, type, value, day, month, year, category):
        self.type = type
        self.value = value
        self.day = day
        self.month = month
        self.year = year
        self.category = category
        
    def save_money_info(self, user):
        try:
            path = os.path.join("users", user, user + ".txt")
            file = open(path, "a")
            info = self.type + "$" + str(self.value).strip(" ") + "$" + str(self.day) + "$" + str(self.month) + "$" + str(self.year) + "$" + str(self.category + "\n")
            file.write(info)
            
        except:
            print("error")

class MainFrame(ctk.CTk):
    
    # Initialize function for the class
    def __init__(self):
        self.users = {}
        self.categ = []
        self.balance = 0
        self.inc = []
        self.exp = []
        self.pageNumInc = 1
        self.pageNumExp = 1
        
        super().__init__()
        self.load_users()
        
        self.title(' WealthWise')
        self.geometry('1920x1080+0+0')
        
        try:
            img = ctk.CTkImage(light_image= Image.open("photo/logo.png"), size=(500,100))
        except:
            print("Missing .png file or photo file")
        logo = ctk.CTkLabel(self, image=img, text= "")
        logo.place(relx = 0.32, rely = 0.1)

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
        self.login_button = ctk.CTkButton(self, text="Přihlásit", font=("Arial", 25), command = lambda: self.handle_login(self.user_entry.get(), self.pass_entry.get()))
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")
        
        # Create an account button
        self.login_button = ctk.CTkButton(self, text="Vytvořit účet", font=("Arial", 20), fg_color = "black", command = lambda: self.register())
        self.login_button.place(relx=0.5, rely=0.65, anchor="center")
        
        # Error label in case of failure
        self.error = ctk.CTkLabel(self, text="Jméno nebo heslo neexistuje", font=("Arial", 16), text_color="white")
    
    # Function to register a new account
    def register(self):
        reg = ctk.CTkToplevel()
        reg.geometry("400x400")
        reg.title("Zaregistrovat se")
        
        user_label = ctk.CTkLabel(reg, text="Jméno:", font=("Arial", 20))
        user_label.place(relx=0.3, rely=0.3, anchor="e")
        user_entry = ctk.CTkEntry(reg, font=("Arial", 15))
        user_entry.place(relx=0.4, rely=0.3, anchor="w")
        
        pass_label = ctk.CTkLabel(reg, text="Heslo:", font=("Arial", 20))
        pass_label.place(relx=0.3, rely=0.4, anchor="e")
        pass_entry = ctk.CTkEntry(reg, font=("Arial", 12), show='*')
        pass_entry.place(relx=0.4, rely=0.4, anchor="w")
        
        submit_button = ctk.CTkButton(reg, text="Vytvořit účet", font=("Arial", 20),command = lambda: self.handle_register(reg, user_entry.get(), pass_entry.get(), error))
        submit_button.place(relx=0.5, rely=0.6, anchor="center") 
        
        error = ctk.CTkLabel(reg, text="Jméno již existuje", bg_color="red", text_color="white" )     
        
    def load_users(self):
        try:
            file = open("users\password.txt")
            self.users={}
            for i in file:
                self.users.update({i.strip("\n") : file.readline().strip("\n")})
            file.close()
        except:
            print("Loading users failed")
    
    def handle_register(self, reg, user, passw, error):
        if user in self.users: 
            error.place(relx = 0.4, rely = 0.7)
        elif user.strip(" ") != "":
            try:
                file = open("users\password.txt", "a")
                file.write(user + "\n") #Writes the username in the file
                
                salt = os.urandom(5).hex() #Generates a salt
                hasher = hashlib.sha256() #Create a new hasher object using the sha256 algorithm
                hasher.update(salt.encode() + passw.encode()) #Add the salt and password to the hasher object
                hashed_passw = hasher.hexdigest() #Get the hash value as a string
                
                file.write(salt + "$" + hashed_passw + "\n") #Saves the password in a file
                
                ac.AccountMaker(user)
                
                reg.destroy()
                file.close()
                
                self.load_users() #Reloads the users from the file
            except:
                print("Saving account failed")
    
    # Function to handle logging in
    def handle_login(self, username, password):
        if username in self.users:
            
            user_hash = self.users[username]
            salt, hash = user_hash.split("$")

            hasher = hashlib.sha256()
            hasher.update(salt.encode() + password.encode())
            user_hash = hasher.hexdigest()
            
            if user_hash == hash:
                self.user = username
                
                self.open_window()
                
                self.user_entry.delete(0, ctk.END)
                self.pass_entry.delete(0, ctk.END)
                self.error.place_forget()
                
                self.withdraw()
                
            
        else:
            self.error.place(relx=0.5, rely=0.9, anchor="center")
    
    # Function to handle logging out
    def logout(self, win):
        self.user = None
        self.deiconify()
        win.withdraw()
        
    # Function to open the main window
    def open_window(self):
        self.balance = 0
        win = ctk.CTkToplevel(self)
        win.geometry('1920x1080+0+0')
        win.title("WealthWise")
        
        moneyAll = ctk.CTkLabel(win, text= "Zůstatek:  " + str(self.balance), font=("Arial", 50), anchor="center")
        moneyAll.place(relx=0.33, rely = 0.15)
        
        buttonChange = ctk.CTkButton(win,  
                            text='Změnit vzhled',
                            command= lambda: changeApp(),
                            ) 
        buttonChange.place(relx = 0, rely = 0.9)
        
        outLabel = ctk.CTkLabel(win, text="Přihlášen: " + self.user, font=("Arial", 15))
        outLabel.place(relx=0.07, rely=0.06, anchor="center")
        
        buttonLogOut = ctk.CTkButton(win, text="Odhlásit se", command= lambda: self.logout(win))
        buttonLogOut.place(relx = 0.02, rely = 0.08)
        
        tabview = ctk.CTkTabview(win)
        tabview.place(relx = 0.33, rely=0.3, relwidth = 0.33, relheight = 0.5)

        tabview.add("Příjmy")
        tabview.add("Výdaje")
        
        ctk.CTkButton(tabview.tab("Příjmy"), text = "-", command= lambda: self.changePageNum("min", win, "inc")).place(relwidth = 0.05, relheight = 0.05, relx = 0.35, rely = 0.75)
        ctk.CTkButton(tabview.tab("Příjmy"), text = "+", command= lambda: self.changePageNum("add", win, "inc")).place(relwidth = 0.05, relheight = 0.05, relx = 0.65, rely = 0.75)
        ctk.CTkButton(tabview.tab("Výdaje"), text = "-", command= lambda: self.changePageNum("min", win, "exp")).place(relwidth = 0.05, relheight = 0.05, relx = 0.35, rely = 0.75)
        ctk.CTkButton(tabview.tab("Výdaje"), text = "+", command= lambda: self.changePageNum("add", win, "exp")).place(relwidth = 0.05, relheight = 0.05, relx = 0.65, rely = 0.75)

        incNum = ctk.CTkLabel(tabview.tab("Příjmy"), text = str(self.pageNumInc))
        incNum.place(relheight = 0.1, relx = 0.5, rely = 0.73)
        expNum = ctk.CTkLabel(tabview.tab("Výdaje"), text = str(self.pageNumExp))
        expNum.place(relheight = 0.1, relx = 0.5, rely = 0.73)
        
        labels = [[ctk.CTkLabel(tabview.tab("Příjmy"), text = " ") for i in range(5)], [ctk.CTkLabel(tabview.tab("Výdaje"), text = " ") for i in range(5)]]
        buttons = [[ctk.CTkButton(tabview.tab("Příjmy"), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(50, 50)), text = "") for i in range(5)], [ctk.CTkButton(tabview.tab("Výdaje"), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(50, 50)), text = "") for i in range(5)]]
        
        typ = "inc"
        for i in range(2):
            x = 0.11
            for j in range(5):
                buttons[i][j].place(width = 50, height = 50, relx = 0.9, rely = x)
                buttons[i][j].configure(command= lambda: self.deleteMoney(j + 1, typ))
                x += 0.11
            typ = "exp"

        for i in range(2):
            x = 0.11
            for k in labels[i]:
                k.place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = x)
                x += 0.11
        
        self.update_label(tabview, moneyAll, labels)
        
    def deleteMoney(self, pos, type):
        
        print(self.inc)
        print((self.pageNumInc - 1) * 5 + pos)
        
        finder = find.FileHandler(self.user)
        if type == "inc":
            finder.deleteLine(self.inc[(self.pageNumInc - 1) * 5 + pos])
        else:
            finder.deleteLine(self.exp[(self.pageNumExp - 1) * 5 + pos])
        
    def changePageNum(self, operation, win, type):
        
        if type == "inc":
            if self.pageNumInc > 0:
                if operation == "add":
                    self.pageNumInc += 1
                else:
                    self.pageNumInc -= 1
        else:
            if self.pageNumExp > 0:
                if operation == "add":
                    self.pageNumExp += 1
                else:
                    self.pageNumExp -= 1
                
        win.withdraw()
        self.open_window()
                
    def update_label(self, tabview, moneyAll, labels):
        #Add income
        ctk.CTkButton(tabview.tab("Příjmy"), text="Přidat příjem", command= lambda: self.add_income("příjem", tabview, moneyAll)).place(relx = 0.35, rely = 0.9)
        #Add expense
        ctk.CTkButton(tabview.tab("Výdaje"), text= "Přidat výdaj", command= lambda: self.add_income("výdaj", tabview, moneyAll)).place(relx = 0.35, rely = 0.9)
        
        #Add labels
        ctk.CTkLabel(tabview.tab("Příjmy"), text = "        ".join([" Hodnota", "Den", " Měsíc", "Rok", "Kategorie"])).place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0)
        ctk.CTkLabel(tabview.tab("Výdaje"), text = "        ".join([" Hodnota", "Den", " Měsíc", "Rok", "Kategorie"])).place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0)
        
        self.update_money(self.user, self.inc, "inc", self.pageNumInc, moneyAll, labels, 0)
        self.update_money(self.user, self.exp, "exp", self.pageNumExp, moneyAll, labels, 1)
        
    def update_money(self, user, list, type, pageNum, moneyAll, labels, x):

        list.clear()
        info = []
        
        path = os.path.join("users", user, user + ".txt")
        with open(path) as file:
            for i in file:
                if i.startswith(type):
                    typ, val, day, mon, yea, cat = i.split("$")
                    info.append([typ, val, day, mon, yea, cat])
                else:
                    continue
                
                if type == "inc":
                    self.inc.append(i.strip("\n"))
                    self.balance += int(val)
                else:
                    self.exp.append(i.strip("\n"))
                    self.balance -= int(val)
            
            print(self.inc)
            print(self.exp)
            for i in range(5):
                try:
                    statement = ""
                    filerange = i + ((pageNum - 1) * 5)
                    for j in range(1, 6):
                        statement = statement + "         " + info[filerange][j]
                    labels[x][i].configure(text = statement)           
                    moneyAll.configure(text="Zůstatek:     " + str(self.balance))
                except Exception as exception:
                    print(exception)
                    break                
        
    # Function to handle income or expense addition
    def add_income(self, type, tabview, moneyAll):
        window = ctk.CTkToplevel(self)
        window.geometry("400x300")
        window.title("Přidat " + type)
        
        textVal = ctk.CTkEntry(window, font=("Arial", 15), width=140, height=10)
        val_label = ctk.CTkLabel(window, text="Hodnota", font=("Arial", 15))
        textDay = ctk.CTkEntry(window, font=("Arial", 15), width=30, height=10)
        day_label = ctk.CTkLabel(window, text="Den / Měsíc / Rok", font=("Arial", 15))
        textMon = ctk.CTkEntry(window, font=("Arial", 15),width=30, height=10)
        textYea = ctk.CTkEntry(window, font=("Arial", 15), width=60, height=10, placeholder_text= "2000+")
        textCat = ctk.CTkEntry(window, font=("Arial", 15), width=140, height=10, placeholder_text="max 5 char")
        cat_label = ctk.CTkLabel(window, text="Kategorie", font=("Arial", 15))

        textVal.place(relx = 0.55, rely = 0.1)
        textDay.place(relx = 0.55, rely = 0.2)
        textMon.place(relx = 0.65, rely = 0.2)
        textYea.place(relx = 0.75, rely = 0.2)
        textCat.place(relx = 0.55, rely = 0.3)
        
        val_label.place(relx = 0.2, rely = 0.1)
        day_label.place(relx = 0.2, rely = 0.2)
        cat_label.place(relx = 0.2, rely = 0.3)
        
        button = ctk.CTkButton(window, text="Submit", command= lambda: self.submit(window, type, textVal.get(), textDay.get(), textMon.get(), textYea.get(), textCat.get(), tabview, moneyAll))
        button.place(relx = 0.35, rely = 0.5)
        
    def deleteButton(self, butNum):
        find.FileHandler()
        
    # Function to handle submitting info about income or expense
    def submit(self, win, type, val, day, mon, yea, cat, tabview, moneyAll):
        try:
            val = int(val)
            day = int(day)
            mon = int(mon)
            yea = int(yea)
        except:
            error = ctk.CTkLabel(self, text="Invalid information", font=("Arial", 10), bg_color="red", text_color="white")
            error.place(relx = 0.5, rely = 0.9)
        else:    
            if (   
                    ((mon == 2 and day <= 28 and yea % 4 != 0) or (mon == 2 and day <= 29 and yea % 4 == 0)) or 
                    (mon in [4, 6, 9, 11] and day <= 30) or 
                    (mon in [1, 3, 5, 7, 8, 10, 12] and day <= 31)
                ) and val > 0 and len(cat) <= 5 and yea >= 2000:
                
                self.balance = 0
                
                if type == "příjem":
                    Money("inc", val, day, mon, yea, cat).save_money_info(self.user)
                else:
                    Money("exp", val, day, mon, yea, cat).save_money_info(self.user)
                    
                self.update_money(self.user, "inc", 1, tabview.tab("Příjmy"), moneyAll)
                self.update_money(self.user, "exp", 1, tabview.tab("Výdaje"), moneyAll)
                self.categ.append(cat.lower())
                win.destroy()

app = MainFrame()


if __name__ == "__main__":
    app.mainloop()