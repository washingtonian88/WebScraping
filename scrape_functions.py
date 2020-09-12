from bs4 import BeautifulSoup
import requests
import pandas as pd 
import re

debug = 1 #toggle 0/1 to suppress printouts

# Read in spread and OU stats for game
def pull_spread(gameID='401242802'):
    if debug:
        print('\tParsing gameID:\t' + gameID)
    url  = 'https://www.espn.com/nba/game?gameId={}'.format(gameID)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    scores = soup.find_all('td',attrs={'class':"score"})
    if len(scores) > 0: # Game is in the future
        ou = scores[5].get_text()
        spread = scores[3].get_text()
        names  = soup.find_all('div',attrs={'class':"sb-meta"})
        name1  = names[0].find_all('a')[0].get_text().strip()
        name2  = names[1].find_all('a')[0].get_text().strip()
    elif len(soup.find_all('li',attrs={'class':'ou'})) > 0: # Game was in the past
        ou = soup.find_all('li',attrs={'class':'ou'})[0].get_text().strip()[12:]
        spread = soup.find_all('div',attrs={'class':"odds-details"})[0].get_text().strip().split('\n')[0][10:]
        name1  = soup.find_all('span',attrs={'class':"short-name"})[0].get_text()
        name2  = soup.find_all('span',attrs={'class':"short-name"})[1].get_text()
    else: # Game from past, does not have spread data
        return None
    return {'Team1':name1,'Team2':name2,'Spread':spread,'OU':ou,'gameID':gameID}


# Get gameID's from dates
def pull_dates(date='20200913'):
    if debug:
        print('Looking at date:\t' + date)
    url   = 'https://www.espn.com/nba/scoreboard/_/date/{}'.format(date)
    page  = requests.get(url)
    soup  = BeautifulSoup(page.text, 'html.parser')
    mystr = soup.find_all('script')[13].get_text()
    m     = re.compile(r"(game\?gameId=\d+)").findall(mystr)
    if len(m) == 0: # No gameID's gound
        return None
    gameIDs = [x[12:] for x in m]
    retval  = [pull_spread(gameID=x) for x in gameIDs]
    retval  = [x for x in retval if x]
    if len(retval) == 0: # gameID's found but not spread data returned
        return None
    retval = pd.DataFrame(retval)
    retval.loc[:,'Date'] = date
    return retval


