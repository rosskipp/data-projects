from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

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
        if no data in table:
            continue
        else:
            #process and save this data


            # run this team and year combo on the regular season
            url = baseURL + '&season=' + yearId + '&teamId' + teamId + '&gameType=2'
            browser.get(url)
            element = browser.find_element_by_xpath('//*[@id="stats-data-table"]/tbody')
            htmlData = element.get_attribute('innerHTML')
            soup = BeautifulSoup(htmlData, "lxml")
            # process this data
