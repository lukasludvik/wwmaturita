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
    for i in range(0, len(template) - 1):
        for filter in template[i]:
            if not filter_value(filter, row[i]):
                return False
    return True

def filter_lists_by_attributes(template, lists):
    # Filter the sorted lists based on the direction
    return [lst for lst in lists if filter_row(template, lst)]
   
   


   
template = [
    [["=", "inc"]],
    [[">", 1000]],
    [[">", [2003, 1, 1]], ["<", [2007, 7, 1]]],
    [],
]
lists = [["inc", 2000, [2002, 3, 6], "cat"], ["inc", 200, [2002, 3, 25], "cat"], ["inc", 2000, [2005, 9, 30], "cat"]]

result_lists = filter_lists_by_attributes(template, lists)
print(result_lists)  # Output: [['inc', '2000', '3', '6', '2005', 'cat'], ['inc', '20000', '5', '7', '2001', 'cat']]