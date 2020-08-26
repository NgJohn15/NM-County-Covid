import pandas as pd
from pandasgui import show

data = pd.read_excel('Data/NM County Income.xlsx')
print(data.to_string(index=False))

show(data, settings={'block': True})