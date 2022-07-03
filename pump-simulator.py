import requests
import pandas as pd
from datetime import datetime
import time


BASE_URL = 'http://107.20.17.209:80/pump1'
data = pd.read_csv('data/sensor.csv')
data.drop('reading', axis=1, inplace=True)

for i in data.index:
    data.loc[i, 'timestamp'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    print(data.loc[i, 'timestamp'])
    measurement = data.loc[i].to_json()
    print(measurement)
    response = requests.post(BASE_URL, measurement)
    print(response)
    time.sleep(1)
