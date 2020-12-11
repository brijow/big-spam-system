# BigSpamProject
Jack made this. Feel free to edit and make any necessary changes. Intended to use this just for myself and happy to merge it into a proper project later but I'll be commiting my things to a separate branch instead of master just in case. 

run 'cqlsh -f path/to/create_database.cql' to create the keyspace 'email_database' and create the table 'email'

to run the pyspark script with cassandra on local, use the below commands
spark-submit --packages datastax:spark-cassandra-connector:2.4.0-s_2.11,org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4 sparkETL.py input output
