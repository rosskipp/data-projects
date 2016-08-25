import pandas as pd
import numpy as np
import datetime
from ggplot import *

# Read in our data -> we know from checking out the data that cols 0 and 1 are datestamps
# so use the parse_dates function from pandas to try and parse these.  In this case
# it works, and converts them to pandas.tslib.Timestamp.
# Also, we want to make the start_time the index, skip the header row since we're giving
# the cols our own name
df_hour = pd.read_csv('health_data_hour.csv', parse_dates=[0,1], names=['start_time', 'steps'], usecols=[0, 2], skiprows=1, index_col=0)

# ensure the steps col are ints - weirdness going on with this one
df_hour.steps = df_hour.steps.apply(lambda x: int(float(x)))

df_hour.head()
type(df_hour.index)
type(df_hour.steps[1])

# Let's take a look at the data as it stands now (notice we can pass __index__ to the `x`
# param in ggplot to plot against the DF index
ggplot(df_hour, aes(x='__index__', y='steps')) + geom_step()


# Well that's pretty ugly. Lots of data points. Do some re-sampling

## Daily
df_daily = pd.DataFrame()
df_daily['step_count'] = df_hour.steps.resample('D').sum()
df_daily.head()
ggplot(df_daily, aes(x='__index__', y='step_count')) + geom_step() + stat_smooth() + scale_x_date(labels="%m/%Y")

# Weekly
df_weekly = pd.DataFrame()
df_weekly['step_count'] = df_daily.step_count.resample('W').sum()
df_weekly['step_mean'] = df_daily.step_count.resample('W').mean()
df_weekly.head()
ggplot(df_weekly, aes(x='__index__', y='step_count')) + geom_step() + stat_smooth() + scale_x_date(labels="%m/%Y")
ggplot(df_weekly, aes(x='__index__', y='step_mean')) + geom_step() + stat_smooth() + scale_x_date(labels="%m/%Y")

# Monthly
df_monthly = pd.DataFrame()
df_monthly['step_count'] = df_daily.step_count.resample('M').sum()
df_monthly['step_mean'] = df_daily.step_count.resample('M').mean()
df_monthly.head()
ggplot(df_monthly, aes(x='__index__', y='step_count')) + geom_step() + stat_smooth() + scale_x_date(labels="%m/%Y")
ggplot(df_monthly, aes(x='__index__', y='step_mean')) + geom_step() + stat_smooth() + scale_x_date(labels="%m/%Y")

# put when i started running seriously, and moved to NYC
# geom_vline(x=25)







# NOT NEEDED
# This is a hacky way to do this
df_hour['day_id'] = df_hour.start_time.apply(lambda x: str(x.year) + str(x.dayofyear))
grouped_day_id = df_hour.groupby('day_id')