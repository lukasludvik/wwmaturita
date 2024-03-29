def sort_money(money):
    sortedMoney = []

    for mon in money:
        mon[2], mon[3], mon[4] = int(mon[2]), int(mon[3]), int(mon[4])
        
    sort_values = sorted(money, key = lambda x: (x[2], x[3], x[4]), reverse=True)

    return sort_values