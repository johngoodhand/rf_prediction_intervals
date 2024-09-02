# %%
import pandas as pd
from utils import path 
from method import import_data_and_construct_inflation_measure

# Parameters
price_level_list_index = 0

# Import inflation measure and other data
inflation, df = import_data_and_construct_inflation_measure(price_level_list_index)