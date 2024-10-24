# %%
import polars as pl
import matplotlib.pyplot as plt


# %%
# Reading data from a csv file
# You can read data from a CSV file using the `read_csv` function. By default, it assumes that the fields are comma-separated.

# We're going to be looking at some cyclist data from Montréal. Here's the [original page](http://donnees.ville.montreal.qc.ca/dataset/velos-comptage) (in French), but it's already included in this repository. We're using the data from 2012.

# This dataset is a list of how many people were on 7 different bike paths in Montreal, each day.

pl_broken_df = pl.read_csv("../data/bikes.csv", encoding="ISO-8859-1")

# TODO: please load the data with the Polars library (do not forget to import Polars at the top of the script) and call it pl_broken_df

# %%
# Look at the first 3 rows
pl_broken_df[:3]

# TODO: do the same with your polars data frame, pl_broken_df

# %%
# You'll notice that this is totally broken! `read_csv` has a bunch of options that will let us fix that, though. Here we'll

# * change the column separator to a `;`
# * Set the encoding to `'latin1'` (the default is `'utf8'`)


pl_fixed_df = pl.read_csv(
    "../data/bikes.csv", 
    separator=";",
    encoding="latin1"
)


# * Convert the 'Date' column from string to date format
# * Ensure the date is parsed with day first (day/month/year)

pl_fixed_df = pl_fixed_df.with_columns(
    pl.col("Date").str.strptime(pl.Date, "%d/%m/%Y")
)

pl_fixed_df[:3]

# TODO: do the same (or similar) with polars


# %%
# Selecting a column
# When you read a CSV, you get a kind of object called a `DataFrame`, which is made up of rows and columns. You get columns out of a DataFrame the same way you get elements out of a dictionary.

# Here's an example:
pl_fixed_df["Berri 1"]

# TODO: how would you do this with a Polars data frame?


# %%
# Plotting is quite easy in Pandas
pl_fixed_df.plot.line(x="Date", y="Berri 1")  
# TODO: how would you do this with a Polars data frame?


# %%
# We can also plot all the columns just as easily. We'll make it a little bigger, too.
# You can see that it's more squished together, but all the bike paths behave basically the same -- if it's a bad day for cyclists, it's a bad day everywhere.

pl_fixed_df.plot.line(x="Date", y="Berri 1") .properties(
    width=800,  # Equivalent to figsize=(15, 10) in width and height
    height=600
)

# TODO: how would you do this with a Polars data frame? With Polars data frames you might have to use the Seaborn library and it mmight not work out of the box as with pandas.

# %%
