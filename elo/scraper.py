import bs4
import requests

# create the global dataframe for data storage
df = pd.DataFrame(columns=['season', 'date', 'away_team', 'away_score', 'home_team', 'home_score'])

# Fall '16 sunday league
season = '2016_fall_sunday'
soup = bs4.BeautifulSoup(requests.get("http://unionhall.teamopolis.com/league/division_info.aspx?DivisionID=22295&SeasonID=12950&DisplayType=3&ShowType=0").text, "lxml")
tables = soup.find_all("table", { "class": "inside_table" })

# The second table has the data, and each row is a game
rows = table[1].find_all('tr')

# go into each row and pull out the data
for row in rows:
    # pull out the data from the row and put it into the df
    tds = row.find_all('td')
    # check if this row is the header
    if tds[0].text == 'Away' or tds[3].text == 'Home':
        continue
    gameDate = tds[4].text
    awayTeam = tds[0].text
    homeTeam = tds[2].text
    awayScore = tds[1].text
    homeScore = tds[3].text
    try:
        awayScore = int(awayScore)
    except:
        awayScore = 'F'
    try:
        homeScore = int(homeScore)
    except:
        homeScore = 'F'
    
    df.loc[(df.shape[0])+1] = [season, gameDate, awayTeam, awayScore, homeTeam, homeScore]


# save the data to overwrite - just so we have Something if id decides to break
df.to_csv('data_bak.csv', index=False)