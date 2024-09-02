# %%
import pandas as pd
from method import import_data_and_construct_inflation_measure
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# Parameters
price_level_list_index = 0
p = 4
h = 4

# Import inflation measure and other data
inflation, levels, stationary = import_data_and_construct_inflation_measure(price_level_list_index)

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

    