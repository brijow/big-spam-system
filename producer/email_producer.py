"""Produce emails by randomly sampling data set and sending to kafka topic."""
import os
import json
from time import sleep
from kafka import KafkaProducer
import utils

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
BATCH_SIZE = int(os.environ.get("BATCH_SIZE"))
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 10))
DATA_DIR_REGEX = os.environ.get("DATA_DIR_REGEX", "*")


def get_random_email_batch(n=BATCH_SIZE):
    # allow user to provide an environment var for this process
    # to control the emails we're sampling. If not provided, sample randomly.
    filenames = utils.get_n_random_email_file_names(n, DATA_DIR_REGEX)

    batch = []
    for filename in filenames:
        with open(filename, 'r', encoding='windows-1252', errors="ignore") as f:
            batch.append(f.read())
    return batch


def run():
    # Nit: move this line into a intialization script - it can crash easily...
    # This is idempotent but just smells a bt
    utils.download_and_extract_email_data()

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode('ascii'),
    )

    while True:
        email_batch = get_random_email_batch()
        producer.send(TOPIC_NAME, value=email_batch)
        sleep(SLEEP_TIME)


if __name__ == "__main__":
    run()
