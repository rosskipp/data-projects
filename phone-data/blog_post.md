# Using pandas time series functionality to analyze step data from an iPhone.

My name is Ross, and I am addicted to counting steps. The walking kind. This behavior usually manifests itself as me opening my step counting app on my iPhone many times a day to watch the number climb and ensure that I am getting over 10,000 (my mom says that's the magic number). Luckily, NYC is a walking city, so this target is very accessible.

Like any legit data nerd, I wanted to be able to export this data for analysis outside my phone. Of course, there's an app for that provided by some smart people over at Quantified Self Labs put out an app called QS Access that makes retrieving this data a cinch! Here're some screenshots of exporting my step data as a CSV.

#### INSERT SCREEN SHOTS HERE

The QS Access app exports a CSV containing three columns: a start timestamp, an end timestamp, and the step count during that period. There's an option to produce rows of hourly or daily data. Why not start with hours and see how it goes - bigger data is always better, right?

The analysis will draw on the time series tools in pandas. When Wes McKinny wrote pandas, he was working for an investment management company.  That industry relies extensively on time series analysis so pandas ships with comprehensive functionality in this area.

## TO THE DATAS

A couple of notes about importing this data. We already know that we have time series data, so we want to let pandas know by using the `parse_dates` parameter. The end time data isn't interesting because we have the start time and are aware it's hourly data so we can omit it with `usecols`. Last, setting the start time (col 0) to be the index column gives a DateTimeIndex and will make life easier later.

```
df_hour = pd.read_csv('health_data_hour.csv', parse_dates=[0,1], names=['start_time', 'steps'], usecols=[0, 2], skiprows=1, index_col=0)
# ensure the steps col are ints - weirdness going on with this one
df_hour.steps = df_hour.steps.apply(lambda x: int(float(x)))
df_hour.head()
type(df_hour.index)
type(df_hour.steps[1])
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>steps</th>
    </tr>
    <tr>
      <th>start_time</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2014-10-24 18:00:00</th>
      <td>459</td>
    </tr>
    <tr>
      <th>2014-10-24 19:00:00</th>
      <td>93</td>
    </tr>
    <tr>
      <th>2014-10-24 20:00:00</th>
      <td>421</td>
    </tr>
    <tr>
      <th>2014-10-24 21:00:00</th>
      <td>1306</td>
    </tr>
    <tr>
      <th>2014-10-24 22:00:00</th>
      <td>39</td>
    </tr>
  </tbody>
</table>

Notice that the type of the start_time column: `pandas.tseries.index.DatetimeIndex`. We got this type because we set the index column and it gives us access to all sorts of goodies - resampling for one, as we'll see later. As mentioned previously, pandas does Timestamps quite well.

How about a quick [(gg)plot](http://github.com/yhat/ggplot) to explore the data we have here. (Notice that you can pass the dataframe `__index__` into the ggplot function)

PLOT 1 - hourly data all

Yuck! That's a little too busy. How can we improve our visualization? I've got an idea - pandas has a function called `resample` that will allow us to aggregate our time series data over a given period. More precisely, this is called downsampling when you reduce the sampling rate of a given signal. For this example, we will take the hourly data, and resample it on a daily, weekly, and monthly basis.  Let's start with the daily totals:

```
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
```

PLOT 2 - DAILY DATA, STAT SMOOTH

Ah-ha! We're getting somewhere now.  That's a much more readable plot :) and it looks like there's a nice upward trend. Armed with this, we're able to do weekly and monthly resampling easily as well. Just pass `'W'` or `'M'` into the resample function. It makes sense to start averaging the data with this resampling to get a daily average during the week and month sample as that is the metric that I'm interested in targeting (got to get those 10,000 a day!). That just takes changing the `sum()` function after the `resample` to a `mean()`. Like this:

```
df_weekly['step_mean'] = df_daily.step_count.resample('W').mean()
df_monthly['step_mean'] = df_daily.step_count.resample('M').mean()
```

PLOT 3 AND 4 - WEEK AND MONTH AVERAGES

Pandas can also do the opposite of what we just did; called upsampling. Take a look at the docs if that's in your wheelhouse!

## Going (slightly) deeper

I'm curious if I'm getting more steps during the weekend than during the week. We can use the tab suggestions in Rodeo to take a look at the methods we have available on the DateTimeIndex, and notice that there is a `weekday` and `weekday_name` method. The former will give an integer corresponding to a day of the week, while the latter will give the string name of that day. After we make a new column with that info, applying a helper function to it can return a boolean value for if that is a weekend or not.

```
## Helper to return if the day of week is a weekend or not
def weekendBool(day):
    if day not in ['Saturday', 'Sunday']:
        return False
    else:
        return True

df_daily['weekday'] = df_daily.index.weekday
df_daily['weekday_name'] = df_daily.index.weekday_name
df_daily['weekend'] = df_daily.weekday_name.apply(weekendBool)
df_daily.head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>step_count</th>
      <th>weekday</th>
      <th>weekday_name</th>
      <th>weekend</th>
    </tr>
    <tr>
      <th>start_time</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2014-10-24</th>
      <td>2333</td>
      <td>4</td>
      <td>Friday</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2014-10-25</th>
      <td>3085</td>
      <td>5</td>
      <td>Saturday</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2014-10-26</th>
      <td>21636</td>
      <td>6</td>
      <td>Sunday</td>
      <td>True</td>
    </tr>
    <tr>
      <th>2014-10-27</th>
      <td>13776</td>
      <td>0</td>
      <td>Monday</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2014-10-28</th>
      <td>5732</td>
      <td>1</td>
      <td>Tuesday</td>
      <td>False</td>
    </tr>
  </tbody>
</table>

ggplot has a stat_density plot available that's perfect for comparing the weekend vs. weekday populations.

```
ggplot(aes(x='step_count', color='weekend'), data=df_daily) + \
    stat_density() + \
    ggtitle("Comparing Weekend vs. Weekday Daily Step Count") + \
    xlab("Step Count")
```

DENSITY PLOT

We can also group the data on this weekend_bool and run some aggregation methods to see the differences in the data.  Have a look at my previous post on [grouping in padas](http://blog.yhat.com/posts/grouping-pandas.html) for an explanation of this functionality.

```
weekend_grouped = df_daily.groupby('weekend')
weekend_grouped.describe()

                 step_count     weekday
weekend                                
False   count    479.000000  479.000000
        mean   10145.832985    1.997912
        std     4962.913936    1.416429
        min      847.000000    0.000000
        25%     6345.000000    1.000000
        50%     9742.000000    2.000000
        75%    13195.000000    3.000000
        max    37360.000000    4.000000
True    count    192.000000  192.000000
        mean   11621.166667    5.500000
        std     7152.197426    0.501307
        min      641.000000    5.000000
        25%     6321.000000    5.000000
        50%    10228.000000    5.500000
        75%    15562.500000    6.000000
        max    35032.000000    6.000000

weekend_grouped.median()
            step_count  weekday
weekend                     
False          9742      2.0
True          10228      5.5
```

So maybe a slight edge goes to those weekends :) Hopefully, this analysis was enough to get you interested in checking out your data, and using rodeo to explore the time series functionality of pandas! Have a look at [my repo](https://github.com/rkipp1210/data-projects) for this project if you want to see the source.
