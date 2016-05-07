from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import random

# setup the chrome webdriver
path_to_chromedriver = '/Users/rossie/Downloads/chromedriver'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

"""
URL Scheme:
gameType -> 2 for regular season, 3 for playoffs
season -> this is a two year id, ex: 20132014
teamId -> 1-30
"""
years = ['2008','2009','2010','2011','2012','2013','2014','2015', '2016']
teamIds = range(1, 31, 1)
baseURL = 'http://www.nhl.com/stats/player?reportType=game&report=realtime&aggregate=1&pos=S'

# create the global dataframe for data storage
df = pd.DataFrame(columns=['season', 'team', 'gameType', 'numGames', 'numBlocks'])

for i in range(len(years-1))
    yearId = years[i] + years[i+1]
    for teamId in teamIds:
        url = baseURL + '&season=' + yearId + '&teamId' + teamId + '&gameType=3'
        browser.get(url)
        element = browser.find_element_by_xpath('//*[@id="stats-data-table"]/tbody')
        htmlData = element.get_attribute('innerHTML')
        soup = BeautifulSoup(htmlData, "lxml")

        # if there is no data in the table, then the team didn't make the playoffs
        # and we can move on
        table
        if soup.text == 'No data available in table':
            continue
        else:
            df = processDataTable(df, soup, True)

            # run this team and year combo on the regular season
            url = baseURL + '&season=' + yearId + '&teamId' + teamId + '&gameType=2'
            browser.get(url)
            element = browser.find_element_by_xpath('//*[@id="stats-data-table"]/tbody')
            htmlData = element.get_attribute('innerHTML')
            soup = BeautifulSoup(htmlData, "lxml")

            df = processDataTable(df, soup, False)

            # be nice and humanlike
            seconds = 5 + (random.random() * 5)
            time.sleep(seconds)


def processDataTable(df, soup, reqularSeason):
    tableRows = soup.find_all('tr')
    team = trs[1].find(class_=" playerTeamsPlayedFor").text
    print team
    season = trs[1].find(class_=" seasonId").text
    if regularSeason:
        gameType = 'regular'
        numGames = 82
    else:
        gameType = 'playoffs'
        numGames = 0

    maxGames = 0
    shotBlocks = 0
    for row in tableRows:
        gamesPlayed = int(row.find(class_=" gamesPlayed").text)
        if gamesPlayed > maxGames:
            maxGames = gamesPlayed
        shotBlocks += int(row.find(class_="blockedShots").text)

    if maxGames > numGames:
        numGames = maxGames

    print 'season: ' + season
    print 'team: ' + team
    print 'game type: ' + gameType
    print 'number of games: ' + str(numGames)
    print 'number of shot bocks: ' + str(shotBlocks)
    df.append([season, team, gameType, numGames, shotBlocks])
    return df
