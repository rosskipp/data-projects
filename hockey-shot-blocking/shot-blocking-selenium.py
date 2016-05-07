from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import random, time

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
baseURL = 'http://www.nhl.com/stats/player?reportType=game&report=realtime&aggregate=1&pos=S&sort=hits'

# create the global dataframe for data storage
df = pd.DataFrame(columns=['season', 'team', 'gameType', 'numGames', 'numBlocks'])

def processDataTable(df, soup, yearId, teamId, regularSeason):
    tableRows = soup.find_all('tr')
    try:
        team = tableRows[1].find(class_=" teamAbbrev").text
    except:
        team = str(teamId)
    season = yearId

    if regularSeason:
        gameType = 'regular'
        numGames = 82
    else:
        gameType = 'playoff'
        numGames = 0

    maxGames = 0
    shotBlocks = 0
    for row in tableRows:
        try:
            gamesPlayed = int(row.find(class_=" gamesPlayed").text)
        except:
            gamesPlayed = 0
            print 'could not get games played: ' + str(row)
        if gamesPlayed > maxGames:
            maxGames = gamesPlayed
        try:
            shotBlocks += int(row.find(class_="blockedShots").text)
        except:
            print 'could not get shot blocks: ' + str(row)

        if maxGames > numGames:
            numGames = maxGames

    print 'season: ' + season
    print 'team: ' + team
    print 'game type: ' + gameType
    print 'number of games: ' + str(numGames)
    print 'number of shot bocks: ' + str(shotBlocks)
    df.loc[(df.shape[0])+1] = [season, team, gameType, numGames, shotBlocks]
    return df


for i in range(len(years)-1):
    yearId = years[i] + years[i+1]
    for teamId in teamIds:
        url = baseURL + '&season=' + yearId + '&teamId=' + str(teamId) + '&gameType=3'
        print 'url: ' + url
        browser.get(url)
        element = browser.find_element_by_xpath('//*[@id="stats-data-table"]/tbody')
        htmlData = element.get_attribute('innerHTML')
        soup = BeautifulSoup(htmlData, "lxml")

        # wait for page load
        seconds = 2 + (random.random() * 3)
        time.sleep(seconds)
        # if there is no data in the table, then the team didn't make the playoffs
        # and we can move on
        if soup.text == 'No data available in table':
            continue
        else:
            df = processDataTable(df, soup, yearId, teamId, False)

            # run this team and year combo on the regular season
            url = baseURL + '&season=' + yearId + '&teamId=' + str(teamId) + '&gameType=2'
            print 'url: ' + url
            browser.get(url)
            element = browser.find_element_by_xpath('//*[@id="stats-data-table"]/tbody')
            htmlData = element.get_attribute('innerHTML')
            soup = BeautifulSoup(htmlData, "lxml")
            # wait for page load
            seconds = 2 + (random.random() * 3)
            time.sleep(seconds)

            df = processDataTable(df, soup, yearId, teamId, True)

            # be nice and humanlike
            seconds = 5 + (random.random() * 5)
            time.sleep(seconds)

            # save the data to overwrite - just so we have Something if id decides to break
            df.to_csv('~/Development/github/data-projects/hockey-shot-blocking/data.csv',index=False)
