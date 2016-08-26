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
p = ggplot(df_hour, aes(x='__index__', y='steps')) + \
    geom_step() + \
    ggtitle("Hourly Step Count") + \
    xlab("Date") + \
    ylab("Steps")
print p
p.save("hourly_step_plot.png")

# Well that's pretty ugly. Lots of data points. Do some re-sampling

## Daily
df_daily = pd.DataFrame()
df_daily['step_count'] = df_hour.steps.resample('D').sum()
df_daily.head()
p = ggplot(df_daily, aes(x='__index__', y='step_count')) + \
    geom_step() + \
    stat_smooth() + \
    scale_x_date(labels="%m/%Y") + \
    ggtitle("Daily Step Count") + \
    xlab("Date") + \
    ylab("Steps")
print p
p.save("daily_step_plot.png")

# Weekly
df_weekly = pd.DataFrame()
df_weekly['step_count'] = df_daily.step_count.resample('W').sum()
df_weekly['step_mean'] = df_daily.step_count.resample('W').mean()
df_weekly.head()
p = ggplot(df_weekly, aes(x='__index__', y='step_count')) + \
    geom_step() + \
    stat_smooth() + \
    scale_x_date(labels="%m/%Y") + \
    ggtitle("Weekly Step Count") + \
    xlab("Date") + \
    ylab("Steps")
print p
p.save("weekly_step_count_plot.png")

p = ggplot(df_weekly, aes(x='__index__', y='step_mean')) + \
    geom_step() + \
    stat_smooth() + \
    scale_x_date(labels="%m/%Y") + \
    ggtitle("Weekly Step Mean") + \
    xlab("Date") + \
    ylab("Steps")
print p
p.save("weekly_step_mean_plot.png")


# Monthly
df_monthly = pd.DataFrame()
df_monthly['step_count'] = df_daily.step_count.resample('M').sum()
df_monthly['step_mean'] = df_daily.step_count.resample('M').mean()
df_monthly.head()
p = ggplot(df_monthly, aes(x='__index__', y='step_count')) + \
    geom_step() + \
    stat_smooth() + \
    scale_x_date(labels="%m/%Y") + \
    ggtitle("Monthly Step Count") + \
    xlab("Date") + \
    ylab("Steps")
print p
p.save("monthly_step_mean_plot.png")

p = ggplot(df_monthly, aes(x='__index__', y='step_mean')) + \
    geom_step() + \
    stat_smooth() + \
    scale_x_date(labels="%m/%Y") + \
    ggtitle("Monthly Step Mean") + \
    xlab("Date") + \
    ylab("Steps")
print p
p.save("monthly_step_mean_plot.png")

# Quarters
df_quarterly = pd.DataFrame()
df_quarterly['step_count'] = df_daily.step_count.resample('Q').sum()
df_quarterly['step_mean'] = df_daily.step_count.resample('Q').mean()
df_quarterly.head()
p = ggplot(df_quarterly, aes(x='__index__', y='step_count')) + \
    geom_step() + \
    stat_smooth() + \
    scale_x_date(labels="%m/%Y") + \
    ggtitle("Quartly Step Count") + \
    xlab("Date") + \
    ylab("Steps")
print p
p.save("quarterly_step_mean_plot.png")

p = ggplot(df_quarterly, aes(x='__index__', y='step_mean')) + \
    geom_step() + \
    stat_smooth() + \
    scale_x_date(labels="%m/%Y") + \
    ggtitle("Quartly Step Mean") + \
    xlab("Date") + \
    ylab("Steps")
print p
p.save("quarterly_step_mean_plot.png")

### look at weekday vs. weekend averages
## Helper to return if the day of week is a weekend or not
def weekendBool(day):
    if day not in ['Saturday', 'Sunday']:
        return False
    else:
        return True

df_daily['weekday'] = df_daily.index.weekday
df_daily['weekday_name'] = df_daily.index.weekday_name
# apply the helper on the weekday_name col
df_daily['weekend'] = df_daily.weekday_name.apply(weekendBool)
df_daily.head()

weekend_grouped = df_daily.groupby('weekend')
weekend_grouped.describe()
weekend_grouped.median()

p = ggplot(aes(x='step_count', color='weekend'), data=df_daily) + \
    stat_density() + \
    ggtitle("Comparing Weekend vs. Weekday Daily Step Count") + \
    xlab("Step Count")
print p
p.save("weekday_step_compare_plot.png")
# put when i started running seriously, and moved to NYC
# geom_vline(x=25)







# NOT NEEDED

# This is a hacky way to do this
# df_hour['day_id'] = df_hour.start_time.apply(lambda x: str(x.year) + str(x.dayofyear))

# split into two dfs so we can plot two overlaying histograms
# weekend_daily_data = df_daily[df_daily['weekend'] == True]
# weekday_daily_data = df_daily[df_daily['weekend'] == False]
# grouped_day_id = df_hour.groupby('day_id')
