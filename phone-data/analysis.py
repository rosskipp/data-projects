import pandas as pd
import datetime

# Read in our data -> we know from checking out the data that cols 0 and 1 are dates
# so use the parse_dates function from pandas to try and parse these.  In this case
# it works, and converts them to pandas.tslib.Timestamp
df = pd.read_csv('health_data.csv', parse_dates=[0,1]) 

# take a look
df.head()
type(df.Start[1])


