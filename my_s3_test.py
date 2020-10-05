import datetime
import os

from flask import jsonify, Flask, request

from pprint import pprint
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col, date_format, format_number
from pyspark.sql.types import (
    BooleanType, DateType, IntegerType, NumericType, StringType,
    StructField, StructType
)
from time import time

# AWS Info
region = 'us-west-1'
bucket = 'gelt-folder'

# Header file for column headers
key = 'gdelt-data/CSV.header.dailyupdates.txt'

# Create SparkContext and set log level to ERROR only
sc = SparkContext()
sc.setLogLevel("ERROR")
sc._jsc.hadoopConfiguration().set(
    'fs.s3a.endpoint',
    f's3-{region}.amazonaws.com'
)
spark = SparkSession(sc)

# Read in the column header file
s3file = f's3a://{bucket}/{key}'
column_headers = spark.read.text(
    s3file, lineSep='\t'
)
column_headers = [row.value for row in column_headers.collect()]
column_headers[0] = 'GlobalEventID'
column_headers[1] = 'Day'
column_headers[-1] = 'SourceURL'
column_headers[-2] = 'DateAdded'

# for column in column_headers:
#     print(column)

# Set general schema type for columns
fields = [
    StructField(field_name, StringType(), nullable=True)
    for field_name in column_headers
]

print(f'Length of fields: {len(fields)}')

# for field in fields:
#     print(field)


def search_field(name):
    '''
    Searches for a field with given name.

    Parameters
    ----------
    name : str
        The name of the field to search for

    Returns
    -------
    str
        The field name
    '''
    for field in fields:
        if name == field.name:
            return field
        else:
            return "Oops! Field doesn't exist!"


# Set the schema based on the fields above
schema = StructType(fields)

DATES = []  # List to hold date ranges

## CHANGE OVERWRITE METHOD TO APPEND in Postgres settings below!
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2020, 9, 30)
delta = datetime.timedelta(days=1)

# Loop over and append to DATES
while start_date <= end_date:
    DATES.append(str(start_date).replace('-', ''))
    start_date += delta

key_list = []  # List to hold file key names
for day in DATES:
    key_list.append(f'gdelt-data/{day}.export.CSV')

s3_files = []  # List to hold the s3 filenames

for key in key_list:
    s3_files.append(
        f's3a://{bucket}/{key}'
    )

# Read in the list of files from s3
gdelt_log = spark.read.csv(
    s3_files, schema, sep='\t'
)

# SANITY check!
print("Schema before cleaning")
gdelt_log.printSchema()

# Change Date and DateAdded column format from string to date object
# also from 20200101 format to 2020-01-01
gdelt_log = gdelt_log.withColumn('Date', to_date(gdelt_log.Day, 'yyyyMMdd'))
gdelt_log = gdelt_log.withColumn('DateAdded',
                                 to_date(gdelt_log.DateAdded, 'yyyyMMdd'))

gdelt_log.createOrReplaceTempView('gdelt_log')  # Create a temp view to query

# SANITY check, DON'T RUN ON FULL DATASET!
# print("Num rows before cleaning")

# spark.sql("""
#    SELECT COUNT(*)
#    FROM gdelt_log
# """).show()

# Grab only necessary columns from full dataset, and cast specific types
test_query = spark.sql("""
    SELECT
        INT(GlobalEventID),
        Date, DAY(Date) AS Day, MONTH(Date) AS Month, YEAR(Date) AS Year,
        Actor1Code, Actor1Name, Actor2Code, Actor2Name,
        BOOLEAN(IsRootEvent), EventCode, EventBaseCode, EventRootCode,
        INT(QuadClass), FLOAT(GoldsteinScale), INT(NumMentions),
        INT(NumSources), INT(NumArticles), FLOAT(AvgTone),
        INT(Actor1Geo_Type), Actor1Geo_FullName, Actor1Geo_CountryCode,
        INT(Actor2Geo_Type), Actor2Geo_FullName, Actor2Geo_CountryCode,
        Actor1Geo_Lat, Actor1Geo_Long, Actor2Geo_Lat, Actor2Geo_Long,
        DateAdded, SourceURL
    FROM gdelt_log
    WHERE ActionGeo_CountryCode = 'US'
""")

# print("Schema after cleaning")
# test_query.printSchema()

# Postgresql info
user = os.environ['PG_USER']
password = os.environ['PG_PWD']
mode = "append"
url = "jdbc:postgresql://localhost:5432/gdelt_data"
properties = {"user": user, "password": password,
              "driver": "org.postgresql.Driver"}

# This writes to PostgreSQL
#
# print("Writing to PostgreSQL")

# start = time()
# test_query.write.jdbc(url=url, table='events',
#                       mode=mode, properties=properties)
# end = time()

# print("Write complete!")
# print(f"Total time: {end-start:0.2f} sec")

app = Flask(__name__)

print("Reading Postgres Table...")

# Read in entire dataset!
start = time()
test_df = spark.read.jdbc(url=url, table='events', properties=properties)
end = time()

print("Read complete!")
print(f"Total time: {end-start:0.2f} sec")

print("Final Schema")
test_df.printSchema()

# Create tempview to query dataset
test_df.createOrReplaceTempView('events')

# Query the dataset :)
test_query = spark.sql("""
    SELECT
        STRING(Date), Actor1Name, Actor2Name, EventRootCode, EventCode,
        QuadClass, GoldsteinScale, AvgTone, STRING(DateAdded), SourceURL
    FROM events
    WHERE
        Actor1Name = 'PRESIDENT' AND GoldsteinScale < 0 AND IsRootEvent
    LIMIT 10
""")

print("Running query...")
start = time()

data_list = [{
    'Date': row.Date,
    'Actor1 Name': row.Actor1Name,
    'Actor2 Name': row.Actor2Name,
    'Event Root Code': row.EventRootCode,
    'Event Code': row.EventCode,
    'Quad Class': row.QuadClass,
    'Goldstein Scale': row.GoldsteinScale,
    'Average Tone': row.AvgTone,
    'Date Added': row.DateAdded,
    'Source URL': row.SourceURL
} for row in test_query.collect()]
end = time()
print("Done!")
print(f"Total time: {end-start:0.2f} sec")

spark.stop()

# Create/Start Flask app here
# app = Flask(__name__)


@app.route('/events/president/<sentiment>/')
def run_test_query(sentiment):
    '''
    Displays just a test query.
    '''
    
    if sentiment == 'negative':
        return jsonify(Data=data_list)
    # for row in test_query.collect():
    #     print(row, '\n')
    # end = time()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

