# Grouping in Pandas

### Summary
Grouping can be a powerful tool for any data analyst to leverage while trying to get the most out of a dataset.

### Why would I want to group data?

Sometimes, you have a set of data that lends itself to being split into groups. For example, say we have a bunch of data about people.  We may want to group this data by age, gender, or maybe even profession! It provides us with another way to slice the data and gain more insight.


### Grouping in Pandas

Pandas offers the following functionality in their `groupby` functionality for dataframes.  From the docs:

> By “group by” we are referring to a process involving one or more of the following steps
>
> * Splitting the data into groups based on some criteria
> * Applying a function to each group independently
> * Combining the results into a data structure

Sounds like a handy tool. But how do I use it?

### Codes and Stuff

First, I’ll just state that I’m running pandas 0.18.1, just so we're on the same page.

```
>>> import pandas
>>> pandas.__version__
u’0.18.1'
```

I was looking around for some data to analyze, and came across [data](https://www.citibikenyc.com/system-data) from Citi Bike, the NYC bike share program.  It seemed like there was potential here for some interesting findings, and applications of data grouping. Let's take a look





### More Resources
* [Pandas Docs](http://pandas.pydata.org/pandas-docs/stable/groupby.html)
* [Excellent into to Pandas series by Tom Augspurger](http://tomaugspurger.github.io/modern-1.html)
* [Also excellent series from Greg Reda](http://www.gregreda.com/2013/10/26/working-with-pandas-dataframes/)
