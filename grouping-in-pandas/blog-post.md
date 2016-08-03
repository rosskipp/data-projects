# An Introduction to Grouping in Pandas

Grouping data is an integral part of many data analysis projects. The functionality for grouping in pandas is vast, but can be tough to grasp initially. Have no fear...we will get through a short introduction together.

![]({{ STATIC_URL }}/img/grouping-buddies.jpg)

### Why would I want to group data?

Most of the time, you have a set of data that lends itself to being categorized or grouped. As a general example, let's say we have data on a wide variety of people. We may perform an analysis where we compare groups in the data based on age, gender, birth month, shoe size, or birth city; the options are as numerous as the data points!

The pandas `groupby` functionality draws from the `Split-Apply-Combine` method as described by Hadley Wickham from the land of R. It's a great approach to solving data analysis problems, and his paper on the subject is worth a read (it's linked in the resources section). To summarize, he states that a common methodology for analyzing data comes from splitting the data into categories or groups based on some criteria, applying some aggregation function to each group (sum, mean, count), then combining the results for analysis, visualization or other means of better understanding. Here's a graphic I came across illustrating the process:

![]({{ STATIC_URL }}/img/split-apply-combine.jpg)

Sounds handy, but how do I do it in pandas?

### Codes and Stuff

Just so we're on the same page, I’m running pandas `0.18.1`.

