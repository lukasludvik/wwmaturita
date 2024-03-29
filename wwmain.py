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
import graph as graph

# Change appearance from dark to light and back
ctk.set_appearance_mode('light')
def changeApp():
    if ctk.AppearanceModeTracker.appearance_mode == 1:
        ctk.set_appearance_mode('light')
    else:
        ctk.set_appearance_mode('dark')
        
class Money():
    def __init__(self, type, value, year, month, day, category):
        self.type = type
        self.value = value
        self.year = year
        self.month = month
        self.day = day
        
        self.category = category
        
    def save_money_info(self, user):
        try:
            path = os.path.join("users", user, user + ".txt")
            file = open(path, "a")
            file.write(self.type + "$" + str(self.value).strip(" ") + "$" + str(self.year) + "$" + str(self.month) + "$" + str(self.day) + "$" + str(self.category) + "\n")
            
        except Exception as e:
            print("error")
            print(e)

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
            logo = ctk.CTkLabel(self, image=img, text= "")
            logo.place(relx = 0.32, rely = 0.1)
        except:
            print("Missing .png file or photo file")
        
        

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
        self.error = ctk.CTkLabel(self, text="Jméno nebo heslo neexistuje", font=("Arial", 16), fg_color="red")
    
    # Function to register a new account
    def register(self):
        reg = ctk.CTkToplevel()
        reg.geometry("400x400")
        reg.title("Zaregistrovat se")
        reg.resizable(False, False)
        
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
        elif user.strip(" ") != "" and passw.strip(" ") != "" and not "$" in passw and (not "\n" in user and not "\t" in user):
            try:
                file = open("users\password.txt", "a")
                file.write(user + "\n")
                
                salt = os.urandom(5).hex()
                hasher = hashlib.sha256()
                hasher.update(salt.encode() + passw.encode())
                hashed_passw = hasher.hexdigest()
                
                file.write(salt + "$" + hashed_passw + "\n")
                
                ac.AccountMaker(user)
                
                reg.destroy()
                file.close()
                
                self.load_users()
            except:
                print("Saving account failed")
        else:
            error.place(relx = 0.3, rely = 0.8)
            error.configure(text = "Jméno nebo heslo není povoleno")
    
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
        self.balance = 0
        win.protocol("WM_DELETE_WINDOW", lambda: app.destroy())
        win.resizable(False, False)
        
        moneyAll = ctk.CTkLabel(win, text= "Zůstatek:  " + str(self.balance), font=("Arial", 50), anchor="center")
        moneyAll.place(relx=0.33, rely = 0.15)
        
        buttonChange = ctk.CTkButton(win,  
                            text='Změnit vzhled',
                            command= lambda: changeApp(),
                            ) 
        buttonChange.place(relwidth = 0.05, relheight = 0.03, relx = 0.025, rely = 0.9)
        
        outLabel = ctk.CTkLabel(win, text="Přihlášen: " + self.user, font=("Arial", 15))
        outLabel.place(relwidth = 0.1, relheight = 0.05, relx=0.05, rely=0.06, anchor="center")
        
        buttonLogOut = ctk.CTkButton(win, text="Odhlásit se", command= lambda: self.logout(win))
        buttonLogOut.place(relwidth = 0.05, relheight = 0.03, relx = 0.025, rely = 0.08)
        
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
        
        ctk.CTkButton(win, text = "Filtrovat", command= lambda: self.filter_money_window(win), fg_color="green").place(relwidth = 0.1, relheight = 0.03, relx = 0.45, rely = 0.85)
        ctk.CTkButton(tabview.tab("Příjmy"), text="Přidat příjem", command= lambda: self.add_income("příjem", win)).place(relwidth = 0.2, relheight = 0.07, relx = 0.42, rely = 0.9)
        ctk.CTkButton(tabview.tab("Výdaje"), text= "Přidat výdaj", command= lambda: self.add_income("výdaj", win)).place(relwidth = 0.2, relheight = 0.07, relx = 0.42, rely = 0.9)
        ctk.CTkLabel(tabview.tab("Příjmy"), text = "        ".join([" Hodnota", "Rok", " Měsíc", "Den", "Kategorie"])).place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0)
        ctk.CTkLabel(tabview.tab("Výdaje"), text = "        ".join([" Hodnota", "Rok", " Měsíc", "Den", "Kategorie"])).place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0)
        
        self.update_money(self.user, self.money[0], "inc", self.pageNum[0], moneyAll, labels, 0)
        self.update_money(self.user, self.money[1], "exp", self.pageNum[1], moneyAll, labels, 1)

        ctk.CTkButton(win, text= "Ukázat graf", command= lambda: graph.showGraph(self.info), fg_color="black").place(relwidth = 0.08, relheight = 0.02, relx = 0.46, rely = 0.9)
        
    def delete_money(self, pos, typ, win):
        try:
            text = ""
            for i in range(6):
                text = text + str(self.info[0][(((self.pageNum[0] - 1) * 5) + pos) - 1][i])
                if i != 5:
                    text = text + '$'

            finder = filehandle.FileHandler(self.user)
            if typ == "inc":
                finder.deleteLine(text)
                
            elif typ == "exp":
                finder.deleteLine(text)

        except:
            print("Invalid button clicked")

        win.withdraw()
        self.open_window()
        
    def change_page_num(self, operation, win, type):
        if type == "inc":
            if operation == "add" and self.pageNum[0] > 0 and self.pageNum[0] < self.maxPageNum[0]:
                    self.pageNum[0] += 1
            elif operation == "min" and self.pageNum[0] > 1 and self.pageNum[0] <= self.maxPageNum[0]:
                    self.pageNum[0] -= 1
            self.changeConstant = "Příjmy"
        else:
            if operation == "add" and self.pageNum[1] > 0 and self.pageNum[1] < self.maxPageNum[1]:
                self.pageNum[1] += 1
            elif operation == "min" and self.pageNum[1] > 1 and self.pageNum[1] <= self.maxPageNum[1]:
                self.pageNum[1] -= 1 
            self.changeConstant = "Výdaje"
                
        win.withdraw()
        self.open_window()
        
        
    def update_money(self, user, list, type, pageNum, moneyAll, labels, x):
        if x == 0:
            self.balance = 0
        list.clear()
        self.info[x].clear()
              
        path = os.path.join("users", user, user + ".txt")
        with open(path) as file:
            for i in file:
                if i.startswith(type):
                    typ, val, yea, mon, day, cat = i.split("$")
                    self.info[x].append([typ, int(val), yea, mon, day, cat.strip("\n")])
                else:
                    continue
                
                if type == "inc":
                    list.append(i.strip("\n"))
                    self.balance += int(val)
                else:
                    list.append(i.strip("\n"))
                    self.balance -= int(val)
            
            try:
                self.info[x] = sorter.sort_money(self.info[x])
            except:
                print("sorting error")

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
                    break  


            print(self.info)              
        
    # Function to handle income or expense addition
    def add_income(self, type, topWindow):
        window = ctk.CTkToplevel(self)
        window.geometry("400x300")
        window.title("Přidat " + type)
        window.resizable(False, False)
        
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
        
        button = ctk.CTkButton(window, text="Přidat", command= lambda: self.submit(window, type, textVal.get(), textDay.get(), textMon.get(), textYea.get(), textCat.get(), errorLabel, topWindow))
        button.place(relx = 0.35, rely = 0.5)
        
    def isValidMonth(self, day, mon, yea):
       if (((mon == 2 and day <= 28 and self.isLeapYear(yea) == False) or (mon == 2 and day <= 29 and self.isLeapYear(yea))) or 
            (mon in [4, 6, 9, 11] and day <= 30) or 
            (mon in [1, 3, 5, 7, 8, 10, 12] and day <= 31)) and mon > 0 and yea > 0 and day > 0:
           return True
       else:
           return False

    # Function to handle submitting info about income or expense
    def submit(self, win, type, val, day, mon, yea, cat, errorLabel, topWindow):
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
            if self.isValidMonth(day, mon, yea) == True and val > 0 and len(cat) <= 5 and cat.strip(" ") != "" and not "$" in cat: #Here check
                
                self.balance = 0
                
                if type == "příjem":
                    Money("inc", val, yea, mon, day, cat.strip()).save_money_info(self.user)
                else:
                    Money("exp", val, yea, mon, day, cat.strip()).save_money_info(self.user)
                    
                win.destroy()   
                topWindow.destroy()
                self.open_window() 

    def isLeapYear(self, year):
        if year % 4 != 0:
            return False
        elif year % 100 != 0:
            return True
        elif year % 400 != 0:
            return False
        else:
            return True  

    def filter_money_window(self, topWin):
        window = ctk.CTkToplevel(self)
        window.geometry("400x300")
        window.title("Filtrovat")
        window.resizable(False, False)
        

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
        
        button = ctk.CTkButton(window, text="Submit", command = lambda: self.check_filter(textDayOne, textMonOne, textYeaOne, textDayTwo, textMonTwo, textYeaTwo, textVal, textCat, optionMenu, window, topWin, errorLabel))
        button.place(relx = 0.35, rely = 0.7)
        
        errorLabel = ctk.CTkLabel(window, text = "Chyba", bg_color="red", state = "disabled")

    def check_filter(self, textDayOne, textMonOne, textYeaOne, textDayTwo, textMonTwo, textYeaTwo, textVal, textCat, optionMenu, window, topWin, errorLabel):
        
        self.template = [[],[],[],[]]

        try:
            try:
                if textVal.get() != "":
                    if optionMenu.get() == "Více než":
                        self.template[1] = [[">", int(textVal.get())]]
                    elif optionMenu.get() == "Méně než":
                        self.template[1] = [["<", int(textVal.get())]]
                    else:
                        self.template[1] = [["=", int(textVal.get())]]

            except:
                print("Error with value")
                errorLabel.place(relx = 0.35, rely = 0.7)

            try:
                if textDayOne.get() != "" and textMonOne.get() != "" and textYeaOne.get() != "":
                    if self.isValidMonth(int(textDayOne.get()), int(textMonOne.get()), int(textYeaOne.get())) == True:
                        self.template[2].append([">", [int(textYeaOne.get()), int(textMonOne.get()), int(textDayOne.get())]])
                    else:
                        errorLabel.place(relx = 0.35, rely = 0.7)
            except Exception as e:
                print("Error with first date", e)
                errorLabel.place(relx = 0.35, rely = 0.7)

            try:
                if textDayTwo.get() != "" and textMonTwo.get() != "" and textYeaTwo.get() != "":
                    if self.isValidMonth(int(textDayTwo.get()), int(textMonTwo.get()), int(textYeaTwo.get())) == True:
                        self.template[2].append(["<", [int(textYeaTwo.get()), int(textMonTwo.get()), int(textDayTwo.get())]])
                    else:
                        errorLabel.place(relx = 0.35, rely = 0.7)
            except Exception as e:
                print("Error with second date", e)
                errorLabel.place(relx = 0.35, rely = 0.7)

            try:
                if textCat.get() != "":
                    self.template[3] = [["=", textCat.get()]]
            
            except Exception as e:
                print("Error with category")
                errorLabel.place(relx = 0.35, rely = 0.7)

            topWin.withdraw()
            window.withdraw()

            self.open_window()
            
        except Exception as e:
            print(e)

            
app = MainFrame()

app.attributes("-toolwindow", True)

app.protocol("WM_DELETE_WINDOW", lambda: app.destroy())

if __name__ == "__main__":
    app.mainloop()