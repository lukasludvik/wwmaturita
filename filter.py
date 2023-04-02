# Soubor vytvořen s pomocí učitele programování, Jakuba Červenky
def filter_value(filter, value):
    if filter[0] == ">":
        return value >= filter[1]
    elif filter[0] == "<":
        return value <= filter[1]
    elif filter[0] == "=":
        return value == filter[1]
    else:
        raise ValueError("Direction must be '>', '<' or '='")
           
def filter_row(template, row):
    for i in range(0, len(template)):
        for filter in template[i]:
            if not filter_value(filter, row[i]):
                return False
    return True
   
def code_list(lists):
    coded_list = []
    
    for list in lists:
        coded_list.append(list[:2] + [list[2:5]] + list[5:])
    
    return coded_list

# Vytvořeno s pomocí AI (https://chat.openai.com)
def decode_list(lst):
    new_lst = []
    for element in lst:
        if isinstance(element, list):
            new_lst.extend(decode_list(element))
        else:
            new_lst.append(element)
    return new_lst

# Konec pomoci AI

def filter_lists_by_attributes(template, lists):
    print(lists)
    lists = code_list(lists)
    print(lists)

    new_lists =  [lst for lst in lists if filter_row(template, lst)]
   
    final_lists = []

    for lst in new_lists:
        new_list = decode_list(lst)
        final_lists.append(new_list)

    print(final_lists)
    
    return final_lists