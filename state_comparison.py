import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import csv
import os
from datetime import date


def save_data(list1, list2, title, final_dir):
    # creates counties directory if it doesn't exist
    outdir = 'Data/Counties/'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # makes type directory
    outdir = 'Data/Counties/' + final_dir
    path = outdir + '/' + title + '.csv'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # saves data to its filepath with its given data as csv
    d = {'Date': list1, 'Cases': list2}
    df = pd.DataFrame(d)
    df.to_csv(path, sep=',', index=False, date_format='%s')


# returns temp_dates, temp_cases
def normalize_dateline(start, end, dates, cases):
    temp_dates = np.arange(start, end, dtype='datetime64')
    temp_cases = []
    for i in temp_dates:
        if str(i) in dates:
            temp_cases.append(cases[dates.index(str(i))])
        else:
            if len(temp_cases) > 0:
                temp_cases.append(temp_cases[-1])
            else:
                temp_cases.append(0)
    return temp_dates, temp_cases


def covid_cases(states):
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    r = requests.get(url, allow_redirects=True)
    filename = 'us-states.csv'
    first_date = str(date.today())
    today = str(date.today())
    last_date = today

    open('Data/' + filename, 'wb').write(r.content)
    data = pd.read_csv('Data/' + filename)

    plt.figure(1)
    for index, state in enumerate(states):
        temp_state = data[data.state == state]

        temp_dates = temp_state['date'].tolist()
        if len(temp_dates) == 0:
            continue
        if min(temp_dates) < first_date:
            first_date = min(temp_dates)

    for index, state in enumerate(states):
        temp_state = data[data.state == state]
        cases = temp_state['cases'].tolist()
        dates = temp_state['date'].tolist()
        save_data(dates, cases, state, 'TotalCases')
        temp_dates, temp_cases = normalize_dateline(first_date, last_date, dates, cases)
        plt.plot(temp_dates, temp_cases, label=state)
        # mplcursors.cursor(hover=True)
        # mng = plt.get_current_fig_manager()
        # mng.resize(*mng.window.maxsize())

    plt.ylabel('Cases')
    plt.xlabel('Date')
    plt.title('AZ, CO, NM Cases')
    plt.legend(loc='best')
    plt.savefig('Data/CountyCases.png', dpi=300)


def getDiff(list):
    res = []
    for index, value in enumerate(list):
        if (index+1 < len(list)):
            res.append(list[index+1]-list[index])
    return res

def main():
    states = ["New Mexico", "Arizona", "Colorado"]
    covid_cases(states)
    plt.show()


if __name__ == "__main__":
    main()
