import pandas as pd
import numpy as np
import datetime
from ggplot import *

# Read in our data -> we know from checking out the data that cols 0 and 1 are datestamps
# so use the parse_dates function from pandas to try and parse these.  In this case
# it works, and converts them to pandas.tslib.Timestamp
df_day = pd.read_csv('health_data_hour.csv', parse_dates=[0,1]) 

# take a look
df_day.head()
type(df_day.Start[1])

# Let's take a look at the data as it stands now:
ggplot(df_day, aes(x='Start', y='Steps (count)')) + geom_line()

# Well that's pretty ugly. Lots of data points.

