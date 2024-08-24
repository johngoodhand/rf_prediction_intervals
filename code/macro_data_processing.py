'''
This code transforms the FRED-MD data using the suggested methods.
Download current.csv from https://research.stlouisfed.org/econ/mccracken/fred-databases/ and place
the file in the data folder.
'''
# %%
import pandas as pd
import numpy as np
from utils import generate_path


def transform_series(series, transformation_type):
    """
    Transform a time series based on the specified transformation type.

    Parameters:
    -----------
    series : pandas.Series
        The input time series to be transformed.
    transformation_type : int
        An integer specifying the type of transformation to apply:
        1: No transformation
        2: First difference (∆x_t)
        3: Second difference (∆2x_t)
        4: Natural log (log(x_t))
        5: First difference of log (∆ log(x_t))
        6: Second difference of log (∆2 log(x_t))
        7: Difference of relative change (∆(x_t/x_t-1 - 1.0))

    Returns:
    --------
    pandas.Series
        The transformed time series.

    Raises:
    -------
    ValueError
        If an invalid transformation_type is provided.

    Notes:
    ------
    - For log transformations (types 4, 5, 6), ensure the series contains only positive values.
    - NaN values may be introduced at the beginning of the series for difference operations.
    """
    if transformation_type == 1:
        # (1) No transformation
        return series
    elif transformation_type == 2:
        # (2) ∆xt (First difference of the series)
        return series.diff()
    elif transformation_type == 3:
        # (3) ∆2xt (Second difference of the series)
        return series.diff().diff()
    elif transformation_type == 4:
        # (4) log(xt) (Log transformation)
        return np.log(series)
    elif transformation_type == 5:
        # (5) ∆ log(xt) (First difference of the log-transformed series)
        return np.log(series).diff()
    elif transformation_type == 6:
        # (6) ∆2 log(xt) (Second difference of the log-transformed series)
        return np.log(series).diff().diff()
    elif transformation_type == 7:
        # (7) ∆(xt/xt−1 − 1.0) (Difference of relative change)
        return (series / series.shift(1) - 1.0).diff()
    else:
        raise ValueError("Invalid transformation type")
    

# Load monthly data.
fred_md = pd.read_csv(generate_path('data', 'current.csv'))

# Rename column to align with appendix
fred_md = fred_md.rename(columns={'IPB51222S':'IPB51222s'})

# Extract transform codes from fred_md
info = pd.DataFrame(fred_md.iloc[0].drop('sasdate'))
info = info.reset_index()

# Rename columns and set index
info = info.rename(columns={0:'tcode', 'index':'fred'})
info = info.set_index('fred').sort_index()

# Drop the transform row (this info is contained in fred_info)
fred_md = fred_md.drop(0)

# Rename date column and convert to pandas datetime object
fred_md = fred_md.rename(columns={'sasdate':'date'})
fred_md['date'] = pd.to_datetime(fred_md['date'])

# Set index
fred_md = fred_md.set_index('date').sort_index()

# Generate dataframe that will contain the transformed series.
df = pd.DataFrame(fred_md.index)
df = df.set_index('date').sort_index()

# Transform each series appropriately.
for series in fred_md.columns:
    trans_series = transform_series(fred_md[series], info.loc[series,'tcode'])
    df = df.join(trans_series, how='outer')

# Save
df.to_csv(generate_path('data', 'fred_md_processed.csv'))