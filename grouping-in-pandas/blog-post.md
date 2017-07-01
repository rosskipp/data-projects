# An Introduction to Grouping in Pandas

Grouping data is an integral part of many data analysis projects. The functionality for grouping in pandas is vast, but can be tough to grasp initially. Have no fear...we will get through a short introduction together using some data from NYC's beloved bike share program, Citi Bike.

![]({{ STATIC_URL }}/img/grouping-buddies.jpg)

### Why would I want to group data?

Most of the time, you have a set of data that lends itself to being categorized or grouped. As a general example, let's say we have data on a wide variety of people. We may perform an analysis where we compare groups in the data based on age, gender, birth month, shoe size, or birth city; the options are as numerous as the data points!

The pandas `groupby` functionality draws from the `Split-Apply-Combine` method as described by Hadley Wickham from the land of R. It's a great approach to solving data analysis problems, and his paper on the subject is worth a read (it's linked in the resources section).

To summarize, he states that a common methodology for analyzing data comes from splitting the data into categories or groups based on some criteria, applying some aggregation function to each group (sum, mean, count), then combining the results for analysis, visualization or other means of better understanding.

Here's a graphic I came across illustrating the process:

![]({{ STATIC_URL }}/img/split-apply-combine.jpg)
<center>From <u>Data Analysis in Python</u> by Wes McKinney</center>

Sounds handy, but how do I do it in pandas?

### Codes and Stuff

Just so we're on the same page, I’m running pandas `0.18.1`.

