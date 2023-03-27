def sort_money(money):
    sortedMoney = []

    for mon in money:
        mon[2], mon[3], mon[4] = int(mon[2]), int(mon[3]), int(mon[4])
        
    sort_values = sorted(money, key = lambda x: (x[4], x[3], x[2]))
    print(sort_values)
    
    for expense in sort_values:
            sort = f"{expense[0]}${expense[1]}${expense[2]}${expense[3]}${expense[4]}${expense[5]}"
            sortedMoney.append(sort)

    return sort_values


nig = sort_money([['inc', '500', '23', '6', '2020', 'cat\n'], ['inc', '500', '23', '5', '2020', 'cat\n'], ['inc', '500', '12', '6', '2020', 'cat\n'], ['inc', '500', '1', '7', '2021', 'cat\n']])
print(nig)