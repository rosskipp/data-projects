import bs4
import requests

### Helper functions
def isThisHeader(tds):
    return tds[0].text == 'Away' or tds[3].text == 'Home':

def formatScore(score):
    try:
        score = int(score)
    except:
        score = 'F'
    return score

# create the global dataframe for storage
df = pd.DataFrame(columns=['season', 'date', 'away_team', 'away_score', 'home_team', 'home_score'])

# Fall '16 sunday league data
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
    if isThisHeader(tds):
        continue

    gameDate = tds[4].text
    awayTeam = tds[0].text
    homeTeam = tds[2].text
    homeScore = formatScore(tds[3].text)
    awayScore = formatScore(tds[1].text)

    df.loc[(df.shape[0])+1] = [season, gameDate, awayTeam, awayScore, homeTeam, homeScore]

# save the data to overwrite - just so we have Something if id decides to break
df.to_csv('data_bak.csv', index=False)
