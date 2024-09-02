# %%
import pandas as pd
from utils import path 
from method import import_data_and_construct_inflation_measure
import plotly.graph_objects as go

# Parameters
price_level_list_index = 0

# Import inflation measure and other data
inflation, df = import_data_and_construct_inflation_measure(price_level_list_index)

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
