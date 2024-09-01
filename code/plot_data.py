# %%
import pandas as pd
from utils import path 
from macro_data_processing import transform_series
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go

# Parameters
price_level_list_index = 0

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

# Create the plot
fig = go.Figure()

fig.add_trace(go.Scatter(x=inflation.index, y=inflation, mode='lines'))

# Customize the plot
fig.update_layout(
    title='Date vs Value Plot (1950-2023)',
    xaxis_title='Date',
    yaxis_title='Value',
    xaxis=dict(
        tickmode='array',
        tickvals=pd.date_range(start=inflation.index.min(), 
                               end=inflation.index.max(), 
                               freq='5YE'),
        tickformat='%Y'
    )
)

# Show the plot
fig.show()
