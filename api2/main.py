from fastapi import FastAPI 
from pydantic import BaseModel
from typing import Union
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import json

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# from kafka.admin import KafkaAdminClient, NewTopic

# # KafkaAdmin Client instance
# admin_client = KafkaAdminClient(
#     bootstrap_servers='kafka:9092', 
#     client_id='CLIENT',
#     api_version = (0, 10, 1)
# )

# # creating the topic
# topic_list = []
# topic_list.append(NewTopic(name="testtt", num_partitions=1, replication_factor=1))
# admin_client.create_topics(new_topics=topic_list, validate_only=False)

# instantiating the producer

class Pump(BaseModel):
    timestamp: str
    sensor_00: Union[float, None]
    sensor_01: Union[float, None]
    sensor_02: Union[float, None]
    sensor_03: Union[float, None]
    sensor_04: Union[float, None]
    sensor_05: Union[float, None]
    sensor_06: Union[float, None]
    sensor_07: Union[float, None]
    sensor_08: Union[float, None]
    sensor_09: Union[float, None]
    sensor_10: Union[float, None]
    sensor_11: Union[float, None]
    sensor_12: Union[float, None]
    sensor_13: Union[float, None]
    sensor_14: Union[float, None]
    sensor_15: Union[float, None]
    sensor_16: Union[float, None]
    sensor_17: Union[float, None]
    sensor_18: Union[float, None]
    sensor_19: Union[float, None]
    sensor_20: Union[float, None]
    sensor_21: Union[float, None]
    sensor_22: Union[float, None]
    sensor_23: Union[float, None]
    sensor_24: Union[float, None]
    sensor_25: Union[float, None]
    sensor_26: Union[float, None]
    sensor_27: Union[float, None]
    sensor_28: Union[float, None]
    sensor_29: Union[float, None]
    sensor_30: Union[float, None]
    sensor_31: Union[float, None]
    sensor_32: Union[float, None]
    sensor_33: Union[float, None]
    sensor_34: Union[float, None]
    sensor_35: Union[float, None]
    sensor_36: Union[float, None]
    sensor_37: Union[float, None]
    sensor_38: Union[float, None]
    sensor_39: Union[float, None]
    sensor_40: Union[float, None]
    sensor_41: Union[float, None]
    sensor_42: Union[float, None]
    sensor_43: Union[float, None]
    sensor_44: Union[float, None]
    sensor_45: Union[float, None]
    sensor_46: Union[float, None]
    sensor_47: Union[float, None]
    sensor_48: Union[float, None]
    sensor_49: Union[float, None]
    sensor_50: Union[float, None]
    sensor_51: Union[float, None]
    machine_status: str

app = FastAPI()

client = InfluxDBClient(
    url = 'http://influxdb:8086',
    token = 'V7bAH-_Z_bcOTE_POvqJYZ3JBb9tRPdVVKd-mR_sODaV0nFxjWth5J62MkbRp4GOKztUDRnWmn3FI0MqYzD1PA==',
    org = 'my-org'
)

write_api = client.write_api(write_options=SYNCHRONOUS)

@app.get('/')
async def root():
    return {"message" : "Hello World!"}

@app.post('/pump1')
async def pump1(pump_data: Pump):
    json_fmt = jsonable_encoder(pump_data)
    load = {
        "measurement": "latest-pump2",
        "tags": {"type": "water-pump"},
        "fields": {k: v for k, v in json_fmt.items() if k != 'timestamp'},
        "time": json_fmt['timestamp']
    }
    print(load)

    # writing to influx-db
    message = write_api.write(
        bucket = 'pump',
        org = 'my-org',
        record = load)

    print(message)

    write_api.flush()
    return JSONResponse(json_fmt, status_code=201)