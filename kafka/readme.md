# Docker-based Kafka Cluster

## Install

This kafka cluster is fully containerised.

To run, you will need [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/) .

## Quickstart

You simply need to create a Docker network called `kafka-network` to enable communication between the Kafka cluster and producers / consumers applications (not yet implemented):

```bash
$ docker network create kafka-network
```

Then, spin up the local single-node Kafka cluster (will run in the background):

```bash
$ cd kafka-cluster
$ docker-compose -f docker-compose.yml up -d
```

## Teardown

To stop the docker-compose services and purge all topic contents:

```bash
$ docker-compose down
```

To remove the Docker network:

```bash
$ docker network rm kafka-network
```

## FAQs

How can I connect to the running container?

```bash
docker exec -it kafkadocker_kafka_1
```

How to use consumer from host machine to communicate with kafka in docker?

1. create kafka-network

2. create kafka cluster

3. optionally scale the number of brokers up

4. check what ports the brokers are connected to

5. start the producer to generate random input into "emails.topic" topic name

6. to use spark as the consumer, make sure you have spark installed, and then,


Here is basic workflow:


```bash
$ docker network create kafka-network
$ cd kafka-cluster
$ docker-compose up -d
$ docker-compose scale broker=3  # optional if you want more brokers
$ cd ../kafka-producer
$ docker-compose up -d
$ ./broker-list.sh  #  can run 'docker ps' for the same information
# note the ports, use these in consuer code
$ pyspark  --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4
```
```python
messages = spark.readStream.format('kafka').\
    option('kafka.bootstrap.servers', '172.17.0.1:32775').\
    option('subscribe', 'emails.topic').load()

values = messages.select(messages['value'].cast('string'))

query = values.writeStream.outputMode('update').format('console').start()
```
