# Copyright 2019 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script accompanies this codelab:
# https://codelabs.developers.google.com/codelabs/pyspark-bigquery/

# This script outputs subreddits counts for a given set of years and month
# This data comes from BigQuery via the dataset "fh-bigquery.reddit_comments"

# These allow us to create a schema for our data
from pyspark.sql.types import StructField, StructType, StringType, LongType

# A Spark Session is how we interact with Spark SQL to create Dataframes
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


# This will help catch some PySpark errors
from py4j.protocol import Py4JJavaError

# Create a SparkSession under the name "reddit". Viewable via the Spark UI
spark = SparkSession.builder.appName("movie-project-submit-final").getOrCreate()

bucket = "bucket-deproject"
spark.conf.set('temporaryGcsBucket', bucket)
# Create a two column schema consisting of a string and a long integer
fields = [StructField("userId", StringType(), True),
          StructField("avg_rating", LongType(), True)]
schema = StructType(fields)

# Create an empty DataFrame. We will continuously union our output with this
subreddit_counts = spark.createDataFrame([], schema)


# gcloud dataproc jobs submit pyspark --cluster cluster-project  --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar --driver-log-levels root=FATAL getting_data_from_redshift.py

    # counts_by_subreddit.py

# df.groupBy("firstname").agg({"salary":"avg"}).show()

tables_read = []
table  = f"projectmovies-381510.dataset_movie.movies_data_par"


table_df = (spark.read.format('bigquery').option('table', table)
                        .load())

# subreddit_counts = (
#             table_df
#             .groupBy("userId")
#             .count()
#             .union(subreddit_counts)
#         )

avg_rating_df =  table_df.groupBy("userID").agg({"rating":"avg"})

# Keep track of all tables accessed via the job
# tables_read = []
# for year in years:
#     for month in months:

#         # In the form of <project-id>.<dataset>.<table>
#         table = f"fh-bigquery.reddit_posts.{year}_{month}"

#         # If the table doesn't exist we will simply continue and not
#         # log it into our "tables_read" list
#         try:
#             table_df = (spark.read.format('bigquery').option('table', table)
#                         .load())
#             tables_read.append(table)
#         except Py4JJavaError as e:
#             if f"Table {table} not found" in str(e):
#                 continue
#             else:
#                 raise

#         # We perform a group-by on subreddit, aggregating by the count and then
#         # unioning the output to our base dataframe
#         subreddit_counts = (
#             table_df
#             .groupBy("subreddit")
#             .count()
#             .union(subreddit_counts)
#         )

# print("The following list of tables will be accounted for in our analysis:")
# for table in tables_read:
#     print(table)

# From our base table, we perform a group-by, summing over the counts.
# We then rename the column and sort in descending order both for readability.
# show() will collect the table into memory output the table to std out.
# (
#     subreddit_counts
#     .groupBy("subreddit")
#     .sum("count")
#     .withColumnRenamed("sum(count)", "count")
#     .sort("count", ascending=False)
#     .show()
# )

print (avg_rating_df.show(3))
print ("***")
print (type(avg_rating_df))

avg_rating_df = avg_rating_df.withColumnRenamed("avg(rating)", "AverageRating")



## processing year and month wise data

from pyspark.sql.functions import month, year

# df = table_df
df = table_df.alias('df')


# Convert the "datetime_column" column to a PySpark date type
df = df.withColumn("date_column", df["datetime_column"].cast("date"))
# Extract the month and year from the "date_column" column
df = df.withColumn("month", month("date_column")).withColumn("year", year("date_column"))

# Group by year and month, and calculate the average rating
result = df.groupBy("year", "month").agg({"rating": "avg"}).orderBy("year", "month")

result = result.withColumnRenamed("avg(rating)", "averagerating")

print ("time based datframe is")
print (result.show(3))
print ("time base df is built")







avg_rating_df.write.format('bigquery').option('table', 'projectmovies-381510.dataset_movie.avg_rating').save()


result.write.format('bigquery').option('table', 'projectmovies-381510.dataset_movie.year_month_avg_rating').save()

# gcloud dataproc jobs submit pyspark --cluster ${CLUSTER_NAME} \
#     --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
#     --driver-log-levels root=FATAL \
#     counts_by_subreddit.py
