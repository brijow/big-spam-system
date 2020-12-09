from pyspark import SparkConf, SparkContext
import re, sys
from pyspark.sql import SparkSession, functions, types

cassandra_host = 'localhost'

# add more functions as necessary
def output_line(rdd):
    orderkey, price, names = rdd
    namestr = ', '.join(sorted(list(names)))
    return 'Order #%d $%.2f: %s' % (orderkey, price, namestr)

def main(date):
    # main logic starts here
    emails_df = spark.read.format("org.apache.spark.sql.cassandra").options(table="emails", keyspace="email_database").load()
   
    clean_df = emails_df.filter(emails_df['current_date'] > date)
    clean_df.write.format("org.apache.spark.sql.cassandra").options(table="emails", keyspace="email_database").save()
    

if __name__ == '__main__':  
    #input like 2020-12-08
    date = sys.argv[1]
    spark = SparkSession.builder.appName('clean table df').config('spark.cassandra.connection.host', cassandra_host).getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main(date)