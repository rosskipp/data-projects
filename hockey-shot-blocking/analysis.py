import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

# df = pd.DataFrame(columns=['season', 'team', 'gameType', 'numGames', 'numBlocks'])

# load the csv
df = pd.read_csv('block-data.csv')

# pull out just the regular season games
regular_season = df[df['gameType']=='regular']

# make a pivot table to calc the totals for the regular season
reg_season_total = regular_season.pivot_table(values=['numGames', 'numBlocks'], index='season', aggfunc=np.sum)

reg_season_total['blocksPerGame'] = reg_season_total.numBlocks / reg_season_total.numGames
