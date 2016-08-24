#

Using pandas time series functionality to analyze step data from an iPhone.

I have recently become addicted to counting steps. This usually manifests itself as opening my step counting app on my iPhone a few times a day to ensure that I am getting over 10,000 steps (my mom says that's the magic number).  Luckily, this target happens to be relatively straightforward to achieve in NYC, where you're always on your feet.

Like any true data nerd, I wanted to be able to export this data for analysis outside my phone. Luckily some smart people over at Quantified Self Labs put out an app called QS Access that makes retrieving this data a cinch!  Here's some screen shots of exporting my step data as a CSV.

#### INSERT SCREEN SHOTS HERE

The QS Access app exports a CSV containing 3 columns: a start timestamp, an end timestamp, and the step count for this time period.  You can choose to have this data in rows of hours or days.  I figured I'd start with hours and see how it went - bigger data is always better, right?

### Talk about pandas time series here
This analysis is going to have to draw on the time series tools in pandas. Lucky for us, pandas has extensive time series functionality  having been developed initially for the financial services industry, which deals

TO THE DATAS

The usual...except that we know that the first two columns in the dataset are timestamps, so we'll let pandas parse these as dates.

```
df_hour = pd.read_csv('health_data_hour.csv', parse_dates=[0,1])

# take a look
df_hour.head()
type(df_hour.Start[1])
```

Notice that the type of the timestamp columns: `pandas.tslib.Timestamp`


#### resampling

#### summary stats (best day, worst day)


#### Window functions/moving average


Have a look at [my repo](https://github.com/rkipp1210/data-projects) for this project if you want to see the source.