I was looking around for an intriguing dataset and came across [this data](https://www.citibikenyc.com/system-data) from Citi Bike, which is the NYC bike share program. It's pretty medium data at ~250MB CSV for one month's worth of data, and there was potential for some compelling findings with data grouping. Let's start down the rabbit hole...
<center>
<iframe src="//giphy.com/embed/swtiK9jRfE0zS" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="http://giphy.com/gifs/blue-adventure-time-rabbit-swtiK9jRfE0zS"></a></p>
</center>

```
df = pd.read_csv('data.csv')
df.head()
```

<div id="tableWrapper" style="overflow-x: scroll;">
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
</div>

It looks like there is a good opportunity to break the data down into groups to look for some interesting trends. Some ideas are:

- Group on the gender column and see if there are more male or female riders.
- Do specific stations get used more than others? We can group on the station start or finish id.
- Group the data on the day of the week, to see if there is more utilization for a particular day, on average.

### How about a few examples?

If we want to group by just the gender, then we pass this key (column name) to the `groupby` function as the sole argument. This example is the simplest form of grouping, so please check out [the docs](http://pandas.pydata.org/pandas-docs/stable/groupby.html) to get all the options!

```
groupedGender = df.groupby('gender')
print(groupedGender)
<pandas.core.groupby.DataFrameGroupBy object at 0x1133854d0>
```

The output shows that `groupby` returns a pandas `DataFrameGroupBy` object. Pandas has just made some internal calculations about the new gender groups and is ready to apply some operation on each of these groups.

We can take a look at the available methods with the docstring/tab complete functionality of [Rodeo](https://www.yhat.com/products/rodeo)!

![]({{ STATIC_URL }}/img/rodeo-pandas-docstring.png)

### Counts of groups

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

It looks like males make up the majority of Citi Bike riders (~65%). I was pretty surprised to see that male riders outnumbered female riders 3 to 1. I wonder if that's true of commuters in general, or if there's some other factor, like females tending to own their own bikes. A question for another post...

### Mean and Std Dev of groups

We can use a single column from the DataFrameGroupBy object and apply some aggregation function on it - how about the mean and standard deviation of the trip durations for all three groups?

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

Although males make up the majority of Citi Bike riders, there's not much of a difference in their trip durations. Interestingly, gender unknown riders take 2x as long of rides on average. These riders are likely single-use customers (when you purchase a one time pass at a Citi Bike kiosk you are not asked for your gender).

### More summary statistics

So there are some summary statistics for these groups (as an aside, you can use the `describe` function to get these statistics and more in one call). That's a whole lot of spread around the mean, which probably means there are some outliers in the data (maybe people that kept the bike for days). Just a brief look at this even though it's outside the scope, because I'm sure you were all interested 😊

```
df[df.tripduration > 10000].tripduration.count()
5110
```

Our suspicions are confirmed - there are many bike rentals outside 2:45 even though the "max" is supposed to be 30 minutes (or 45 if you're a Citi Bike member).

Brief aside / public service announcement, it costs up to $1200 to replace a Citi Bike. Don't be an outlier!

### A quick (gg)plot

Okay, back on track...the plot, just because we can (using [ggplot](http://yhat.github.io/ggplot/) of course):


```
df_short = df[df.tripduration < 10000]
df_short.tripduration = df_short.tripduration / 60.
ggplot(df_short, aes(x='tripduration')) + geom_histogram(bins=30) + xlab("Trip Duration (mins)") + ylab("Count")
```

<img src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAxgAAAJACAYAAAAO18BKAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1%2B/AAAIABJREFUeJzs3X9s1Pd9x/HX937Y97XvLncjuAlnNTG2ZwSsYLsdTsdBUZgC8wJrZyM1WcW0RoSCYmn9Y9q0aWm7H39MWjshIVWWpkhpVE0hsgmSp6aoLMbppmVitpd4MY0LlBqD4gWPO5/P5zvu9gfzlS9nfsT52N/Dfj6kyvhz9/3c%2B17xSX71%2B72zVSgUCgIAAAAAAzxuDwAAAABg5aBgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGN8bg%2BwHPL5vLq7uxUOh/Xcc88pnU7rxIkTunHjhiKRiDo7OxUIBCRJAwMDGhwclMfj0Z49e9TQ0CBJmpiY0MmTJ5XL5dTY2Ki9e/dKknK5nHp7e3X16lVVVVWpo6NDkUhEkjQ0NKSzZ8/KsizF43Ft3brVnQAAAACAZbIqzmD8%2B7//u9auXVv8/p133tH69ev10ksvqa6uTgMDA5Kkjz76SCMjIzp69Kief/559fX1qVAoSJL6%2Bvq0f/9%2BdXV16eOPP9bY2JgkaXBwULZtq6urS21tbTp9%2BrQkKZ1Oq7%2B/X4cOHdILL7yg/v5%2Bzc7OLvMzBwAAAJbXii8YN27c0IcffqiWlpbi2ujoaPFswpYtWzQ6OipJOn/%2BvDZv3iyv16toNKo1a9boypUrSiaTymQyisViJcfcvtfGjRt18eJFSdLY2Jjq6%2BsVCARk27bq6%2BuLpQQAAABYqVZ8wXjrrbf027/927Isq7iWSqUUDAYlSaFQSKlUSpKUTCYVDoeL9wuFQkokEiXr4XBYiUSi5BiPx6NAIKCZmZm77gUAAACsZCv6PRg/%2B9nPVF1drccff7x4ZmEht5ePT2v%2Bkqr7SSQSmp6edqwFg0FHKQEAAAAeNiu6YFy%2BfFnnz5/Xhx9%2BqFwup0wmo56eHgWDQU1PTysYDCqZTKq6ulpS6VmGRCKhcDh81/XbjwmHw8rn88pkMqqqqlIoFNKlS5ccx9TV1RW/P3funPr7%2Bx3z7ty5U7t27VqKKAAAAIBlsaILxu7du7V7925J0qVLl/Sv//qv%2BspXvqIf//jHGhoa0vbt2zU8PKympiZJUlNTk3p6etTW1qZkMqnr168rFovJsixVVlZqfHxcsVhMw8PD2rZtW/GYoaEh1dbWamRkpFgiGhoadObMGc3OzqpQKOjChQvFWSSptbW1%2BLjzgsGgpqamlMvlliOeu6qsrFQmk3F1Bp/Pp2g0Sh7/r5zykMjkTuThRB5O5OFEHqXIxKmc8sDirOiCcTfbt2/XiRMnNDg4qEceeUSdnZ2SpJqaGm3atEnHjx%2BX1%2BtVe3t78fKp9vZ2x8fUNjY2SpJaWlrU09OjY8eOybZtdXR0SJJs29aOHTvU3d0t6dbZCdu2izOEw%2BEFL4eanJxUNptd0ud/Pz6fz/UZ5uVyOddnIY9SZOJEHk7k4UQeTuRRikycyikPLM6qKRhPPvmknnzySUlSVVWVDh48uOD94vG44vF4yfq6det05MiRknWfz6cDBw4suFdzc7Oam5sXPzQAAADwkFnxnyIFAAAAYPlQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMVahUCi4PQRumZ2d1ezsrNz%2BT%2BLxeJTP512dwbIsVVRUaG5ujjxUXnlIZHIn8nAiDyfycCKPUmTiVC55RCIRV2d4mPncHgC/EggElEwmlc1mXZ3Dtm2l02lXZ/D7/YpEIkqlUuSh8spDIpM7kYcTeTiRhxN5lCITp3LJA4vHJVIAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKxiowNzf3ie6fTqeN7QUAAIDVxef2AFh6FRUV2rdvn5G9Tp06ZWQfAAAArEycwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMas6L%2BDkcvl9Morr%2BjmzZu6efOmmpqatHv3br399ts6d%2B6cqqurJUlPP/20GhsbJUkDAwMaHByUx%2BPRnj171NDQIEmamJjQyZMnlcvl1NjYqL179xYfo7e3V1evXlVVVZU6OjoUiUQkSUNDQzp79qwsy1I8HtfWrVtdSAEAAABYPiu6YPh8Ph08eFAVFRXK5/P6x3/8R12%2BfFmS9NRTT%2BmLX/yi4/6Tk5MaGRnR0aNHlUgk9Oqrr6qrq0uWZamvr0/79%2B9XLBbTa6%2B9prGxMTU0NGhwcFC2baurq0vvv/%2B%2BTp8%2Brc7OTqXTafX39%2BvFF19UoVBQd3e3NmzYoEAg4EYUAAAAwLJY8ZdIVVRUSLp1pqFQKNzzF/zR0VFt3rxZXq9X0WhUa9as0ZUrV5RMJpXJZBSLxSRJW7Zs0ejoaPGY%2BTMTGzdu1MWLFyVJY2Njqq%2BvVyAQkG3bqq%2Bv19jY2FI%2BVQAAAMB1K/oMhiTl83l1d3fr%2BvXr%2BvznP6%2Bamhr993//t959910NDw9r3bp1euaZZxQIBJRMJlVbW1s8NhQKKZFIyOPxKBwOF9fD4bASiYQkKZlMFm/zeDwKBAKamZlxrN%2B%2BFwAAALCSrfiC4fF4dPjwYc3OzuoHP/iBLl26pC984QvauXOnLMvST37yE7311lvav3%2B/kccrFAoPdL9EIqHp6WnHWjAYlM9n/j9JNps1up/f7ze630Lmc1iKPD4pr9e7LM/5XsopD4lM7kQeTuThRB5O5FGKTJzKKQ8szqpJLxAI6Nd//dc1MTGhJ598srje2tqqH/7wh5JKzzIkEgmFw%2BG7rt9%2BTDgcVj6fVyaTUVVVlUKhkC5duuQ4pq6urvj9uXPn1N/f75hx586d2rVrl8mnLenWG9RNWrt2rdH97iUajS7bYz0MyKMUmTiRhxN5OJGHE3mUIhOYsKILRiqVktfrVSAQUDab1c9//nN96UtfUjKZVCgUkiR98MEHqqmpkSQ1NTWpp6dHbW1tSiaTun79umKxmCzLUmVlpcbHxxWLxTQ8PKxt27YVjxkaGlJtba1GRkaKJaKhoUFnzpzR7OysCoWCLly4oN27dxdna21tVVNTk2PeYDCoqakp5XK55Yhn0SYnJ5f8MXw%2Bn6LRaFnkUVlZqUwm4%2BoM5ZSHRCZ3Ig8n8nAiDyfyKEUmTuWUBxZnRReM6elp9fb2Srp16dLnPvc5rV%2B/Xj09Pbp27Zosy1IkEtGzzz4rSaqpqdGmTZt0/Phxeb1etbe3y7IsSVJ7e7vjY2rnP9a2paVFPT09OnbsmGzbVkdHhyTJtm3t2LFD3d3dkm6dnbBtuzhbOBx2vEdj3uTkpPFLmkxbzvlyuZzrefh8PtdnmFcOeUhkcifycCIPJ/JwIo9SZOJUTnlgcVZ0wfjMZz6jw4cPl6x/5Stfuesx8Xhc8Xi8ZH3dunU6cuRIybrP59OBAwcW3Ku5uVnNzc2fYGIAAADg4bbiP6YWAAAAwPKhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAY3xuD4BfmZ2dld/vl89n9j9LOp02up9t20b3W4hlWZqZmVmSPD4pj8ezLM/5XsopD4lM7kQeTuThRB5O5FGKTJzKJQ8snvuvKhQFAgElk0lls1m3R7kn04VlIX6/X5FIRKlUyvU8bNtelud8L%2BWUh0QmdyIPJ/JwIg8n8ihFJk7lkgcWj0ukAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAY43N7gKWUy%2BX0yiuv6ObNm7p586aampq0e/dupdNpnThxQjdu3FAkElFnZ6cCgYAkaWBgQIODg/J4PNqzZ48aGhokSRMTEzp58qRyuZwaGxu1d%2B/e4mP09vbq6tWrqqqqUkdHhyKRiCRpaGhIZ8%2BelWVZisfj2rp1qztBAAAAAMtkRZ/B8Pl8OnjwoA4fPqxvfOMbunjxoi5fvqx33nlH69ev10svvaS6ujoNDAxIkj766CONjIzo6NGjev7559XX16dCoSBJ6uvr0/79%2B9XV1aWPP/5YY2NjkqTBwUHZtq2uri61tbXp9OnTkqR0Oq3%2B/n4dOnRIL7zwgvr7%2BzU7O%2BtOEAAAAMAyWdEFQ5IqKiok3TrTUCgUFAgENDo6WjybsGXLFo2OjkqSzp8/r82bN8vr9SoajWrNmjW6cuWKksmkMpmMYrFYyTG377Vx40ZdvHhRkjQ2Nqb6%2BnoFAgHZtq36%2BvpiKQEAAABWqhV9iZQk5fN5dXd36/r16/r85z%2BvmpoapVIpBYNBSVIoFFIqlZIkJZNJ1dbWFo8NhUJKJBLyeDwKh8PF9XA4rEQiUTxm/jaPx6NAIKCZmRnH%2Bu17AQAAACvZii8YHo9Hhw8f1uzsrF577bXiGYbbWZZl7PHmL6m6n0QioenpacdaMBiUz3frP0k%2Bn3/gve4nn88b2Wee3%2B83ut9C5nOY/%2Bomr9e7LM/5XsopD4lM7kQeTuThRB5O5FGKTJzKKQ8szqpJLxAIqLGxURMTEwoGg5qenlYwGFQymVR1dbWk0rMMiURC4XD4ruu3HxMOh5XP55XJZFRVVaVQKKRLly45jqmrqyt%2Bf%2B7cOfX39ztm3Llzp3bt2qVCoVB8U/mnFY1G9aUvfelT73O7tWvXGt3vXqLR6LI91sOAPEqRiRN5OJGHE3k4kUcpMoEJK7pgpFIpeb1eBQIBZbNZ/fznP9eXvvQlzczMaGhoSNu3b9fw8LCampokSU1NTerp6VFbW5uSyaSuX7%2BuWCwmy7JUWVmp8fFxxWIxDQ8Pa9u2bcVjhoaGVFtbq5GRkWKJaGho0JkzZzQ7O6tCoaALFy5o9%2B7dxdlaW1uLjzsvGAxqampK2WxW%2BXxer7zyyqfOoKGhwXjBmJycNLrfQnw%2Bn6LRqKamppTL5Zb88e6lsrJSmUzG1RnKKQ%2BJTO5EHk7k4UQeTuRRikycyikPLM6KLhjT09Pq7e2VdOvSpc997nNav369HnvsMZ04cUKDg4N65JFH1NnZKUmqqanRpk2bdPz4cXm9XrW3txcvn2pvb3d8TG1jY6MkqaWlRT09PTp27Jhs21ZHR4ckybZt7dixQ93d3ZJunZ2wbbs4WzgcdrxHY97k5KTrL%2Bz7yWazy/ZYuVxuWR9vIT6fz/UZ5pVDHhKZ3Ik8nMjDiTycyKMUmTiVUx5YnBVdMD7zmc/o8OHDJetVVVU6ePDggsfE43HF4/GS9XXr1unIkSMl6z6fTwcOHFhwr%2BbmZjU3N3/CqQEAAICH14r/mFoAAAAAy4eCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACM8bk9AH5ldnZWfr9fXq9XqVTK7XHuyrbtJX8My7I0MzMjv98vn8/dH1OPx7Msz/leyikPiUzuRB5O5OFEHk7kUYpMnMolDyye%2B68qFAUCASWTSWWzWbdHuad0Or3kj%2BH3%2BxWJRJRKpVzPw7btZXnO91JOeUhkcifycCIPJ/JwIo9SZOJULnlg8bhECgAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMT63B1hqN27cUG9vr1KplCzLUmtrq7Zt26a3335b586dU3V1tSTp6aefVmNjoyRpYGBAg4OD8ng82rNnjxoaGiRJExMTOnnypHK5nBobG7V3715JUi6XU29vr65evaqqqip1dHQoEolIkoaGhnT27FlZlqV4PK6tW7e6kAIAAACwPFZ8wfB4PHrmmWf0%2BOOPK5PJqLu7W%2BvXr5ckPfXUU/riF7/ouP/k5KRGRkZ09OhRJRIJvfrqq%2Brq6pJlWerr69P%2B/fsVi8X02muvaWxsTA0NDRocHJRt2%2Brq6tL777%2Bv06dPq7OzU%2Bl0Wv39/XrxxRdVKBTU3d2tDRs2KBAIuBEFAAAAsORW/CVSoVBIjz/%2BuCSpsrJSjz76qJLJ5F3vPzo6qs2bN8vr9SoajWrNmjW6cuWKksmkMpmMYrGYJGnLli0aHR0tHjN/ZmLjxo26ePGiJGlsbEz19fUKBAKybVv19fUaGxtbyqcLAAAAuGrFn8G43dTUlK5du6ZYLKbLly/r3Xff1fDwsNatW6dnnnlGgUBAyWRStbW1xWNCoZASiYQ8Ho/C4XBxPRwOK5FISJKSyWTxNo/Ho0AgoJmZGcf67XsBAAAAK9WqKRiZTEavv/669u7dq8rKSn3hC1/Qzp07ZVmWfvKTn%2Bitt97S/v37jTxWoVC4730SiYSmp6cda8FgUD6fT4VCQTdv3jQyy1Lw%2B/1L/hg%2Bn8/x1U1er3dZnvO9lFMeEpnciTycyMOJPJzIoxSZOJVTHlicVZHezZs39frrr2vLli3asGGDJBXf3C1Jra2t%2BuEPfyip9CxDIpFQOBy%2B6/rtx4TDYeXzeWUyGVVVVSkUCunSpUuOY%2Brq6iRJ586dU39/v2POnTt3ateuXSoUChofHzcbgkFr165dtseKRqPL9lgPA/IoRSZO5OFEHk7k4UQepcgEJqyKgvHmm29q7dq1amtrK64lk0mFQiFJ0gcffKCamhpJUlNTk3p6etTW1qZkMqnr168rFovJsixVVlZqfHxcsVhMw8PD2rZtW/GYoaEh1dbWamRkpFgiGhoadObMGc3OzqpQKOjChQvavXu3pFulpqmpyTFnMBjU1NSUstnskmfyaUxOTi75Y/h8PkWjUU1NTSmXyy35491LZWWlMpmMqzOUUx4SmdyJPJzIw4k8nMijFJk4lVMeWJwVXzAuX76s9957TzU1Nfr%2B978v6dZH0r733nu6du2aLMtSJBLRs88%2BK0mqqanRpk2bdPz4cXm9XrW3t8uyLElSe3u742Nq5z/WtqWlRT09PTp27Jhs21ZHR4ckybZt7dixQ93d3ZJunaGwbVvSrfdw3P7%2BjHmTk5Ouv7DvZzkLUC6Xc71w%2BXw%2B12eYVw55SGRyJ/JwIg8n8nAij1Jk4lROeWBxVnzB%2BOxnP6uXX365ZH2%2BHCwkHo8rHo%2BXrK9bt05HjhwpWff5fDpw4MCCezU3N6u5ufkTTAwAAAA8vFb8x9QCAAAAWD4UDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgjM/tAfArs7Oz8vv98nq9SqVSbo9zV7ZtL/ljWJalmZkZ%2Bf1%2B%2BXzu/ph6PJ5lec73Uk55SGRyJ/JwIg8n8nAij1Jk4lQueWDx3H9VoSgQCCiZTCqbzbo9yj2l0%2Bklfwy/369IJKJUKuV6HrZtL8tzvpdyykMikzuRhxN5OJGHE3mUIhOncskDi8clUgAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGPpG5ubmy3AsAAADlwef2AHi4VFRUaN%2B%2BfUb2OnXqlJF9AAAAUD44gwEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwZsX/ob0bN26ot7dXqVRKlmWppaVFbW1tSqfTOnHihG7cuKFIJKLOzk4FAgFJ0sDAgAYHB%2BXxeLRnzx41NDRIkiYmJnTy5Enlcjk1NjZq7969kqRcLqfe3l5dvXpVVVVV6ujoUCQSkSQNDQ3p7NmzsixL8XhcW7dudScIAAAAYBms%2BDMYHo9HzzzzjI4ePaqvf/3r%2Bo//%2BA9NTk7qnXfe0fr16/XSSy%2Bprq5OAwMDkqSPPvpIIyMjOnr0qJ5//nn19fWpUChIkvr6%2BrR//351dXXp448/1tjYmCRpcHBQtm2rq6tLbW1tOn36tCQpnU6rv79fhw4d0gsvvKD%2B/n7Nzs66EwQAAACwDFZ8wQiFQnr88cclSZWVlXr00UeVSCQ0OjpaPJuwZcsWjY6OSpLOnz%2BvzZs3y%2Bv1KhqNas2aNbpy5YqSyaQymYxisVjJMbfvtXHjRl28eFGSNDY2pvr6egUCAdm2rfr6%2BmIpAQAAAFaiFV8wbjc1NaVr166ptrZWqVRKwWBQ0q0SkkqlJEnJZFLhcLh4TCgUUiKRKFkPh8NKJBIlx3g8HgUCAc3MzNx1LwAAAGClKrv3YJw4cUKdnZ0l62%2B88YY6OjoWvW8mk9Hrr7%2BuvXv3qrKysuR2y7IWvfed5i%2BpupdEIqHp6WnHWjAYlM/nU6FQ0M2bN43NU878fv%2BC6z6fz/HVTV6v965zLpdyykMikzuRhxN5OJGHE3mUIhOncsoDi1N26X39619fsGAcOnRo0QXj5s2bev3117VlyxZt2LBB0q1f5qenpxUMBpVMJlVdXS2p9CxDIpFQOBy%2B6/rtx4TDYeXzeWUyGVVVVSkUCunSpUuOY%2Brq6iRJ586dU39/v2POnTt3ateuXSoUChofH1/Uc33YrF279p63R6PRZZrk4UAepcjEiTycyMOJPJzIoxSZwISyKRgXLlyQJOXzeV28eNFxFuDChQvFT3hajDfffFNr165VW1tbca2pqUlDQ0Pavn27hoeH1dTUVFzv6elRW1ubksmkrl%2B/rlgsJsuyVFlZqfHxccViMQ0PD2vbtm2OvWprazUyMlIsEQ0NDTpz5oxmZ2dVKBR04cIF7d69W5LU2tpafMx5wWBQU1NTymazi36uD5vJyckF130%2Bn6LRqKamppTL5ZZ5KqfKykplMhlXZyinPCQyuRN5OJGHE3k4kUcpMnEqpzywOGVTMBoaGmRZlgqFgurr6x23PfbYY/rWt761qH0vX76s9957TzU1Nfr%2B978vSXr66af1W7/1Wzpx4oQGBwf1yCOPFM%2Ba1NTUaNOmTTp%2B/Li8Xq/a29uLl0%2B1t7c7Pqa2sbFRktTS0qKenh4dO3ZMtm0Xz7TYtq0dO3aou7tb0q0zFLZtS7r1Ho7b358xb3Jy0vUX9nK6X5nK5XKuFy6fz%2Bf6DPPKIQ%2BJTO5EHk7k4UQeTuRRikycyikPLE7ZFIx8Pi/p1i/hd1469Gl89rOf1csvv7zgbQcPHlxwPR6PKx6Pl6yvW7dOR44cKVn3%2BXw6cODAgns1Nzerubn5E0wMAAAAPLzK7lOkTJYLAAAAAMurbM5gzLt48aL%2B/M//XENDQyWfsnT58mWXpgIAAADwIMquYDz33HOqr6/X3//936uqqsrtcQAAAAB8AmVXMEZGRvTTn/5UHk/ZXb0FAAAA4D7K7rf4HTt2aHBw0O0xAAAAACxC2Z3BePLJJ7Vnzx59%2Bctf1mOPPea47Tvf%2BY5LUwEAAAB4EGVXMFKplH73d39X2WxWv/zlL90eBwAAAMAnUHYF45VXXnF7BAAAAACLVHYF48KFC3e9bf369cs4CQAAAIBPquwKRkNDgyzLUqFQKK5ZliVJunnzpltjAQAAAHgAZVcw8vm84/tr167p29/%2BtuLxuEsTAQAAAHhQZfcxtXd67LHH9A//8A/6sz/7M7dHAQAAAHAfZV8wJOn8%2BfOamZlxewwAAAAA91F2l0jF4/FBucsNAAAgAElEQVTiey4kaWZmRiMjI/rLv/xLF6cCAAAA8CDKrmC88MILju%2Brq6u1ZcsWNTY2ujQRAAAAgAdVdgXj4MGDbo8AAAAAYJHK7j0Y2WxWL7/8stavX69AIKD169fr5Zdf1tzcnNujAQAAALiPsjuD8Sd/8id699139f3vf19PPPGEfvGLX%2Biv/uqvlEgk9L3vfc/t8QAAAADcQ9kVjBMnTmh4eFhr1qyRJDU1NamlpUVbtmyhYAAAAABlruwukbr9L3g/yDoAAACA8lF2BaOzs1PPPvus3nrrLX3wwQf60Y9%2BpN/7vd9TZ2en26MBAAAAuI%2Byu0Tq7/7u7/TXf/3XOnr0qCYmJhSLxfTVr35Vf/EXf%2BH2aAAAAADuo2zOYPz0pz/Vn/7pn6qiokLf%2Bc53NDY2ppmZGX344YfKZDL6z//8T7dHBAAAAHAfZVMw/vZv/1Y7duxY8LZdu3bpb/7mb5Z5IgAAAACfVNlcIjU0NKRnnnlmwdt2796tP/qjP1rmiZbf7Oys/H6/vF6vUqmU2%2BMsC9u2F1y3LEszMzPy%2B/3y%2Bdz9MfV4PHedc7mUUx4SmdyJPJzIw4k8nMijFJk4lUseWDz3X1X/L5FIaG5ubsEfqGw2q2Qy6cJUyysQCCiZTCqbzbo9yrJJp9MLrvv9fkUiEaVSKdfzsG37rnMul3LKQyKTO5GHE3k4kYcTeZQiE6dyyQOLVzaXSG3YsEE//vGPF7ztxz/%2BsTZs2LDMEwEAAAD4pMqmYPzxH/%2BxXnzxRfX09Cifz0uS8vm8enp6dPjwYX3zm990eUIAAAAA91M2l0g999xzunbtmg4ePKhMJqNHH31U//M//6PKykp9%2B9vf1le/%2BlW3RwQAAABwH2VTMCTpm9/8pl544QX927/9mz7%2B%2BGOtWbNGTz31lMLhsNujAQAAAHgAZVUwJCkcDt/106QAAAAAlLeyeQ8GAAAAgIcfBQMAAACAMRQMAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAY43N7gKX25ptv6mc/%2B5mqq6t15MgRSdLbb7%2Btc%2BfOqbq6WpL09NNPq7GxUZI0MDCgwcFBeTwe7dmzRw0NDZKkiYkJnTx5UrlcTo2Njdq7d68kKZfLqbe3V1evXlVVVZU6OjoUiUQkSUNDQzp79qwsy1I8HtfWrVuX%2B%2BkDAAAAy2rFF4ytW7fqN3/zN9Xb2%2BtYf%2Bqpp/TFL37RsTY5OamRkREdPXpUiURCr776qrq6umRZlvr6%2BrR//37FYjG99tprGhsbU0NDgwYHB2Xbtrq6uvT%2B%2B%2B/r9OnT6uzsVDqdVn9/v1588UUVCgV1d3drw4YNCgQCy/n0AQAAgGW14i%2BReuKJJ2Tb9gPdd3R0VJs3b5bX61U0GtWaNWt05coVJZNJZTIZxWIxSdKWLVs0OjpaPGb%2BzMTGjRt18eJFSdLY2Jjq6%2BsVCARk27bq6%2Bs1Nja2BM8QAAAAKB8r/gzG3bz77rsaHh7WunXr9MwzzygQCCiZTKq2trZ4n1AopEQiIY/Ho3A4XFwPh8NKJBKSpGQyWbzN4/EoEAhoZmbGsX77XgAAAMBKtioLxhe%2B8AXt3LlTlmXpJz/5id566y3t37/fyN6FQuGB7pdIJDQ9Pe1YCwaD8vl8KhQKunnzppF5yp3f719w3efzOb66yev13nXO5VJOeUhkcifycCIPJ/JwIo9SZOJUTnlgcVZlevNv7pak1tZW/fCHP5RUepYhkUgoHA7fdf32Y8LhsPL5vDKZjKqqqhQKhXTp0iXHMXV1dcXvz507p/7%2BfsdcO3fu1K5du1QoFDQ%2BPm70OZertWvX3vP2aDS6TJM8HMijFJk4kYcTeTiRhxN5lCITmLAqCsadZxWSyaRCoZAk6YMPPlBNTY0kqampST09PWpra1MymdT169cVi8VkWZYqKys1Pj6uWCym4eFhbdu2rXjM0NCQamtrNTIyUiwRDQ0NOnPmjGZnZ1UoFHThwgXt3r27OENra6uampoccwWDQU1NTSmbzS5ZFuVmcnJywXWfz6doNKqpqSnlcrllnsqpsrJSmUzG1RnKKQ%2BJTO5EHk7k4UQeTuRRikycyikPLM6KLxhvvPGGLl26pHQ6re9%2B97vatWuXLl68qGvXrsmyLEUiET377LOSpJqaGm3atEnHjx%2BX1%2BtVe3u7LMuSJLW3tzs%2Bpnb%2BY21bWlrU09OjY8eOybZtdXR0SJJs29aOHTvU3d0t6dbZidvfbB4Ohx3v0Zg3OTnp%2Bgt7Od2vTOVyOdcLl8/nc32GeeWQh0QmdyIPJ/JwIg8n8ihFJk7llAcWZ8UXjPlf%2BG/X3Nx81/vH43HF4/GS9XXr1hX/jsbtfD6fDhw4sOBezc3N93wsAAAAYKVZ8R9TCwAAAGD5UDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDDgmrm5ubvels1mNTExoWw2%2B6n3AgAAwPLxuT0AVq%2BKigrt27fPyF6nTp0ysg8AAAA%2BHc5gAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhr/kXUZmZ2fl9/vl9XqVSqXcHuehY9v2kuzr8XiWbO8HZVmWZmZm5Pf75fO5/7IlEyfycCIPJ/JwIo9SZOJULnlg8dx/VaEoEAgomUwqm826PcpDKZ1OL8m%2Btm0v2d4Pyu/3KxKJKJVKlcXPB5k4kYcTeTiRhxN5lCITp3LJA4vHJVIAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAY3xuD7DU3nzzTf3sZz9TdXW1jhw5IklKp9M6ceKEbty4oUgkos7OTgUCAUnSwMCABgcH5fF4tGfPHjU0NEiSJiYmdPLkSeVyOTU2Nmrv3r2SpFwup97eXl29elVVVVXq6OhQJBKRJA0NDens2bOyLEvxeFxbt251IQEAAABg%2Baz4Mxhbt27VH/zBHzjW3nnnHa1fv14vvfSS6urqNDAwIEn66KOPNDIyoqNHj%2Br5559XX1%2BfCoWCJKmvr0/79%2B9XV1eXPv74Y42NjUmSBgcHZdu2urq61NbWptOnT0u6VWL6%2B/t16NAhvfDCC%2Brv79fs7OwyPnMAAABg%2Ba34gvHEE0/Itm3H2ujoaPFswpYtWzQ6OipJOn/%2BvDZv3iyv16toNKo1a9boypUrSiaTymQyisViJcfcvtfGjRt18eJFSdLY2Jjq6%2BsVCARk27bq6%2BuLpQQAAABYqVZ8wVhIKpVSMBiUJIVCIaVSKUlSMplUOBwu3i8UCimRSJSsh8NhJRKJkmM8Ho8CgYBmZmbuuhcAAACwkq3492A8CMuyjO01f0nV/SQSCU1PTzvWgsGgfD6fCoWCbt68aWym1cLv9y/Jvl6vd8n2flA%2Bn8/x1W1k4kQeTuThRB5O5FGKTJzKKQ8szqpMLxgManp6WsFgUMlkUtXV1ZJKzzIkEgmFw%2BG7rt9%2BTDgcVj6fVyaTUVVVlUKhkC5duuQ4pq6urvj9uXPn1N/f75hr586d2rVrlwqFgsbHx5fiqa9oa9eudXuEJReNRt0eoeyQiRN5OJGHE3k4kUcpMoEJq6Jg3HlWoampSUNDQ9q%2BfbuGh4fV1NRUXO/p6VFbW5uSyaSuX7%2BuWCwmy7JUWVmp8fFxxWIxDQ8Pa9u2bY69amtrNTIyUiwRDQ0NOnPmjGZnZ1UoFHThwgXt3r27OENra2vxcecFg0FNTU0pm80uZRwr1uTk5JLsW1lZqUwmsyR7Pyifz6doNKqpqSnlcjlXZ5HI5E7k4UQeTuThRB6lyMSpnPLA4qz4gvHGG2/o0qVLSqfT%2Bu53v6tdu3Zp%2B/btev311zU4OKhHHnlEnZ2dkqSamhpt2rRJx48fl9frVXt7e/Hyqfb2dsfH1DY2NkqSWlpa1NPTo2PHjsm2bXV0dEiSbNvWjh071N3dLenW2Ynb32weDocd79GYNzk56foL%2B2G1VMXM5/OVTenL5XJlMQuZOJGHE3k4kYcTeZQiE6dyygOLs%2BILxvwv/Hc6ePDgguvxeFzxeLxkfd26dcW/o3E7n8%2BnAwcOLLhXc3OzmpubP8G0AAAAwMNtVX6KFAAAAIClQcEAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMLAizM3NleVeAAAAq43P7QEAEyoqKrRv3z4je506dcrIPgAAAKsRZzAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgjM/tAfArs7Oz8vv98nq9SqVSbo%2Bzqtm2Xfy3x%2BNxfO8Gy7I0MzMjv98vn8/9ly2ZOJGHE3k4kYcTeZQiE6dyyQOL5/6rCkWBQEDJZFLZbNbtUVa9dDpd/Ldt247v3eD3%2BxWJRJRKpcri54NMnMjDiTycyMOJPEqRiVO55IHF4xIpAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMAAAAAMZQMAAAAAAYQ8EAAAAAYAwFAwAAAIAxFAwAAAAAxlAwAAAAABhDwQAAAABgDAUDAAAAgDEUDAAAAADG%2BNwewE3f%2B973FAgEZFmWPB6PDh06pHQ6rRMnTujGjRuKRCLq7OxUIBCQJA0MDGhwcFAej0d79uxRQ0ODJGliYkInT55ULpdTY2Oj9u7dK0nK5XLq7e3V1atXVVVVpY6ODkUiEdeeLwAAALDUVvUZDMuy9Id/%2BIc6fPiwDh06JEl65513tH79er300kuqq6vTwMCAJOmjjz7SyMiIjh49queff159fX0qFAqSpL6%2BPu3fv19dXV36%2BOOPNTY2JkkaHByUbdvq6upSW1ubTp8%2B7c4TBQAAAJbJqi4YkoolYd7o6Ki2bt0qSdqyZYtGR0clSefPn9fmzZvl9XoVjUa1Zs0aXblyRclkUplMRrFYrOSY2/fauHGjLl68uFxPCwAAAHDFqr5ESpJeffVVeTwetba2qrW1ValUSsFgUJIUCoWUSqUkSclkUrW1tcXjQqGQEomEPB6PwuFwcT0cDiuRSBSPmb/N4/EoEAhoZmZGVVVVy/X0AAAAgGW1qgvG17/%2B9WKJ%2BMEPfqBHH3205D6WZRl7vNvPliQSCU1PTztuDwaD8vl8KhQKunnzprHHxSfn9/uL//Z6vY7v3eDz%2BRxf3UYmTuThRB5O5OFEHqXIxKmc8sDirOr0QqGQJKm6ulobNmzQlStXFAwGNT09rWAwqGQyqerq6uJ9589MSLcKQjgcvuv67ceEw2Hl83llMpni2Ytz586pv7/fMc/OnTu1a9cuFQoFjY%2BPL%2Blzx72tXbvW7REWFI1G3R6h7JCJE3k4kYcTeTiRRykygQmrtmDMzc2pUCiosrJSc3Nz%2BvnPf66dO3eqqalJQ0ND2r59u4aHh9XU1CRJampqUk9Pj9ra2pRMJnX9%2BnXFYjFZlqXKykqNj48rFotpeHhY27ZtKx4zNDSk2tpajYyMqK6urvj4ra2txb3nBYNBTU1NKZvNLl8QWNDk5GTx35WVlcpkMi5Oc%2Bv/SYlGo5qamlIul3N1FolM7kQeTuThRB5O5FGKTJzKKQ8szqotGKlUSv/0T/8ky7KUz%2Bf1G7/xG2poaNC6det04sQJDQ4O6pFHHlFnZ6ckqaamRps2bdLx48fl9XrV3t5evHyqvb3d8TG1jY2NkqSWlhb19PTo2LFjsm1bHR0dxccPh8OO927Mm5ycdP2FDTlKns/nK5vSl8vlymIWMnEiDyfycCIPJ/IoRSZO5ZQHFmfVFoxoNKpvfOMbJetVVVU6ePDggsfE43HF4/GS9XXr1unIkSMl6z6fTwcOHPj0w2JZzc3NqaKiovh9Op02sg8AAMBqsGoLBnA3FRUV2rdv36fe59SpUwamAQAAeLis%2Br%2BDAQAAAMAcCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGAAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoGAAAAAGMoGMASmZubM7ZXKpUythcAAMBS8rk9AH5ldnZWfr9fXq%2BXXyhXgIqKCu3bt8/IXqdOndLMzIz8fr98Pvdfth6PR7ZtuzqDZVllkwl5OJGHE3k4kUcpMnEqlzyweO6/qlAUCASUTCaVzWbdHgVlqKqqSqlUqix%2BPmzbVjqddnUGv9%2BvSCRSFpmQhxN5OJGHE3mUIhOncskDi8clUgAAAACMoWAAAAAAMIaCAQAAAMAYCgYAAAAAYygYAAAAAIyhYAAAAAAwhoIBAAAAwBgKBgAAAABjKBgAAAAAjKFgAAAAADCGggEAAADAGAoG8BCYm5vTxMSEstmskb0AAACWis/tAQDcX0VFhfbt22dkr1OnThnZBwAAYCGcwQAAAABgDAUDAAAAgDEUDAAAAADGUDAAAAAAGEPBAAAAAGAMBQMAAACAMRQMYJUx8Xcw0um0sb0AAMDKwt/BAFYZ/qYGAABYShSMJfbhhx/qRz/6kQqFglpaWrR9%2B3a3RwIAAACWDJdILaF8Pq9//ud/1te%2B9jUdPXpU7733niYnJ90eCzDG5CVSXG4FAMDKwBmMJXTlyhWtWbNGkUhEkrR582adP39ea9eudXkywAyTl1u98cYbn%2Bj%2B2WxWExMTC942NzeniooKE2MBAIBPiIKxhJLJpMLhcPH7cDisK1euuDgRUL7cLCt3k8lkVFlZed/7zb/p/V4oPQCA1YKC4ZJEIqHp6WnHWjAYlM/nU6FQUD6f11e/%2BtVP/Ti/9mu/9qn3AB42psrKqVOnyq70SAsXn3ud0fmke33auR6kcD3oXos1n8dSPL9PaqE85ubmVF1dbWKsB%2BLz%2BRxf3eT1euX3%2B12doZzykMjkTuWUBxbHKhQKBbeHWKl%2B%2Bctf6u2339bXvvY1SdLAwIAsy9L27dv1L//yL%2Brv73fc/4knntDv//7vO856rFaJRELnzp1Ta2sreYg8FkImTuThRB5O5OFEHqXIxIk8Ph3e5L2EYrGYrl%2B/rv/93/9VLpfT%2B%2B%2B/r6amJklSa2urDh06VPzfl7/8Zf3iF78oOauxWk1PT6u/v588/h95lCITJ/JwIg8n8nAij1Jk4kQenw7nf5aQx%2BPR7/zO7%2BgHP/iBCoWCmpubi2/wDofDNGIAAACsOBSMJdbY2KjGxka3xwAAAACWBZdIAQAAADDG%2B61vfetbbg8BqVAoqKKiQk8%2B%2BaSxTzx5mJGHE3mUIhMn8nAiDyfycCKPUmTiRB6fDpdIlYEPP/xQP/rRj1QoFOT3%2B7V9%2B3a3R1p2N27cUG9vr1KplCzLUktLi3bt2qV0Oq1XX31VN27cUCQSUWdnpwKBgNvjLot8Pq/u7m6Fw2E999xzamtr04kTJ1ZlFpI0OzurU6dO6aOPPpJlWdq/f/%2BqzmRgYED/9V//Jev/2rvzoKjrx4/jz90NFGQXEWQVUAxUwAM18yKPzPs2r/FuPGrQmYxsmppxrGa0Zuof%2BKdpnLRy1NHQzDNHGxsV884jMVFDFEEZQYFFTcRlf38w7k8UPL5%2BZMvP6/EXfPZzvPcFu/Daz2Wx4HQ6TZnHxo0bOXv2LA0aNGDu3LlA1SVh78%2BgR48e3vkzMjI4duwYVquVwYMH07JlS18N/bmoKY8dO3Zw9uxZbDYbjRo1qnYvFjPmcU9mZia7d%2B%2BmW7du3mlmzePgwYMcPnwYq9VKq1atvOeHmjGP/Px8tm7dSmVlJVarlWHDhpkmD6NpD4aPVVZWsmrVKqZPn07Pnj3Ztm0bLVq0qNPro/8bVFRU0Lx5c9544w0SExPZvHkzMTExHDp0iPDwcMaPH09ZWRnZ2dnExsb6erh14sCBA1RWVuJ2u2nfvj27du0ybRYAmzdvJjY2llGjRtG5c2fq16/P3r17TZlJSUkJ27ZtY%2B7cuXTr1o1Tp07hdrvJysoyVR4BAQF06tSJrKwsunTpAlDr6%2BTq1avs2bOH5ORk4uLiWLduHd26dcNisfj4WRinpjwABg4cSNeuXbly5QqXLl0iJibG1HmUlpZy4MABPB4PnTt3xs/Pj8LCQnbv3m26PHJycjh69CgzZ86kW7duNGnSBH9/f9PmsX79evr06cPAgQNxOBzs2rWLjh07muL1YjSdg%2BFj%2Bfn5hIaG0rBhQ2w2G%2B3atePMmTO%2BHlads9vtNG3aFIB69eoRFhaGy%2BUiKyuLjh07AtChQweysrJ8Ocw6U1payrlz53jllVe808yaBVTtvcjNzaVTp05A1U2Y6tevb9pM6tWrh81mo6KiArfbTUVFBXa73XR5REdHExAQUG1abRmcOXOGdu3aYbPZCAkJITQ0lPz8/Dof8/NUUx6xsbFYrVV/6qOionC5XIB58wDYvn07AwcOrDYtKyvLlHkcOXKEnj17YrPZALwfbpo1j6CgIMrLy4Gqvzt2ux0wx%2BvFaDpEysfKysqqXa7W4XCY/pe2uLiYgoICoqKiuHnzJkFBQUBVCbl586aPR1c3tm/fzoABA7xvdIBps4CqT%2BwDAwPZsGEDBQUFREREMHjwYNNmEhAQQFJSEqmpqfj5%2BREbG0tsbKxp87hfbRmUlZURFRXlnc9ut3v/2TaLY8eO0b59e8C8eWRlZeFwOHA6ndWmmzWPa9eucfHiRXbu3Imfnx8DBw4kIiLCtHn079%2Bf7777ju3btwMwa9YswLy/H89CezDkX6W8vJz09HSGDBlS40lVZtgdee%2BY0KZNm%2BLxeGqdzwxZ3FNZWcmVK1fo0qULycnJ%2BPv7s3fv3ofmM0sm169fZ//%2B/aSkpPDBBx9w584d/vzzz4fmM0sej6IMquzZswebzeYtGGZUUVFBRkYGffv29fVQ/jUqKyu5ffs2b7/9NgMGDCA9Pd3XQ/KpTZs2MWTIEObPn8%2BgQYPYuHGjr4f0n6WC4WN2u53S0lLv9y6Xy7Q34HO73aSnp9OhQwfi4%2BOBqt2V9%2B6iWVZWZopzU3Jzczlz5gxpaWn89NNP5OTksH79elNmcc%2B9G1NGRkYCkJCQwJUrV0ybyeXLl2nevDmBgYFYrVYSEhK4dOmSafO4X20ZPPiJo5nea48dO8a5c%2BcYO3asd5oZ87h%2B/TolJSV88803pKWl4XK5WLJkCTdu3DDt32KHw0FCQgIAkZGRWK1Wbt26Zdo88vLyvHm0bdvWe0SJGV8vz0oFw8ciIyO9b3p3794lMzOTuLg4Xw/LJzZu3Ejjxo3p3r27d1pcXBzHjx8H4MSJE6bIpn///syfP5%2BUlBTGjRvHyy%2B/zJgxY2jdurXpsrgnKCiI4OBgioqKgKoTE8PDw035%2BwEQFhZGXl4eFRUVeDwezp8/T%2BPGjU2Zx4N7%2BWrLIC4ujszMTO7evUtxcTHXr1/3FtYXyYN5nDt3jn379jFp0iReeun/j4o2Yx5Op5MPP/yQlJQUUlJScDgcJCcnExQURFxcHKdOnTJVHgDx8fHk5OQAUFRUhNvtJjAw0LR5hIaGcuHCBQDOnz9PaGgoYJ7Xi5EsnkcdgyF14v7L1Hbq1IlevXr5ekh1Ljc3l%2B%2B//57w8HDvIQ39%2BvUjMjKStWvX4nK5CA4OZvz48TWetPeiunDhAvv27WPy5MncunXL1FkUFBSwadMm3G43ISEhjB49msrKStNm8vvvv3P8%2BHEsFgtNmzZl5MiRlJeXmyqPdevWceHCBf755x8aNGhA3759iY%2BPJz09vcYMMjIyOHr0KDab7YW8zGRNeWRkZOB2u70ZREVFMXz4cMCcedy7UARAWloa77zzDoGBgYA580hMTGTjxo0UFBRgs9kYNGgQLVq0AMyZh9PpZOvWrbjdbl566SWGDRvmvQDNi56H0VQwRERERETEMDpESkREREREDKOCISIiIiIihlHBEBERERERw6hgiIiIiIiIYVQwRERERETEMCoYIiIiIiJiGBUMERERERExjAqGiIiIiIgYRgVDREREREQMo4IhIiIiIiKGUcEQERERERHDqGCIiIiIiIhhVDBERERERMQwKhgiIiIiImIYFQwRERERETGMCoaIiIiIiBhGBUNERERERAyjgiEiIiIiIoZRwRARqSOLFy9m7ty5vh7GM3mez%2BHq1askJCRQUVHx1MtWVlZit9vJy8t7pjGkpKSwdOnSZ1qHiIjZWTwej8fXgxAR%2Ba%2Bx2%2B1YLBYAbt68Sb169bDZbFgsFpYsWcKkSZMM3d7UqVNZu3Yt9evXB6BFixaMGDGCjz76CLvdbui27tm5cyezZ88mJyfnuaz/QSkpKTRv3pz58%2BfXyfZqkp%2BfT1JSEjk5OVit%2BgxOROR/oXdPEZH/QVlZGS6XC5fLRXR0NFu3bvVOq6lcuN3uZ9qexWJhwYIFlJaWUlhYyLJly8jIyOMLrEIAAAcPSURBVKBXr16Ul5c/9fo8Hg%2BP%2B3zJ4/F4S9Tzdvv2bVasWMGUKVPqZHu1iYyMpGXLlmzZssWn4xAR%2BS9TwRAReUY1/bO%2BcOFCJk6cyOTJkwkODmbVqlUsXLiQGTNmAJCdnY3VamXp0qVERkYSFRVFWlraE23P39%2BfV199lc2bN1NQUMDy5cu925w5c6Z3vnvbuKdXr1588sknJCUlERQUxKVLl1i2bBlt2rTB4XDQqlUrli1bBoDL5WLkyJHk5uZit9txOBwUFRVVew4AP//8M%2B3ataNRo0b079%2Bfs2fPeh9r1qwZqampJCYmEhISwpQpU2o9/Gn//v04nU6cTme18X766af06NEDu93OmDFjuHbtGpMmTSI4OJgePXp4D4lyu91YrVZyc3MBmDZtGu%2B99x5Dhw7F4XDw2muvcfHiRe/Pa968eTidTho2bEjHjh3JysrybrdPnz5s3br1iX4WIiLyMBUMEZHnZMOGDUydOpXS0lImTJgA8NAegYyMDM6fP88vv/zC4sWL2bNnzxOv3%2BFw0K9fPzIyMmqd58HtrVy5kh9%2B%2BAGXy0VkZCRNmjRh27ZtuFwuvv32W959910yMzNxOBxs3ryZ5s2be/fMhIWFVVvn6dOnmT59Ol9//TWFhYX069ePkSNHVttbs3btWnbu3Mn58%2Bc5cuQIK1asqHGcJ0%2BeJC4u7qHp6enprFmzhry8PE6fPk1SUhJz5syhuLiYmJgYFi1aVOtzXb16NZ9//jnFxcU0a9aMhQsXArBt2zYOHTpEdnY2JSUlrFmzhkaNGnmXS0hI4MSJE7VmKiIij6aCISLynPTs2ZOhQ4cCeM%2BduJ/FYuGzzz6jXr16JCYm8tZbb7F69eqn2kZERATXr19/4vlnzpxJ69atsdls2Gw2hg0bRnR0NACvv/76YwvL/X788UdGjRpFnz59sNlsfPzxx5SWlnLw4EHvPO%2B//z6NGzcmJCSE4cOHc/z48RrXVVJSUuO5JDNnziQ6Oprg4GAGDRpEfHw8vXv3xmq1Mn78eI4dO%2Bad98G9SOPGjaNTp07YbDamTJni3bafnx8ul4u//voLj8dDfHw84eHh3uXsdjslJSVPlIGIiDxMBUNE5Dlp1qzZY%2BeJioryfh0dHc3ly5efahv5%2BfnVPn1/2jFt2bKF7t27ExoaSkhICL/%2B%2BitFRUVPtK7Lly97ywlUFaaoqCjy8/O90%2B4/5CkwMJAbN27UuK6QkBDKysoemn7/8gEBAQ99X9v6AJo0aVLjtgcMGEBycjJz5syhSZMmzJ07t9p6ysrKaNiwYa3rFRGRR1PBEBF5Tp7kBOlLly55v87NzSUiIuKJ1%2B9yufjtt9/o3bs3AA0aNODWrVvex69cufLIMd2%2BfZvx48ezYMECCgsLKS4uZsCAAd49AY8bf0REhPe8Bqjag5CXl1etND2pxMTEaudvPG/z5s3jjz/%2BIDMzk1OnTpGamup97PTp03To0KHOxiIi8qJRwRAR8RGPx8OiRYu4ffs2J0%2BeZPny5UycOPGxy925c4cjR44wevRonE4n06ZNA6Bjx47s3r2bvLw8SkpK%2BPLLLx%2B5nvLycioqKggLC8NisbBlyxZ27tzpfdzpdFJUVFTrXoIJEyawadMm9uzZw927d/nqq69wOBx07dr1KVKo0qNHDwoLC7l69epTL/u0Dh8%2BzOHDh3G73QQEBODv71/tZPjdu3czZMiQ5z4OEZEXlQqGiMgzepZLufbs2ZOYmBgGDx7MggUL6NOnT63zfvHFFwQHBxMWFsaMGTNISkpi79693vM7Bg8ezJtvvkn79u3p3r07o0aNeuQ4g4ODSU1NZfTo0YSGhrJ%2B/XpGjBjhfbxt27aMHTuWFi1a0KhRo4cOnWrTpg3Lly8nOTmZ8PBwduzYwaZNm7DZbE%2Bdi7%2B/P9OmTWPlypW1jvdx7p//UcuWlJQwa9YsQkJCiImJITIy0nvvjfz8fP7%2B%2B%2B9qOYiIyNPRjfZERHwgOzub1q1bP/P9MV4kV69epW/fvhw/fhw/Pz%2BfjCElJYV27doxe/Zsn2xfRORFoIIhIuID2dnZtGrVisrKSl8PRURExFA6REpExEfq6i7ZIiIidUl7MERERERExDDagyEiIiIiIoZRwRAREREREcOoYIiIiIiIiGFUMERERERExDAqGCIiIiIiYhgVDBERERERMYwKhoiIiIiIGEYFQ0REREREDKOCISIiIiIihlHBEBERERERw6hgiIiIiIiIYVQwRERERETEMCoYIiIiIiJiGBUMERERERExjAqGiIiIiIgYRgVDREREREQMo4IhIiIiIiKGUcEQERERERHDqGCIiIiIiIhhVDBERERERMQwKhgiIiIiImIYFQwRERERETGMCoaIiIiIiBhGBUNERERERAyjgiEiIiIiIob5P3bsHnA0qUCkAAAAAElFTkSuQmCC"/>

### Grouping by station name

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

### Wrapping Up

Hopefully, the above examples helped introduce some basic uses for the grouping process in pandas to help enhance your analysis and whet your appetite for more! What ideas do you have for further analysis on this dataset? Can you conquer the last idea of looking at the days of the week? Please, take a look at the resources linked below for further investigation!


### More Resources
* [Pandas Docs](http://pandas.pydata.org/pandas-docs/stable/groupby.html)
* [Hadley Wickam - The Split-Apply-Combine Strategy for Data Analysis](http://www.jstatsoft.org/v40/i01/paper)
* [Data Analysis for Python book by Wes McKinney](http://shop.oreilly.com/product/0636920023784.do?cmp=af-prog-books-videos-lp-na_afp_book_mckinney_cj_12307942_7040302)
* [Also excellent series from Greg Reda](http://www.gregreda.com/2013/10/26/working-with-pandas-dataframes/)
* [Excellent into to pandas series by Tom Augspurger](http://tomaugspurger.github.io/modern-1.html)
