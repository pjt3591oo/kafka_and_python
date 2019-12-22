from time import sleep
from json import dumps
from kafka import KafkaProducer
import random

def on_send_success(record_metadata):
    print(record_metadata.__dict__)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))


while True:
  producer.send('numtest1', value={'number' : random.randrange(0, 100)}).add_callback(on_send_success)
  sleep(1)
producer.flush()
producer = KafkaProducer(retries=5)
