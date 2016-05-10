import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

# DataFrame Layout
# df = pd.DataFrame(columns=['season', 'team', 'gameType', 'numGames', 'numBlocks'])

# load the csv
df = pd.read_csv('block-data.csv')



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
    zeroline = true,
    zerolinewidth = 2.0,
    bargap = 0.25
)
fig=dict(data=data, layout=layout)
plotly.offline.plot(fig)
