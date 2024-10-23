# %%
import polars as pl

# %%
# We saw earlier that pandas is really good at dealing with dates. It is also amazing with strings! We're going to go back to our weather data from Chapter 5, here.
pl_weather_2012 = pl.read_csv("../data/weather_2012.csv")
pl_weather_2012 = pl_weather_2012.with_columns(
    pl.col("date_time").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S").alias("date_time")
).set_sorted("date_time")
pl_weather_2012 = pl_weather_2012.with_columns([
    pl.col("date_time").dt.month().alias("month")
])
pl_weather_2012.head(5)

# TODO: load the data using polars and call the data frame pl_wather_2012


# %%
# You'll see that the 'Weather' column has a text description of the weather that was going on each hour. We'll assume it's snowing if the text description contains "Snow".
# Pandas provides vectorized string functions, to make it easy to operate on columns containing text. There are some great examples: "http://pandas.pydata.org/pandas-docs/stable/basics.html#vectorized-string-methods" in the documentation.

weather_description = pl_weather_2012["month", "weather"]

is_snowing = weather_description["weather"].str.contains("Snow").cast(pl.Float64).alias("is_snowing")

# Let's plot when it snowed and when it did not:

weather_with_snow = weather_description.with_columns(is_snowing)

# TODO: do the same with polars


    # %%
# If we wanted the median temperature each month, we could use the `resample()` method like this:

# Group by month and calculate the median temperature for each month
monthly_median_temp = pl_weather_2012.group_by("month").agg(
   [pl.median("temperature_c").alias("median_temperature")])
monthly_median_temp.plot.bar(x="month",y="median_temperature")
# Unsurprisingly, July and August are the warmest.

# TODO: and now in Polars

# %%

monthly_snow_percentage = weather_with_snow.group_by("month").agg(
   [pl.mean("is_snowing").alias("snow_percentage")])
monthly_snow_percentage.plot.bar(x="month",y="snow_percentage")



# So now we know! In 2012, December was the snowiest month. Also, this graph suggests something that I feel -- it starts snowing pretty abruptly in November, and then tapers off slowly and takes a long time to stop, with the last snow usually being in April or May.

# TODO: please do the same in Polars

# %%
