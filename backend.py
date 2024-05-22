import pandas as pd
import numpy as np
from census_vars import census_vars

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

def get_census_data(state_name, county_name, var):
    return (
        df
        .loc[(df['STATE_NAME'] == state_name) & (df['COUNTY_NAME'] == county_name)]
        [['STATE_NAME', 'COUNTY_NAME', 'YEAR', var]]
    )

# This code is hard to read but it serves a purpose.
# In short: the order in which census_vars lists the variables is the order
# in which I want them to appear in the dropdown. The issue is that they contain
# duplicates due to the variable for "Work From Home" changing name throughtout
# the years. This code removes the duplicates while retaining the initial ordering,
# and prevents me from needing to duplicate data here. 
# See: https://stackoverflow.com/a/17016257/2518602
def get_unique_census_labels():
    return list(dict.fromkeys(census_vars.values()))

def get_ranking_df(column):
    df2 = df.copy() # We don't want to modify the global variable

    # Select just the rows and columns we need
    df2 = df2.loc[(df2['YEAR'] == 2019) | (df2['YEAR'] == 2021)]
    df2 = df2[['STATE_NAME', 'COUNTY_NAME', 'YEAR', column]]

    # Combine state and county into a single column
    df2 = df2.assign(County=lambda x: x.COUNTY_NAME + ', ' + x.STATE_NAME)
    df2 = df2.drop(columns=['STATE_NAME', 'COUNTY_NAME'])

    # Pivot for structure we need, calculate change and percent change, sort
    df2 = df2.pivot_table(index='County', columns='YEAR', values=column)
    df2['Change'] = df2[2021] - df2[2019]
    df2['Percent Change'] = (df2[2021] - df2[2019]) / df2[2019] * 100
    df2['Percent Change'] = df2['Percent Change'].round(1)
    df2 = df2.sort_values('Percent Change', ascending=False)

    # Create an index called "Rank" and drop columns with NA
    df2['Rank'] = list(range(1, len(df2.index) + 1))
    df2 = df2.reset_index().set_index('Rank')
    df2 = df2.dropna()

    return df2