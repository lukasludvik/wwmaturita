import matplotlib.pyplot as plt
from datetime import datetime

# Vvtvořeno s pomocí umělé inteligence (https://chat.openai.com/) a (https://matplotlib.org/stable/index.html)
def showGraph(old_data):
    data = []
    
    for i in range(2):
        for j in old_data[i]:
            data.append(j)    

    dates_inc = []
    values_inc = []
    dates_exp = []
    values_exp = []
    for d in data:
        date = datetime(d[4], d[3], d[2])
        value = d[1]
        if d[0] == 'inc':
            if date in dates_inc:
                idx = dates_inc.index(date)
                values_inc[idx] += value
            else:
                dates_inc.append(date)
                values_inc.append(value)
        else:
            if date in dates_exp:
                idx = dates_exp.index(date)
                values_exp[idx] += abs(value)
            else:
                dates_exp.append(date)
                values_exp.append(abs(value))

 
    fig, ax = plt.subplots(figsize=(19.2, 10.8))

    ax.scatter(dates_inc, values_inc, color='green')
    ax.scatter(dates_exp, values_exp, color='red')

    dates = sorted(list(set(dates_inc + dates_exp)))
    ax.set_xticks(dates)

    ax.set_ylim(bottom=0)
    plt.xticks(rotation=45)

    for i, date in enumerate(dates_inc):
        value = values_inc[i]
        ax.annotate(value, (date, value+100), ha='center', fontsize=9)
    for i, date in enumerate(dates_exp):
        value = values_exp[i]
        ax.annotate(value, (date, value+100), ha='center', fontsize=9)

    # show the plot
    plt.show()
