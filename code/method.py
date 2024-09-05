'''
This file contains many of the functions used to construct the forecasts from the paper.
'''
# %%
import pandas as pd
from utils import path 
from macro_data_processing import transform_series
from dateutil.relativedelta import relativedelta


def import_data_and_construct_inflation_measure(price_level_list_index):

    # Load data
    df = pd.read_csv(path('data', 'fred_md_stationary.csv'))
    levels = pd.read_csv(path('data', 'fred_md_levels.csv'))

    # Set index
    levels['date'] = pd.to_datetime(levels['date'])
    levels = levels.set_index('date').sort_index()

    # Load appendix
    appendix = pd.read_csv(path('data', 'FRED-MD_updated_appendix.csv'), encoding='latin-1')

    # Dictionary of inflation measures
    price_level_measures = [
        'CPIAUCSL', # CPI: All Items
        'CPIULFSL', # CPI: All items less food
        'PCEPI' # PCE
        ]

    # Selected price level measure
    price_level_column_name = price_level_measures[price_level_list_index]

    # Isolate selected price level
    price_level = levels[price_level_column_name]

    # Log first difference of price level
    inflation = transform_series(price_level, 5).dropna()

    return inflation, df


def construct_rolling_windows(h, p, price_level_list_index=0):
    '''
    Constructs the rolling windows for this paper.

    Args:
        p (int): Number of lags used in the forecasting model, which is required to prevent data leakage.
        h (int): Horizon of the forecast.
    '''
    
    # Import inflation measure and other data
    inflation, stationary = import_data_and_construct_inflation_measure(price_level_list_index)

    # Start and end date
    start_date = inflation.index.min()
    end_date = inflation.index.max()

    df = pd.DataFrame()
    df.loc[0, 'start_training'] = start_date 
    df.loc[0, 'end_training'] = df.loc[0, 'start_training'] + relativedelta(years=10)

    df.loc[0, 'start_validation'] = df.loc[0, 'end_training'] + relativedelta(months=1)
    df.loc[0, 'first_validation_date_forecasted'] = df.loc[0, 'start_validation'] + relativedelta(months=p+h)
    df.loc[0, 'end_validation'] = df.loc[0, 'start_validation'] + relativedelta(months=12+p+h)

    df.loc[0, 'start_test'] = df.loc[0, 'end_validation'] + relativedelta(months=1)
    df.loc[0, 'first_test_date_forecasted'] = df.loc[0, 'start_test'] + relativedelta(months=p+h)
    df.loc[0, 'end_test'] = df.loc[0, 'start_test'] + relativedelta(months=12+p+h)

    i = 0
    while df.loc[i, 'end_test'] <= end_date:
        i += 1
        df.loc[i, 'start_training'] = df.loc[i-1, 'start_training'] + relativedelta(months=13)
        df.loc[i, 'end_training'] = df.loc[i, 'start_training'] + relativedelta(years=10)

        df.loc[i, 'start_validation'] = df.loc[i, 'end_training'] + relativedelta(months=1)
        df.loc[i, 'first_validation_date_forecasted'] = df.loc[i, 'start_validation'] + relativedelta(months=p+h)
        df.loc[i, 'end_validation'] = df.loc[i, 'start_validation'] + relativedelta(months=12+p+h)

        df.loc[i, 'start_test'] = df.loc[i, 'end_validation'] + relativedelta(months=1)
        df.loc[i, 'first_test_date_forecasted'] = df.loc[i, 'start_test'] + relativedelta(months=p+h)
        df.loc[i, 'end_test'] = df.loc[i, 'start_test'] + relativedelta(months=12+p+h)

    return df