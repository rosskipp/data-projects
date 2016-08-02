# An Introduction to Grouping in Pandas

### What is this Grouping data you speak of?

Grouping can be a powerful tool for any data analyst to leverage while trying to get the most out of a dataset. The functionality in pandas is powerful, but can be tough to initially wrap your head around. Have no fear...we will get through this together.

http://9227-presscdn-0-11.pagely.netdna-cdn.com/wp-content/uploads/2016/05/IMG_9352-970x642.jpg

### Why would I want to group data?

Sometimes, you have a set of data that lends itself to being categorized or grouped. For example, say we have data on a wide variety of people. We may to perform analysis where we compare groups based on age, gender, birth month, shoe size, birth city...the options are as wide as our data provides!

The pandas `groupby` functionality draws from the `Split-Apply-Combine` method as described by Hadley Wickham (from the land of R). It's a great approach to solving data analysis problems, and his paper on the subject is worth a read (it's linked in the resourced section). To summarize, he states that an important tool for analyzing data comes from splitting the data into categories or groups based on some criteria, applying some type of function to each group (sum, mean, count, etc...), then combining the results.

Sounds like a handy tool. But how do I use it?


### Codes and Stuff

First, I’ll just state that I’m running pandas 0.18.1, just so we're on the same page.

```
>>> import pandas as pd
>>> pd.__version__
u’0.18.1'
```

I was looking around for some data to analyze, and came across [this data](https://www.citibikenyc.com/system-data) from Citi Bike, which is the NYC bike share program. It's pretty medium data at ~250MB CSV for a months worth of data. It seemed like there was potential here for some interesting findings, and applications of data grouping. Let's go down the rabbit hole...

http://media2.govtech.com/images/770*1000/Big+data.jpg

I started by unzipping the downloaded CSV from June 2016, and reading it into pandas with the `read_csv` function.

```
>>> df = pd.read_csv('data.csv')
>>> df.head()
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

Looking at this, it appears that there is some good opportunity to break the data down into groups to look for some interesting trends. Some ideas are:
* Group the data on day of the week, suand see if there is more utilization for a particular day, on average.
* Group on the gender column and see if there are more male or female riders.
* Do certain stations get used more? We can group on the station start or finish id.

How about a few examples of this functionality?

If we want to group by just the gender, then we pass this key (column) to the `groupby` function as the sole argument. This is the simplest form of grouping, so please checkout out [the docs](http://pandas.pydata.org/pandas-docs/stable/groupby.html) to get all the options!

```
>>> groupedGender = df.groupby('gender')
>>> print groupedGender
<pandas.core.groupby.DataFrameGroupBy object at 0x1133854d0>
```

This shows that `groupby` returns a pandas DataFrameGroupBy object. Pandas has just made some built in calcutaions about the new groups, and is ready to apply some type of computation or operation on each of these groups. We can take a look at the available methods with the docstring/tab complete functionality of Rodeo!

#### INSERT SWEET PICTURES OF RODEO

Getting back to the data, if we use the `count` method, we can see the total number of entries for each gender group. As a key, here's what the website says for the codes - Gender (Zero=unknown; 1=male; 2=female)

```
>>> groupedGender.size()
gender
0    178710
1    783723
2    249847
```

We can use a single column from the DataFrameGroupBy object and calculate some aggregation function on it - how about the median and standard deviation of the trip durations for all three groups?

```
>>> groupedGender['tripduration'].mean() / 60.
gender
0    35.923658
1    13.778720
2    16.198230

# Don't have to use the bracket notation
>>> groupedGender.tripduration.std() / 60.
gender
0    193.417686
1     94.884313
2     91.675397
```

So there's some summary statistics for these groups. That's a whooole lot of spread around the median...which probably means there's some outliers in the data (people that kept the bike for days).






### More Resources
* [Pandas Docs](http://pandas.pydata.org/pandas-docs/stable/groupby.html)
* [Hadley Wickam - The Split-Apply-Combine Strategy for Data Analysis](http://www.jstatsoft.org/v40/i01/paper)
* [Data Analysis for Python book by Wes McKinney](http://shop.oreilly.com/product/0636920023784.do?cmp=af-prog-books-videos-lp-na_afp_book_mckinney_cj_12307942_7040302)
* [Also excellent series from Greg Reda](http://www.gregreda.com/2013/10/26/working-with-pandas-dataframes/)
* [Excellent into to pandas series by Tom Augspurger](http://tomaugspurger.github.io/modern-1.html)
