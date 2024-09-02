# %%
import pandas as pd
from utils import path 
from macro_data_processing import transform_series


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