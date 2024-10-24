# %%
import pandas as pd

# %%
# Parsing Unix timestamps
# It's not obvious how to deal with Unix timestamps in pandas -- it took me quite a while to figure this out. The file we're using here is a popularity-contest file of packages.

# Read it, and remove the last row
popcon = pd.read_csv(
    "/Users/hanxishi/Desktop/pandas_to_polars_cookbook/data/popularity-contest",
    sep=" ",)[:-1]
popcon.columns = ["atime", "ctime", "package-name", "mru-program", "tag"]

# TODO: please reimplement this using Polars
import polars as pl
popcon_pl = pl.read_csv("/Users/hanxishi/Desktop/pandas_to_polars_cookbook/data/popularity-contest",has_header=False,separator=' ' )
popcon_pl = popcon_pl[:-1]
popcon_pl.columns = ["atime", "ctime", "package-name", "mru-program", "tag"]
print(popcon_pl)


# %%
# The magical part about parsing timestamps in pandas is that numpy datetimes are already stored as Unix timestamps. So all we need to do is tell pandas that these integers are actually datetimes -- it doesn't need to do any conversion at all.
# We need to convert these to ints to start:
popcon["atime"] = popcon["atime"].astype(int)
popcon["ctime"] = popcon["ctime"].astype(int)

# TODO: please reimplement this using Polars
popcon_pl = popcon_pl.filter(
    pl.col("atime").str.contains(r"^\d+$") & pl.col("ctime").str.contains(r"^\d+$")
)

# Cast 'atime' and 'ctime' to integer (Unix timestamps)
popcon_pl = popcon_pl.with_columns([
    pl.col("atime").cast(pl.Int64),
    pl.col("ctime").cast(pl.Int64)
])

# Show the resulting DataFrame
print(popcon_pl.head())

# %%
# Every numpy array and pandas series has a dtype -- this is usually `int64`, `float64`, or `object`. Some of the time types available are `datetime64[s]`, `datetime64[ms]`, and `datetime64[us]`. There are also `timedelta` types, similarly.
# We can use the `pd.to_datetime` function to convert our integer timestamps into datetimes. This is a constant-time operation -- we're not actually changing any of the data, just how pandas thinks about it.

popcon["atime"] = pd.to_datetime(popcon["atime"], unit="s")
popcon["ctime"] = pd.to_datetime(popcon["ctime"], unit="s")
popcon.head()

# TODO: please reimplement this using Polars
popcon_pl = popcon_pl.with_columns([
    (pl.col("atime").cast(pl.Int64) * 1000).alias("atime_ms"),
    (pl.col("ctime").cast(pl.Int64) * 1000).alias("ctime_ms")])
popcon_pl = popcon_pl.with_columns([
    pl.col("atime_ms").cast(pl.Datetime("ms")).alias("atime"),
    pl.col("ctime_ms").cast(pl.Datetime("ms")).alias("ctime")])

# %%
# Now suppose we want to look at all packages that aren't libraries.

# First, I want to get rid of everything with timestamp 0. Notice how we can just use a string in this comparison, even though it's actually a timestamp on the inside? That is because pandas is amazing.
popcon = popcon[popcon["atime"] > "1970-01-01"]

# Now we can use pandas' magical string abilities to just look at rows where the package name doesn't contain 'lib'.
nonlibraries = popcon[~popcon["package-name"].str.contains("lib")]
nonlibraries.sort_values("ctime", ascending=False)[:10]

# TODO: please reimplement this using Polars
filtered_popcon = popcon_pl.filter(pl.col("atime") > pl.datetime(1970, 1, 1))
nonlibraries = filtered_popcon.filter(~pl.col("package-name").str.contains("lib"))
nonlibraries_sorted = nonlibraries.sort("ctime", descending=True).head(10)
print(nonlibraries_sorted.select(["atime", "ctime", "package-name", "mru-program", "tag"]))

# The whole message here is that if you have a timestamp in seconds or milliseconds 