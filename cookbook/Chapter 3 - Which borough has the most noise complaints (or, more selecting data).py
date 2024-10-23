# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl


# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)

# This is necessary to show lots of columns in pandas 0.12.
# Not necessary in pandas 0.13.
pd.set_option("display.width", 5000)
pd.set_option("display.max_columns", 60)

# %%
# Let's continue with our NYC 311 service requests example.
# because of mixed types we specify dtype to prevent any errors
pl_complaints = pl.read_csv("../data/311-service-requests.csv", infer_schema_length=0)

# %%
# TODO: rewrite the above using the polars library (you might have to import it above) and call the data frame pl_complaints

# %%
# 3.1 Selecting only noise complaints
# I'd like to know which borough has the most noise complaints. First, we'll take a look at the data to see what it looks like:
pl_complaints.head(5)

# %%
# TODO: rewrite the above in polars

# %%
# To get the noise complaints, we need to find the rows where the "Complaint Type" column is "Noise - Street/Sidewalk".
pl_noise_complaints = pl_complaints.filter(pl_complaints["Complaint Type"] == "Noise - Street/Sidewalk")
pl_noise_complaints.head(3)

# %%
# TODO: rewrite the above in polars


# %%
# Combining more than one condition
is_noise = pl_complaints["Complaint Type"] == "Noise - Street/Sidewalk"
in_brooklyn = pl_complaints["Borough"] == "BROOKLYN"
pl_complaints.filter(is_noise & in_brooklyn).head(5)

# %%
# TODO: rewrite the above using the Polars library. In polars these conditions are called Expressions.
# Check out the Polars documentation for more info.


# %%
# If we just wanted a few columns:
pl_complaints.filter(is_noise & in_brooklyn).select(
    ["Complaint Type", "Borough", "Created Date", "Descriptor"]
).head(10)

# %%
# TODO: rewrite the above using the polars library


# %%
# 3.3 So, which borough has the most noise complaints?
is_noise = pl_complaints["Complaint Type"] == "Noise - Street/Sidewalk"
pl_noise_complaints = pl_complaints.filter(is_noise)
pl_noise_complaints.groupby("Borough").agg(pl.count()).sort("count", reverse=True)

# %%
# TODO: rewrite the above using the polars library


# %%
# What if we wanted to divide by the total number of complaints?
noise_complaint_counts = pl_noise_complaints.groupby("Borough").agg(pl.count().alias("noise_count"))
complaint_counts = pl_complaints.groupby("Borough").agg(pl.count().alias("total_count"))

normalized_complaints = noise_complaint_counts.join(complaint_counts, on="Borough")
normalized_complaints = (normalized_complaints.with_columns(
    (pl.col("noise_count") / pl.col("total_count")).alias("normalized_ratio")
))

normalized_complaints.select(["Borough", "normalized_ratio"])

# %%
# TODO: rewrite the above using the polars library


# %%
# Plot the results
normalized_complaints_pd = normalized_complaints.select(["Borough", "normalized_ratio"]).to_pandas()
normalized_complaints_pd.plot(kind="bar", x="Borough", y="normalized_ratio")
plt.title("Noise Complaints by Borough (Normalized)")
plt.xlabel("Borough")
plt.ylabel("Ratio of Noise Complaints to Total Complaints")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# TODO: rewrite the above using the polars library. NB: polars' plotting method is sometimes unstable. You might need to use seaborn or matplotlib for plotting.
