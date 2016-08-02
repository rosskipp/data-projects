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

# How about the mean/median trip duration for each group, in minutes?
groupedGender['tripduration'].mean() / 60.
groupedGender['tripduration'].median() / 60.
# Don't have to use the bracket notation.
groupedGender.tripduration.std() / 60.


ggplot(df[df.gender == 1], aes(x='tripduration'))

df[df.gender == 1].head()
