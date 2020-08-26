import pandas as pd
import matplotlib.pyplot as plt
import os
import mplcursors


def normalize_by_pop(cases, population):
    nor_cases = [x / population for x in cases]
    return nor_cases


def getPop(county):
    # get full population data
    data = pd.read_excel('Data/County_Population/population.xlsx', sheet_name='2019')
    return data.iloc[0]['Population']


def run_cases(counties):
    filepath = "Data/Counties/TotalCases"
    for county in counties:
        data = pd.read_csv(filepath+'/'+county+'.csv')
        dates = data["Date"]
        dates = pd.to_datetime(dates)
        cases = data["Cases"]
        nor_cases = normalize_by_pop(cases, getPop(county))

        save_data(dates, nor_cases, county, "Normalized/")

        plt.title('Cases Normalized by Population')
        plt.xlabel('Date')
        plt.ylabel('Case/Population')
        plt.plot(dates, nor_cases, label=county)
        # mplcursors.cursor(hover=True)
        # mng = plt.get_current_fig_manager()
        # mng.resize(*mng.window.maxsize())
        plt.legend()


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


def main():
    state = "New Mexico"
    counties = ["Bernalillo", "Catron", "Chaves", "Cibola", "Colfax", "Curry", "De Baca", "Doña Ana", "Eddy", "Grant",
                "Guadalupe", "Harding", "Hidalgo", "Lea", "Lincoln", "Los Alamos", "Luna", "McKinley", "Mora", "Otero",
                "Quay", "Rio Arriba", "Roosevelt", "Sandoval", "San Juan", "San Miguel", "Santa Fe", "Sierra",
                "Socorro","Taos", "Torrance", "Union", "Valencia"]
    run_cases(counties)
    plt.show()


if __name__ == "__main__":
    main()