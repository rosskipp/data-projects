import pandas as pd
from ggplot import *

print pd.__version__

# load the csv
df = pd.read_csv('data.csv')

# lets tabe a look at what we have...
df.head()

# group by gender column
groupedGender = df.groupby('gender')
print groupedGender

# check out the size of each group
groupedGender.size()

# look at the size as a percentage of the whole
total = df.gender.count()
groupedGender.size() / total * 100

# How about the mean/median trip duration for each group, in minutes?
groupedGender['tripduration'].mean() / 60.
groupedGender['tripduration'].median() / 60.
# Don't have to use the bracket notation.
groupedGender.tripduration.std() / 60.

# An easier way to see this data is to use the describe method
groupedGender.tripduration.describe()

# How many data points over 10000 sec ~ 2hr 45min
df[df.tripduration > 10000].tripduration.count()

# Make a plot
df_short = df[df.tripduration < 10000]
df_short.tripduration = df_short.tripduration / 60.
p = ggplot(df_short, aes(x='tripduration')) + geom_histogram(bins=30) + xlab("Trip Duration (mins)") + ylab("Count")
print p.save_as_base64(as_tag=True)

# Which are the most popular start/end stations?
groupedStart = df.groupby('start station name')
groupedEnd = df.groupby('end station name')
groupedStart['start station name'].count().sort_values(ascending=False)[:5]
groupedEnd['end station name'].count().sort_values(ascending=False)[:5]



