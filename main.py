import scrape_functions as sf 
import pandas as pd 
import numpy  as np 
import datetime

# Make date vector
dates = pd.date_range(start='2020/09/01',end='2020/10/31',freq='D').to_list()
dates = [x.strftime('%Y%m%d') for x in dates]

# Read in data
df = [sf.pull_dates(date=x) for x in dates]
df = pd.concat(df).reset_index(drop=True)

# Find upsets and broken spreads
index, row = [*df.iterrows()][1]
for index, row in df.iterrows():
    if row.finalOU == None:
        # Game not played yet
        df.loc[index,'upset'] = None
        df.loc[index,'spreadBeat'] = None
        df.loc[index,'correctedSpread'] = None
        continue
    sameName = row.predictedSpread[0:3] == row.finalSpread[0:3]
    sameSign = np.sign(float(row.predictedSpread[4:])) == \
        np.sign(float(row.finalSpread[4:]))
    if sameName ^ sameSign:
       isUpset = True
    else:
        isUpset = False
    if row.predictedSpread[:3] == row.finalSpread[:3]:
        # do nothing
        correctedSpread = row.finalSpread
    else:
        correctedSpread = row.predictedSpread[:4] + \
                          str(float(row.finalSpread[4:])*-1)
    spreadBeat = np.abs(float(correctedSpread[4:])) > \
                 np.abs(float(row.predictedSpread[4:]))
    
    df.loc[index,'upset'] = isUpset
    df.loc[index,'correctedSpread'] = correctedSpread
    df.loc[index,'spreadBeat'] = spreadBeat
 
 df = df.loc[:,['gameID','Date','Team1','Team2','predictedSpread','finalSpread',\
     'correctedSpread','spreadBeat','OU','finalOU','upset']]