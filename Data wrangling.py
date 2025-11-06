import pandas as pd
from typing import Any


#import files: ------------------------------------------------------------------------------------
broad_money_supply: pd.DataFrame = pd.read_excel( #type: ignore
    r'C:\Users\finle\OneDrive\University\Applied Econometrics\Coursework'
    r'\broad Money Supply/Broad Money Supply - Euro; USA; UK.xlsx', 
    sheet_name="Table",
    header=0,
    parse_dates=['Time period'],
    index_col='Time period'
)

eer: pd.DataFrame = pd.read_excel( #type: ignore
    r'C:\Users\finle\OneDrive\University\Applied Econometrics\Coursework'
    r'\EER\Real Effective Exchange Rates - US^JUK^JFrance^J Germany^J Spain.xlsx',
    sheet_name="timeseries observations",
    header=0,
    parse_dates=['TIME_PERIOD:Period'],
    index_col='TIME_PERIOD:Period'
)
#monthly to quarterly: 
eer = (eer.groupby('REF_AREA:Reference area')
       .resample('QS')['OBS_VALUE:Value']
       .mean()
       .reset_index())  # Preserve column name
eer = eer.set_index('TIME_PERIOD:Period')

energy_index: pd.DataFrame = pd.read_excel( #type: ignore
    r'C:\Users\finle\OneDrive\University\Applied Econometrics\Coursework'
    r'\Energy Price\FRED - Global price of energy Index.xlsx',
    sheet_name='Quarterly',
    header=0,
    parse_dates=['observation_date'],
    index_col='observation_date'
)

inflation: pd.DataFrame = pd.read_csv(#type: ignore
    r'C:\Users\finle\OneDrive\University\Applied Econometrics\Coursework'
    r'\Inflation\Inflation - UK, US, France, Germany, Spain.csv',
    header=0,
    parse_dates=['TIME_PERIOD'],
    index_col='TIME_PERIOD'
)
#time formatting ----------------------------------------------------------------------------------

broad_money_supply.index = pd.DatetimeIndex(broad_money_supply.index).to_period('Q-DEC')
eer.index = pd.DatetimeIndex(eer.index).to_period('Q-DEC')
energy_index.index = pd.DatetimeIndex(energy_index.index).to_period('Q-DEC')
inflation.index = pd.DatetimeIndex(inflation.index).to_period('Q-DEC')



#data cleaning and label changing -----------------------------------------------------------------

eer = eer[['REF_AREA:Reference area','OBS_VALUE:Value']]

inflation = inflation[['COUNTRY', 'OBS_VALUE']]

broad_money_supply = broad_money_supply.rename(columns={'Reference area': 'Country',
                                                        "Value":"money_supply"})

eer = eer.rename(columns={'REF_AREA:Reference area': 'Country',
                          'OBS_VALUE:Value': 'eer'})


energy_index = energy_index.rename(columns={'PNRGINDEXQ': 'Energy_Prices'
                                            })

inflation = inflation.rename(columns={'COUNTRY': 'Country',
                                      'OBS_VALUE': 'inflation'})
#Changing to long form: ---------------------------------------------------------------------------

euro_rows = broad_money_supply[broad_money_supply['Country'] == 'Euro area (19 countries)']
countries = ['Germany', 'France', 'Spain']

duplicated_rows = pd.concat(
    [euro_rows.assign(Country=c) for c in countries])

broad_money_supply = pd.concat(
    [broad_money_supply[broad_money_supply['Country'] != 'Euro area (19 countries)'],
     duplicated_rows])

broad_money_supply['Country'] = broad_money_supply['Country'].str.split(':').str[-1]
eer['Country'] = eer['Country'].str.split(':').str[-1]

countries.extend(["United Kingdom", "United States"])

energy_index = pd.concat(
    [energy_index.assign(Country=c) for c in countries])

# #changing index to column -------------------------------------------------------------------------
broad_money_supply = broad_money_supply.reset_index(names='obs')
energy_index = energy_index.reset_index(names='obs')
eer = eer.reset_index(names='obs')
inflation = inflation.reset_index(names='obs')  

# # Creating overall panel data ---------------------------------------------------------------------
data: list[Any] = [broad_money_supply, eer, energy_index, inflation]

for i in data:
    print(i.groupby('Country').describe())
    

panel = broad_money_supply.merge(
    eer, on=['Country', 'obs'], how='outer').merge(
    energy_index,on=['Country', 'obs'], how='outer').merge(
    inflation, on=['Country', 'obs'], how='outer')

print(panel.groupby('Country').describe())

panel.to_csv("Panel.csv", index=False, header=True)

#creating America data ----------------------------------------------------------------------------
America = panel[panel['Country'] == 'United States']
print(America.describe())

America.to_csv("America.csv", index=False, header=True)


