import matplotlib.pyplot as plt
from datetime import datetime

# assume data is a list of lists in the format specified in the original question

def showGraph(old_data):
    data = []
    
    for i in range(2):
        for j in old_data[i]:
            data.append(j)

    

    # extract the dates and values from the data
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

    # create a new figure with size 1920x1080 pixels
    fig, ax = plt.subplots(figsize=(19.2, 10.8))

    # plot the data as a scatter plot with different colors
    ax.scatter(dates_inc, values_inc, color='green')
    ax.scatter(dates_exp, values_exp, color='red')

    # set the x-ticks to be the dates in the original data
    dates = sorted(list(set(dates_inc + dates_exp)))
    ax.set_xticks(dates)

    # set y-axis limit to zero for expenses
    ax.set_ylim(bottom=0)

    # add annotations to the data points
    for i, date in enumerate(dates_inc):
        value = values_inc[i]
        ax.annotate(value, (date, value+100), ha='center', fontsize=9)
    for i, date in enumerate(dates_exp):
        value = values_exp[i]
        ax.annotate(value, (date, value+100), ha='center', fontsize=9)

    # show the plot
    plt.show()


showGraph([[
        ['inc', 5000, 5, 9, 2022, 'bb'],
        ['inc', 20000, 5, 9, 2022, 'bb'],
        ['inc', 4000, 27, 8, 2023, 'bdbf'],
        ['inc', 200, 9, 11, 2022, 'bf'],
        ['inc', 4000, 23, 6, 2023, 'bdbr'],
        ['inc', 4000, 13, 1, 2023, 'bdbg'],
        ['inc', 4000, 19, 4, 2023, 'bdbe']], 

        [
        ['exp', 4000, 15, 2, 2023, 'bdbb'],
        ['exp', 4000, 17, 3, 2023, 'bdbc'],
        ['exp', 4000, 21, 5, 2023, 'bdbg'],
        ['exp', 4000, 25, 7, 2023, 'bdbw'],
        ['exp', 4000, 11, 12, 2022, 'bdbf']
        ]])
