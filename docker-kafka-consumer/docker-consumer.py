from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from kafka.admin import KafkaAdminClient, NewTopic

# KafkaAdminClient instance
admin_client = KafkaAdminClient(
    bootstrap_servers='kafka:9092', 
    client_id='CLIENT',
    api_version = (0, 10, 1)
)

# creating the kafka topic
def create_kafka_topic(topic_name):
    try:
        topic_list = []
        topic_list.append(NewTopic(name=topic_name, num_partitions=1, replication_factor=1))
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except:
        print('error in creating kafka topic')


# kafka consumer object
consumer = KafkaConsumer('pump1', bootstrap_servers = 'kafka:9092', value_deserializer=lambda m: json.loads(m.decode('ascii')))

client = InfluxDBClient(
    url = 'http://influxdb:8086',
    token = 'V7bAH-_Z_bcOTE_POvqJYZ3JBb9tRPdVVKd-mR_sODaV0nFxjWth5J62MkbRp4GOKztUDRnWmn3FI0MqYzD1PA==',
    org = 'my-org'
)

write_api = client.write_api(write_options=SYNCHRONOUS)

def kafka_python_consumer():
    for msg in consumer:
        
        # configuring the data-load to be written to influxdb
        load = {
            "measurement": "latest-pump",
            "tags": {"type": "water-pump"},
            "fields": {k: v for k, v in msg.value.items() if k != 'timestamp'},
            "time": msg.value['timestamp']
        }

        # writing to influx-db
        message = write_api.write(
            bucket = 'pump',
            org = 'my-org',
            record = load)

        print(message)

        write_api.flush()



if __name__ == '__main__':
    create_kafka_topic('pump1')
    kafka_python_consumer()
