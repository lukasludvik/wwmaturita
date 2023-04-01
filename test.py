def flatten_list(lst):
    new_lst = []
    for element in lst:
        if isinstance(element, list):
            new_lst.extend(flatten_list(element))
        else:
            new_lst.append(element)
    return new_lst

original_lists = [['inc', 4000, [3, 8, 90], 'bdbg'], ['inc', 4000, [3, 8, 90], 'bdbg'], ['inc', 4000, [3, 8, 90], 'bdbg'], ['inc', 4000, [3, 8, 90], 'bdbg']]
new_lists = []

for lst in original_lists:
    new_list = flatten_list(lst)
    new_lists.append(new_list)

print(new_lists)

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

        textVal.place(relx = 0.55, rely = 0.1)
        textDayOne.place(relx = 0.55, rely = 0.2)
        textDayTwo.place(relx = 0.55, rely = 0.4)
        textMonOne.place(relx = 0.65, rely = 0.2)
        textMonTwo.place(relx = 0.65, rely = 0.4)
        textYeaOne.place(relx = 0.75, rely = 0.2)
        textYeaTwo.place(relx = 0.75, rely = 0.4)
        textCat.place(relx = 0.55, rely = 0.4)
        
        val_label.place(relx = 0.2, rely = 0.1)
        day_label_one.place(relx = 0.2, rely = 0.2)
        day_label_two.place(relx = 0.2, rely = 0.4)
        cat_label.place(relx = 0.2, rely = 0.4)