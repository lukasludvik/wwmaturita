            if textVal.get() != "":
                print("hello")
                direction = "="
                if optionMenu.get() == "Více než":
                    direction = ">"
                elif optionMenu.get() == "Méně než":
                    direction = "<"

                try:
                    self.template[1] = [direction, int(textVal.get())]
                    print(self.template) #delete
                except:
                    errorLabel.place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0.8)
                    errorLabel.configure(text = "Hodnota není podporována")
                    condition = False
            
            if textDayOne.get() != "" and textMonOne.get() != "" and textYeaOne.get() != "":
                print("nigger")
                if self.isValidMonth(int(textDayOne.get()), int(textMonOne.get()), int(textYeaOne.get())):
                    self.template[2][0] = [int(textDayOne.get()), int(textMonOne.get()), int(textYeaOne.get())]
                elif self.isValidMonth(int(textDayOne.get()), int(textMonOne.get()), int(textYeaOne.get())) == False and textDayOne.get() != "" and textMonOne.get() != "" and textYeaOne.get() != "":
                    errorLabel.place(relwidth = 0.9, relheight = 0.1, relx = 0.05, rely = 0.8)
                    errorLabel.configure(text = "Datum neexistuje")
                    condition = False
                    
            if textDayTwo.get() != "" and textMonTwo.get() != "" and textYeaTwo.get() != "":
                print("nigger Two")
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
        