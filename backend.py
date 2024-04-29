import pandas as pd
import censusdis.data as ced
from censusdis.datasets import ACS5
from census_vars import census_vars
import shapely

df = pd.read_csv('county_data.csv')

def get_state_names():
    return df['STATE_NAME'].unique()

def get_county_names(state_name):
    return (
        df
        .loc[df['STATE_NAME'] == state_name]
        ['COUNTY_NAME']
        .sort_values()
        .unique()
    )

def get_county_fips_codes(state_name, county_name):
    return (
        df
        .loc[(df['STATE_NAME'] == state_name) & (df['COUNTY_NAME'] == county_name)] # The row
        [['state.fips', 'county.fips']] # The columns we care about
        .values.tolist() # As a list of lists (one list per row)
        [0] # There is only 1 row, so return the first element
    )

# See https://github.com/arilamstein/censusdis-streamlit/issues/3#issuecomment-1986709449
def get_hover_data_for_var_label(var_label):
    if var_label == 'Total Population':
        return ":,"
    else:
        return ":$,"

def get_census_data(state_name, county_name, var_label):
 
    var_table = census_vars[var_label]

    return (
        df
        .loc[(df['STATE_NAME'] == state_name) & (df['COUNTY_NAME'] == county_name)]
        [['STATE_NAME', 'COUNTY_NAME', 'YEAR', var_table]]
        .rename(columns={var_table: var_label})
    )
