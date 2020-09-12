import scrape_functions as sf 
import pandas as pd 
import datetime

# Make date vector
dates = pd.date_range(start='2020/09/01',end='2020/10/31',freq='D').to_list()
dates = [x.strftime('%Y%m%d') for x in dates]

# Read in data
df = [sf.pull_dates(date=x) for x in dates]
df = pd.concat(df).reset_index(drop=True)