I was looking around for an intriguing dataset and came across [this data](https://www.citibikenyc.com/system-data) from Citi Bike, which is the NYC bike share program. It's pretty medium data at ~250MB CSV for one month's worth of data, and there was potential for some compelling findings with data grouping. Let's start down the rabbit hole...

![]({{ STATIC_URL }}/img/data-hole.jpg)

```
df = pd.read_csv('data.csv')
df.head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tripduration</th>
      <th>starttime</th>
      <th>stoptime</th>
      <th>start station id</th>
      <th>start station name</th>
      <th>start station latitude</th>
      <th>start station longitude</th>
      <th>end station id</th>
      <th>end station name</th>
      <th>end station latitude</th>
      <th>end station longitude</th>
      <th>bikeid</th>
      <th>usertype</th>
      <th>birth year</th>
      <th>gender</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>538</td>
      <td>5/1/2016 00:00:03</td>
      <td>5/1/2016 00:09:02</td>
      <td>536</td>
      <td>1 Ave &amp; E 30 St</td>
      <td>40.741444</td>
      <td>-73.975361</td>
      <td>497</td>
      <td>E 17 St &amp; Broadway</td>
      <td>40.737050</td>
      <td>-73.990093</td>
      <td>23097</td>
      <td>Subscriber</td>
      <td>1986.0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>1</th>
      <td>224</td>
      <td>5/1/2016 00:00:04</td>
      <td>5/1/2016 00:03:49</td>
      <td>361</td>
      <td>Allen St &amp; Hester St</td>
      <td>40.716059</td>
      <td>-73.991908</td>
      <td>340</td>
      <td>Madison St &amp; Clinton St</td>
      <td>40.712690</td>
      <td>-73.987763</td>
      <td>23631</td>
      <td>Subscriber</td>
      <td>1977.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>328</td>
      <td>5/1/2016 00:00:14</td>
      <td>5/1/2016 00:05:43</td>
      <td>301</td>
      <td>E 2 St &amp; Avenue B</td>
      <td>40.722174</td>
      <td>-73.983688</td>
      <td>311</td>
      <td>Norfolk St &amp; Broome St</td>
      <td>40.717227</td>
      <td>-73.988021</td>
      <td>23049</td>
      <td>Subscriber</td>
      <td>1980.0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1196</td>
      <td>5/1/2016 00:00:20</td>
      <td>5/1/2016 00:20:17</td>
      <td>3141</td>
      <td>1 Ave &amp; E 68 St</td>
      <td>40.765005</td>
      <td>-73.958185</td>
      <td>237</td>
      <td>E 11 St &amp; 2 Ave</td>
      <td>40.730473</td>
      <td>-73.986724</td>
      <td>19019</td>
      <td>Customer</td>
      <td>NaN</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>753</td>
      <td>5/1/2016 00:00:26</td>
      <td>5/1/2016 00:13:00</td>
      <td>492</td>
      <td>W 33 St &amp; 7 Ave</td>
      <td>40.750200</td>
      <td>-73.990931</td>
      <td>228</td>
      <td>E 48 St &amp; 3 Ave</td>
      <td>40.754601</td>
      <td>-73.971879</td>
      <td>16437</td>
      <td>Subscriber</td>
      <td>1981.0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

It appears that there is some good opportunity to break the data down into groups to look for some interesting trends. Some ideas are:
* Group on the gender column and see if there are more male or female riders.
* Do specific stations get used more than others? We can group on the station start or finish id.
* Group the data on the day of the week, to see if there is more utilization for a particular day, on average.
How about a few examples?

If we want to group by just the gender, then we pass this key (column name) to the `groupby` function as the sole argument. This example is the simplest form of grouping, so please check out [the docs](http://pandas.pydata.org/pandas-docs/stable/groupby.html) to get all the options!

```
groupedGender = df.groupby('gender')
print groupedGender
<pandas.core.groupby.DataFrameGroupBy object at 0x1133854d0>
```

The output shows that `groupby` returns a pandas DataFrameGroupBy object. Pandas has just made some internal calculations about the new gender groups and is ready to apply some operation on each of these groups. We can take a look at the available methods with the docstring/tab complete functionality of Rodeo!

![]({{ STATIC_URL }}/img/rodeo-pandas-docstring.png)


Getting back to the data, if we use the `count` method, we can see the total number of entries for each gender group. For reference, here's what the website says for the gender codes - "Gender (Zero=unknown; 1=male; 2=female)"

```
groupedGender.size()
gender
0    178710
1    783723
2    249847

# look at the size as a percentage of the whole (using the trip)
total = df.gender.count()
groupedGender.size() / total * 100
gender
0    14.741644
1    64.648679
2    20.609678
```

We can use a single column from the DataFrameGroupBy object and apply some aggregation function on it - how about the median and standard deviation of the trip durations for all three groups?

```
groupedGender['tripduration'].mean() / 60.
gender
0    35.923658
1    13.778720
2    16.198230

# Don't have to use the bracket notation
groupedGender.tripduration.std() / 60.
gender
0    193.417686
1     94.884313
2     91.675397
```

So there are some summary statistics for these groups (as an aside, you can use the `describe` function to get these statistics and more in one call). That's a whole lot of spread around the median, which probably means there are some outliers in the data (maybe people that kept the bike for days). Just a brief look at this even though it's outside the scope, because I'm sure you were all interested 😊

```
df[df.tripduration > 10000].tripduration.count()
5110
```

Our suspicions are confirmed - there are many bike rentals outside 2:45 even though the "max" is supposed to be 30 minutes. And the plot, just because we can (using [ggplot](http://yhat.github.io/ggplot/) of course):


```
df_short = df[df.tripduration < 10000]
df_short.tripduration = df_short.tripduration / 60.
ggplot(df_short, aes(x='tripduration')) + geom_histogram(bins=30) + xlab("Trip Duration (mins)") + ylab("Count")
```

### SWEET GGPLOT GOES HERE


One last example is looking at which are the five favorite start and end stations. We'll group the data based on the start and end station names, apply the count function, and sort the values is descending order. Here's the code for that:

```
groupedStart = df.groupby('start station name')
groupedStart['start station name'].count().sort_values(ascending=False)[:5]

start station name
Pershing Square North    12775
West St & Chambers St    10128
Lafayette St & E 8 St     9246
W 21 St & 6 Ave           9220
E 17 St & Broadway        9036

groupedEnd = df.groupby('end station name')
groupedEnd['end station name'].count().sort_values(ascending=False)[:5]

end station name
Pershing Square North    12511
West St & Chambers St    10189
Lafayette St & E 8 St     9459
E 17 St & Broadway        9273
W 21 St & 6 Ave           9268

```

Hopefully, the above examples helped introduce some basic uses for the grouping process in pandas to help enhance your analysis and whet your appetite for more! What ideas do you have for further analysis on this dataset? Can you conquer the last idea of looking at the days of the week? Please, take a look at the resources linked below for further investigation!


### More Resources
* [Pandas Docs](http://pandas.pydata.org/pandas-docs/stable/groupby.html)
* [Hadley Wickam - The Split-Apply-Combine Strategy for Data Analysis](http://www.jstatsoft.org/v40/i01/paper)
* [Data Analysis for Python book by Wes McKinney](http://shop.oreilly.com/product/0636920023784.do?cmp=af-prog-books-videos-lp-na_afp_book_mckinney_cj_12307942_7040302)
* [Also excellent series from Greg Reda](http://www.gregreda.com/2013/10/26/working-with-pandas-dataframes/)
* [Excellent into to pandas series by Tom Augspurger](http://tomaugspurger.github.io/modern-1.html)
