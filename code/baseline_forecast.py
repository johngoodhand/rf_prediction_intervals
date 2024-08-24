# %%
import pandas as pd
from utils import generate_path 

# Load data
df = pd.read_csv(generate_path('data', 'fred_md_processed.csv'))
