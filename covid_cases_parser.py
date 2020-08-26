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


def covid_cases(state, counties):
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    r = requests.get(url, allow_redirects=True)
    filename = 'us-counties.csv'
    first_date = str(date.today())
    today = str(date.today())
    last_date = today

    open('Data/' + filename, 'wb').write(r.content)

    data = pd.read_csv('Data/' + filename)

    # filter out non-new mexico counties
    data = data[data.state == state]

    # filter out any extra headers
    data = data[data.county != "Unknown"]



    plt.figure(1)
    for index, county in enumerate(counties):
        temp_county = data[data.county == county]

        temp_dates = temp_county['date'].tolist()
        if len(temp_dates) == 0:
            continue
        if min(temp_dates) < first_date:
            first_date = min(temp_dates)

    for index, county in enumerate(counties):
        temp_county = data[data.county == county]
        cases = temp_county['cases'].tolist()
        dates = temp_county['date'].tolist()
        save_data(dates, cases, county, 'TotalCases')
        temp_dates, temp_cases = normalize_dateline(first_date, last_date, dates, cases)
        plt.plot(temp_dates, temp_cases, label=county)
        # mplcursors.cursor(hover=True)
        # mng = plt.get_current_fig_manager()
        # mng.resize(*mng.window.maxsize())

    plt.title('NM County Cases')
    plt.legend(loc='best')
    plt.savefig('Data/CountyCases.png', dpi=300)

    plt.figure(2)
    for index, county in enumerate(counties):
        temp_county = data[data.county == county]
        cases = temp_county['deaths'].tolist()
        dates = temp_county['date'].tolist()
        save_data(dates, cases, county, 'Deaths')
        temp_dates, temp_cases = normalize_dateline(first_date, last_date, dates, cases)
        plt.plot(temp_dates, temp_cases, label=county)
        # mplcursors.cursor(hover=True)
        # mng = plt.get_current_fig_manager()
        # mng.resize(*mng.window.maxsize())

    plt.title('NM County Deaths')
    plt.legend(loc='best')
    plt.savefig('Data/CountyDeaths.png', dpi=300)

    plt.figure(3)
    for index, county in enumerate(counties):
        temp_county = data[data.county == county]
        cases = getDiff(temp_county['cases'].tolist())

        dates = temp_county['date'].tolist()
        dates = dates[1:]
        temp_dates, temp_cases = normalize_dateline(first_date, last_date, dates, cases)
        save_data(temp_dates, temp_cases, county, 'NewCases')
        plt.plot(temp_dates, temp_cases, label=county)
        # mplcursors.cursor(hover=True)
        # mng = plt.get_current_fig_manager()
        # mng.resize(*mng.window.maxsize())

    plt.title('NM County New Cases')
    plt.legend(loc='best')
    plt.savefig('Data/CountyNewCases.png', dpi=300)
    plt.ylabel('Cases')
    plt.xlabel('Date')
    plt.show()


def getDiff(list):
    res = []
    for index, value in enumerate(list):
        if (index+1 < len(list)):
            res.append(list[index+1]-list[index])
    return res

def main():
    state = "New Mexico"
    counties = ["Bernalillo", "Catron", "Chaves", "Cibola", "Colfax", "Curry", "De Baca", "Doña Ana", "Eddy", "Grant",
                "Guadalupe", "Harding", "Hidalgo", "Lea", "Lincoln", "Los Alamos", "Luna", "McKinley", "Mora", "Otero",
                "Quay", "Rio Arriba", "Roosevelt", "Sandoval", "San Juan", "San Miguel", "Santa Fe", "Sierra",
                "Socorro","Taos", "Torrance", "Union", "Valencia"]
    covid_cases(state, counties)
    plt.show()


if __name__ == "__main__":
    main()
