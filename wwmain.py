import customtkinter as ctk
from tkinter import * 
from PIL import Image
import hashlib
import os

#My files
import users.accountMaker as ac
import fileHandler as filehandle
import sorter as sorter
import filter as filter

# Change appearance from dark to light and back
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
            file.write(info = self.type + "$" + str(self.value).strip(" ") + "$" + str(self.day) + "$" + str(self.month) + "$" + str(self.year) + "$" + str(self.category + "\n"))
            
        except:
            print("error")

class MainFrame(ctk.CTk):
    
    # Initialize function for the class
    def __init__(self):
        self.users = {}
        self.template = [[], [], [], []]
        self.info = [[],[]] #['inc', 4000, 3, 8, 90, 'bdbc']
        self.categ = []
        self.balance = 0
        self.money = [[], []] #inc$700$3$8$90$db
        self.pageNum = [1, 1]
        self.maxPageNum = [1, 1]
        self.changeConstant = "Příjmy"
        
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
        
        error = ctk.CTkLabel(reg, text="Jméno již existuje", bg_color="red", text_color="white")     
        
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
            self.error.place(relx=0.5, rely=0.8, anchor="center")
    
    # Function to handle logging out
    def logout(self, win):
        self.user = None
        self.deiconify()
        win.withdraw()
        
    # Function to open the main window
    def open_window(self):
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

        tabview.set(self.changeConstant)
        
        ctk.CTkButton(tabview.tab("Příjmy"), text = "-", command= lambda: self.change_page_num("min", win, "inc")).place(relwidth = 0.05, relheight = 0.05, relx = 0.35, rely = 0.75)
        ctk.CTkButton(tabview.tab("Příjmy"), text = "+", command= lambda: self.change_page_num("add", win, "inc")).place(relwidth = 0.05, relheight = 0.05, relx = 0.65, rely = 0.75)
        ctk.CTkButton(tabview.tab("Výdaje"), text = "-", command= lambda: self.change_page_num("min", win, "exp")).place(relwidth = 0.05, relheight = 0.05, relx = 0.35, rely = 0.75)
        ctk.CTkButton(tabview.tab("Výdaje"), text = "+", command= lambda: self.change_page_num("add", win, "exp")).place(relwidth = 0.05, relheight = 0.05, relx = 0.65, rely = 0.75)

        incNum = ctk.CTkLabel(tabview.tab("Příjmy"), text = str(self.pageNum[0]))
        incNum.place(relheight = 0.1, relx = 0.5, rely = 0.73)
        expNum = ctk.CTkLabel(tabview.tab("Výdaje"), text = str(self.pageNum[1]))
        expNum.place(relheight = 0.1, relx = 0.5, rely = 0.73)
        
        #Creating labels to show preffered type
        labels = [[ctk.CTkLabel(tabview.tab("Příjmy"), text = " ") for m in range(5)], [ctk.CTkLabel(tabview.tab("Výdaje"), text = " ") for k in range(5)]]
        
        # Placing the labels
        for x in range(2):
            y = 0.11
            for k in labels[x]:
                k.place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = y)
                y += 0.11
        
        #Creating delete buttons
        try:
            incButton1 = ctk.CTkButton(tabview.tab("Příjmy"), width = 20, height = 20, command = lambda: self.delete_money(1, "inc", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            incButton1.place(relx = 0.9, rely = 0.11)
            incButton2 = ctk.CTkButton(tabview.tab("Příjmy"), width = 20, height = 20, command = lambda: self.delete_money(2, "inc", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            incButton2.place( relx = 0.9, rely = 0.22)
            incButton3 = ctk.CTkButton(tabview.tab("Příjmy"), width = 20, height = 20, command = lambda: self.delete_money(3, "inc", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            incButton3.place( relx = 0.9, rely = 0.33)
            incButton4 = ctk.CTkButton(tabview.tab("Příjmy"), width = 20, height = 20, command = lambda: self.delete_money(4, "inc", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            incButton4.place( relx = 0.9, rely = 0.44)
            incButton5 = ctk.CTkButton(tabview.tab("Příjmy"), width = 20, height = 20, command = lambda: self.delete_money(5, "inc", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            incButton5.place( relx = 0.9, rely = 0.55)
    
            expButton1 = ctk.CTkButton(tabview.tab("Výdaje"), width = 20, height = 20, command = lambda: self.delete_money(1, "exp", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            expButton1.place( relx = 0.9, rely = 0.11)
            expButton2 = ctk.CTkButton(tabview.tab("Výdaje"), width = 20, height = 20, command = lambda: self.delete_money(2, "exp", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            expButton2.place( relx = 0.9, rely = 0.22)
            expButton3 = ctk.CTkButton(tabview.tab("Výdaje"), width = 20, height = 20, command = lambda: self.delete_money(3, "exp", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            expButton3.place( relx = 0.9, rely = 0.33)
            expButton4 = ctk.CTkButton(tabview.tab("Výdaje"), width = 20, height = 20, command = lambda: self.delete_money(4, "exp", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            expButton4.place( relx = 0.9, rely = 0.44)
            expButton5 = ctk.CTkButton(tabview.tab("Výdaje"), width = 20, height = 20, command = lambda: self.delete_money(5, "exp", win), image = ctk.CTkImage(light_image= Image.open("photo/red_check.png"), size=(20, 20)), text = "")
            expButton5.place( relx = 0.9, rely = 0.55)
        except:
            print("Missing .png file or photo folder")
        
        ctk.CTkButton(win, text = "Filtrovat", command= lambda: self.filter_money_window(moneyAll, labels), fg_color="green").place(relwidth = 0.1, relheight = 0.03, relx = 0.45, rely = 0.85)
        ctk.CTkButton(tabview.tab("Příjmy"), text="Přidat příjem", command= lambda: self.add_income("příjem", tabview, moneyAll, labels)).place(relx = 0.35, rely = 0.9)
        ctk.CTkButton(tabview.tab("Výdaje"), text= "Přidat výdaj", command= lambda: self.add_income("výdaj", tabview, moneyAll, labels)).place(relx = 0.35, rely = 0.9)
        ctk.CTkLabel(tabview.tab("Příjmy"), text = "        ".join([" Hodnota", "Den", " Měsíc", "Rok", "Kategorie"])).place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0)
        ctk.CTkLabel(tabview.tab("Výdaje"), text = "        ".join([" Hodnota", "Den", " Měsíc", "Rok", "Kategorie"])).place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0)
        
        self.update_money(self.user, self.money[0], "inc", self.pageNum[0], moneyAll, labels, 0, [[], [], [], []])
        self.update_money(self.user, self.money[1], "exp", self.pageNum[1], moneyAll, labels, 1, [[], [], [], []])
        
    def delete_money(self, pos, typ, win):
        try:
            finder = filehandle.FileHandler(self.user)
            if typ == "inc":
                finder.deleteLine(self.money[0][(((self.pageNum[0] - 1) * 5) + pos) - 1])
                
            elif typ == "exp":
                finder.deleteLine(self.money[1][(((self.pageNum[0] - 1) * 5) + pos) - 1])
            else:
                pass

        except Exception as e:
            print("Invalid button clicked")
            print(e)

        win.withdraw()
        self.open_window()
        
    def change_page_num(self, operation, win, type):
        if type == "inc":
            if self.pageNum[0] > 0 and self.pageNum[0] < self.maxPageNum[0]:
                if operation == "add":
                    self.pageNum[0] += 1
                else:
                    self.pageNum[0] -= 1
            self.changeConstant = "Příjmy"
        else:
            if self.pageNum[1] > 0 and self.pageNum[1] < self.maxPageNum[1]:
                if operation == "add":
                    self.pageNum[1] += 1
                else:
                    self.pageNum[1] -= 1 
            self.changeConstant = "Výdaje"
                
        win.withdraw()
        self.open_window()
        
        
        self.maxPageNum
        
    def update_money(self, user, list, type, pageNum, moneyAll, labels, x, template):
        if x == 0:
            self.balance = 0
        list.clear()
        self.info[x].clear()
              
        path = os.path.join("users", user, user + ".txt")
        with open(path) as file:
            for i in file:
                if i.startswith(type):
                    typ, val, day, mon, yea, cat = i.split("$")
                    self.info[x].append([typ, int(val), day, mon, yea, cat.strip("\n")])
                else:
                    continue
                
                if type == "inc":
                    self.money[0].append(i.strip("\n"))
                    self.balance += int(val)
                else:
                    self.money[1].append(i.strip("\n"))
                    self.balance -= int(val)
            
            try:
                self.info[x] = sorter.sort_money(self.info[x])
            except:
                pass
            
            template[0] = ["=", type]
            self.info[x] = filter.filter_lists_by_attributes(self.template, self.info[x])
            
            self.maxPageNum[x] = (int(len(self.info[x]) / 5) + 1)
            
            for i in range(5):
                try:
                    statement = ""
                    filerange = i + ((pageNum - 1) * 5)
                    for j in range(1, 6):
                        statement = statement + "         " + str(self.info[x][filerange][j])
                    labels[x][i].configure(text = statement)           
                    moneyAll.configure(text="Zůstatek:     " + str(self.balance))
                except:
                    print("Ended loop")
                    break                
        
    # Function to handle income or expense addition
    def add_income(self, type, tabview, moneyAll, labels):
        window = ctk.CTkToplevel(self)
        window.geometry("400x300")
        window.title("Přidat " + type)
        
        textVal = ctk.CTkEntry(window, font=("Arial", 15), width=140, height=10)
        val_label = ctk.CTkLabel(window, text="Hodnota", font=("Arial", 15))
        textDay = ctk.CTkEntry(window, font=("Arial", 15), width=30, height=10)
        day_label = ctk.CTkLabel(window, text="Den / Měsíc / Rok", font=("Arial", 15))
        textMon = ctk.CTkEntry(window, font=("Arial", 15),width=30, height=10)
        textYea = ctk.CTkEntry(window, font=("Arial", 15), width=60, height=10)
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
        
        errorLabel = ctk.CTkLabel(window, text = "", bg_color="red", state = "disabled")
        
        button = ctk.CTkButton(window, text="Submit", command= lambda: self.submit(window, type, textVal.get(), textDay.get(), textMon.get(), textYea.get(), textCat.get(), tabview, moneyAll, labels, errorLabel))
        button.place(relx = 0.35, rely = 0.5)
        
    def isValidMonth(self, day, mon, yea):
       if (((mon == 2 and day <= 28 and self.isLeapYear(yea) == False) or (mon == 2 and day <= 29 and self.isLeapYear(yea))) or 
            (mon in [4, 6, 9, 11] and day <= 30) or 
            (mon in [1, 3, 5, 7, 8, 10, 12] and day <= 31)):
           return True
       else:
           return False

    # Function to handle submitting info about income or expense
    def submit(self, win, type, val, day, mon, yea, cat, tabview, moneyAll, labels, errorLabel):
        try:
            val = int(val)
            day = int(day)
            mon = int(mon)
            yea = int(yea)
        except:
            errorLabel.place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0.8)
            if len(cat) >= 5:
                errorLabel.configure(text = "Název kategorie je příliš dlouhý")
            elif val <= 0:
                errorLabel.configure(text = "Hodnota musí být větší než nula")
            else:
                errorLabel.configure(text = "Datum neexistuje")
            
        else:    
            if self.isValidMonth(day, mon, yea) and val > 0 and len(cat) <= 5:
                
                self.balance = 0
                
                if type == "příjem":
                    Money("inc", val, day, mon, yea, cat.strip()).save_money_info(self.user)
                else:
                    Money("exp", val, day, mon, yea, cat.strip()).save_money_info(self.user)
                    
                self.update_money(self.user, self.money[0], "inc", self.pageNum[0], moneyAll, labels, 0, [[], [], [], []])
                self.update_money(self.user, self.money[1], "exp", self.pageNum[1], moneyAll, labels, 1, [[], [], [], []])
                self.categ.append(cat.lower())
                win.destroy()    

    def isLeapYear(self, year):
        if year % 4 != 0:
            return False
        elif year % 100 != 0:
            return True
        elif year % 400 != 0:
            return False
        else:
            return True  

    def filter_money_window(self, moneyAll, labels):
        window = ctk.CTkToplevel(self)
        window.geometry("400x300")
        window.title("Filtrovat")

        textVal = ctk.CTkEntry(window, font=("Arial", 15), width=140, height=10)
        val_label = ctk.CTkLabel(window, text="Hodnota", font=("Arial", 15))
        textDayOne = ctk.CTkEntry(window, font=("Arial", 15), width=30, height=10)
        day_label_one = ctk.CTkLabel(window, text="Od", font=("Arial", 15))
        textDayTwo = ctk.CTkEntry(window, font=("Arial", 15), width=30, height=10)
        day_label_two = ctk.CTkLabel(window, text="Do", font=("Arial", 15))
        textMonOne = ctk.CTkEntry(window, font=("Arial", 15),width=30, height=10)
        textYeaOne = ctk.CTkEntry(window, font=("Arial", 15), width=60, height=10)
        textMonTwo = ctk.CTkEntry(window, font=("Arial", 15),width=30, height=10)
        textYeaTwo = ctk.CTkEntry(window, font=("Arial", 15), width=60, height=10)
        textCat = ctk.CTkEntry(window, font=("Arial", 15), width=140, height=10, placeholder_text="max 5 char")
        cat_label = ctk.CTkLabel(window, text="Kategorie", font=("Arial", 15))

        optionMenu = ctk.CTkOptionMenu(window, values=["Více než", "Méně než", "Rovná se"])
        optionMenu.place(relx = 0.55, rely = 0.1)
        optionMenu.set("Více než")
        

        textVal.place(relx = 0.55, rely = 0.2)
        textDayOne.place(relx = 0.55, rely = 0.4)
        textDayTwo.place(relx = 0.55, rely = 0.5)
        textMonOne.place(relx = 0.65, rely = 0.4)
        textMonTwo.place(relx = 0.65, rely = 0.5)
        textYeaOne.place(relx = 0.75, rely = 0.4)
        textYeaTwo.place(relx = 0.75, rely = 0.5)
        textCat.place(relx = 0.55, rely = 0.6)
        
        val_label.place(relx = 0.2, rely = 0.2)
        day_label_one.place(relx = 0.2, rely = 0.4)
        day_label_two.place(relx = 0.2, rely = 0.5)
        cat_label.place(relx = 0.2, rely = 0.6)
        
        button = ctk.CTkButton(window, text="Submit", command = lambda: self.check_filter(textDayOne, textMonOne, textYeaOne, textDayTwo, textMonTwo, textYeaTwo, errorLabel, textVal, textCat, optionMenu, moneyAll, labels, window))
        button.place(relx = 0.35, rely = 0.7)
        
        errorLabel = ctk.CTkLabel(window, text = "", bg_color="red", state = "disabled")

    def check_filter(self, textDayOne, textMonOne, textYeaOne, textDayTwo, textMonTwo, textYeaTwo, errorLabel, textVal, textCat, optionMenu, moneyAll, labels, window):
        condition = True
        
        self.template = [[],[],[[], []],[]]
        try:
            if textVal.get != "":
                direction = "="
                if optionMenu.get() == "Více než":
                    direction = ">"
                elif optionMenu.get() == "Méně než":
                    direction = "<"

                try:
                    self.template[1] = [direction, int(textVal.get())]
                except:
                    errorLabel.place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0.8)
                    errorLabel.configure(text = "Hodnota není podporována")
                    condition = False
            
            if textDayOne.get() != "" and textMonOne.get() != "" and textYeaOne.get() != "":
                if self.isValidMonth(int(textDayOne.get()), int(textMonOne.get()), int(textYeaOne.get())):
                    self.template[2][0] = [int(textDayOne.get()), int(textMonOne.get()), int(textYeaOne.get())]
                elif self.isValidMonth(int(textDayOne.get()), int(textMonOne.get()), int(textYeaOne.get())) == False and textDayOne.get() != "" and textMonOne.get() != "" and textYeaOne.get() != "":
                    errorLabel.place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0.8)
                    errorLabel.configure(text = "Datum neexistuje")
                    condition = False
                    
            if textDayTwo.get() != "" and textMonTwo.get() != "" and textYeaTwo.get() != "":
                if self.isValidMonth(int(textDayTwo.get()), int(textMonTwo.get()), int(textYeaTwo.get())):
                    self.template[2][0] = [int(textDayTwo.get()), int(textMonTwo.get()), int(textYeaTwo.get())]
                elif self.isValidMonth(int(textDayTwo.get()), int(textMonTwo.get()), int(textYeaTwo.get())) == False and textDayTwo.get() != "" and textMonTwo.get() != "" and textYeaTwo.get() != "":
                    errorLabel.place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0.8)
                    errorLabel.configure(text = "Datum neexistuje")
                    condition = False
                    
            if textCat != "":
                self.template[3] = textCat.get()
                
            if condition == True:
                self.update_money(self.user, self.money[0], "inc", self.pageNum[0], moneyAll, labels, 0, [[], [], [], []])
                self.update_money(self.user, self.money[1], "exp", self.pageNum[1], moneyAll, labels, 1, [[], [], [], []])        
                window.withdraw()
                    
            print(self.template, "Template")
        
        except Exception as e:
            print(e)
            
app = MainFrame()

app.attributes("-toolwindow", True)


if __name__ == "__main__":
    app.mainloop()