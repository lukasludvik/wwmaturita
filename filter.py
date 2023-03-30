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
            print(filter, row[i])
            if not filter_value(filter, row[i]):
                return False
    return True

def filter_lists_by_attributes(template, lists):
    lists = code_list(lists)
    return [lst for lst in lists if filter_row(template, lst)]
   
def code_list(lists):
    coded_list = []
    for list in lists:
        coded_list.append(list[:2] + [list[2:5]] + list[5:])
    
    return coded_list

template = [
    [["=", "inc"]],
    [[">", 1000]],
    [[">", [2003, 1, 1]], ["<", [2007, 7, 1]]],
    [],
]
lists = [["inc", 2000, [2002, 3, 6], "cat"], ["inc", 200, [2002, 3, 25], "nig"], ["inc", 2000, [2005, 9, 30], "cock"]]
listsTwo = [["inc", 2000, 2002, 3, 6, "cat"], ["inc", 200, 2002, 3, 25, "nig"], ["inc", 2000, 2005, 9, 30, "cock"]]

result_lists = filter_lists_by_attributes(template, listsTwo)
print(result_lists)  # Output: [['inc', '2000', '3', '6', '2005', 'cat'], ['inc', '20000', '5', '7', '2001', 'cat']]