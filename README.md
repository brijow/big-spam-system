Kafka front end is available on localhost:9000 when the broker is running.
# Scalable Real-time Streaming ETL for Spam Detection

## Dataset

Download from [Emails](https://spamassassin.apache.org/old/publiccorpus/) .

## Priject Summury

In this project we focus primarily on designing a scalable system to support near-online learning applications involving high-throughput, computationally expensive data stream processing in near real time.  Secondarily we focus on building a spam detector model that utilises this framework. We make use of state-of-the-art components from the Apache ecosystem to achieve highly scalable and fault tolerant data ingestion, streaming, feature engineering, storage, and model training. In addition to the end-to-end spam detection system, we also consider practical deployment and development strategies for building such cloud-destined, distributed applications.

## Contributor

- Shih-Chieh (Jack) Chen
- Jiuwei Wang
- Brian White

## Scope

This is final project of SFU CMPT 732 coursework 

* How to run instrucntion can be found inside `RUNNING.MD`
* More details of the project can be found at submitted report
* There is a video demo can be found at [YouTube](https://www.youtube.com/playlist?list=PLvlqrqDivHNKc27I12Z11kXzHvzewyrTu)

## Files Intruduction:

### RUNNING.txt

 - Instructions for proejct implementation.

### Kafka/

 - broker-list.sh
    - A fully containerised kafka cluster 
 - docker-compose.yml
    - To run, you will need [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/) .
 - readme.md 
    - Instructions for install the Kafka cluster.

### producer/

- email_producer.py
	- Produce emails by randomly sampling data set and sending to kafka topic.
	- Results of the clean json files.
- utils.py
	- Help functions for email_producer.
- requirements.txt
    - Installation requirements.
- docker-compose.yml
- Dockerfile

### consumer/

- sparkETL.py
	- Data transformation using spark. 
- clean_table_df.py
	- Clean the data rows in Cassandra table using spark dataframe based on input date('2020-12-11').

### dbutils/

- create_database.cql
	- Create keyspace: email_database
    - Create table: emails with columns (current_date, id, sender, receiver, receive_date, subject, word_tokens list, label)   
- clean_table.cql
	- Clean the data rows in Cassandra table using cqlsh based on input date('2020-12-11').

### ml/

- sparkML.py
    - Create a pyspark.ml pipeline for Classification.


