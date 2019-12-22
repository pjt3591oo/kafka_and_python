import threading, logging, time
import multiprocessing
from json import loads
from kafka import KafkaConsumer, KafkaProducer

class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        
    def stop(self):
        self.stop_event.set()
        
    def run(self):
        consumer = KafkaConsumer(
          bootstrap_servers='localhost:9092',
          auto_offset_reset='earliest',
          group_id='my-group1',
          enable_auto_commit=False,
          value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        consumer.subscribe(['numtest2', 'numtest1' ])

        while not self.stop_event.is_set():
            for message in consumer:
                print(message.topic, message.value)
                consumer.commit()
                if self.stop_event.is_set():
                    break
        
        consumer.close()
        
        
def main():
    tasks = [
        # Producer(),
        Consumer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)
    
    # for task in tasks:
    #     task.stop()

    for task in tasks:
        task.join()
        
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()