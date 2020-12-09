from pyspark import SparkConf, SparkContext
import re, sys
from pyspark.sql import SparkSession, functions, types
import datetime

cassandra_host = 'localhost'

# add more functions as necessary

def main(date_time_str):
    # main logic starts here
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    
    emails_df = spark.read.format("org.apache.spark.sql.cassandra").options(table="emails", keyspace="email_database").load()
    # clean up the records before the input date
    clean_df = emails_df.filter(emails_df['current_date'] > date_time_obj.date())
    clean_df.write.format("org.apache.spark.sql.cassandra").options(table="emails", keyspace="email_database").save()
    

if __name__ == '__main__':  
    #input like 2020-12-08
    date_time_str = sys.argv[1]
    spark = SparkSession.builder.appName('clean table df').config('spark.cassandra.connection.host', cassandra_host).getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main(date)