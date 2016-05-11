import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import numpy as np
from scipy import stats
from numpy import arange,array,ones
import matplotlib.pyplot as plt
import pandas as pd

plotly.offline.init_notebook_mode()

# DataFrame Layout
# df = pd.DataFrame(columns=['season', 'team', 'gameType', 'numGames', 'numBlocks'])

# load the csv
df = pd.read_csv('block-data.csv')

# Calculate our normalized stats
df['blkPerGmRegular'] = df.numBlocksRegular / df.numGamesRegular
df['blkPerGmPlayoff'] = df.numBlocksPlayoffs / df.numGamesPlayoffs
df['blkDiff'] = df.blkPerGmPlayoff - df.blkPerGmRegular

# Plot the regular season and playoff data separately
trace1 = go.Histogram(
    x = df.blkPerGmRegular,
    opacity = 0.66,
    name = 'Regluar Season',
    marker = dict(
        line = dict(
            color = 'grey',
            width = 1.0
        )
    )
)
trace2 = go.Histogram(
    x = df.blkPerGmPlayoff,
    opacity = 0.66,
    name = 'Playoffs',
    marker = dict(
        line = dict(
            color = 'grey',
            width = 1.0
        )
    )
)
data = [trace1, trace2]
layout = dict(
    title = '2006-2015 NHL Shot Blocks Per Game For Playoff Teams',
    yaxis = dict(title = '%'),
    xaxis = dict(title = 'Shot Blocks per Game (Cumulative Shot Blocks / Games Played)'),
    bargap = 0.25
    barmode='overlay'
)
fig=dict(data=data, layout=layout)
plotly.offline.plot(fig)

# Plot the Playoff - Regular Difference
trace1 = go.Histogram(
    x = df.blkDiff,
    marker = dict(
        line = dict(
            color = 'grey',
            width = 1.0
        )
    )
)
data = [trace1]
layout = dict(
    title = '2006-2015 NHL Shot Blocks Per Game For Playoff Teams Difference (Playoff - Reguar Season)',
    yaxis = dict(title = '%'),
    xaxis = dict(
        title = 'Shot Blocks per Game Difference',
        zeroline = True
    ),
    bargap = 0.25
)
fig=dict(data=data, layout=layout)
plotly.offline.plot(fig)


# Look at boxplots for each season
seasons = [ 20062007, 20072008, 20082009, 20092010, 20102011, \
            20112012, 20122013, 20132014, 20142015, 20152016 ]
data = []
for seasonInt in seasons:
    trace = go.Box(
        y = df.blkPerGmRegular[df.season==seasonInt],
        name = str(seasonInt)[:4] + ' - ' + str(seasonInt)[4:],
        boxpoints = 'all',
        jitter=0.3,
    )
    data.append(trace)
layout = go.Layout(
    title = "2006-2015 NHL Regular Season Shot Blocks Per Game For Playoff Teams in Each Season",
    showlegend = False,
    yaxis = dict(title = 'Shot Blocks Per Game'),
    xaxis = dict(
        title = 'Season',
        tickangle = -45
    ),
)
fig = dict(data = data, layout = layout)
plotly.offline.plot(fig)

# Is the difference population normal?
resDiff = stats.normaltest(df.blkDiff)
print 'diff normality test: ' + str(resDiff)

resDiffT = stats.ttest_1samp(df.blkDiff, 0.0)
print 'diff t-test: ' + str(resDiffT)
