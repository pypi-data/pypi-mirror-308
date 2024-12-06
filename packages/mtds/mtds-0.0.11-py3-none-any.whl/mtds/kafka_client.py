import json
import logging
import os

from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import Producer

from mtds.common.errors import EnvironmentVariableNotFoundError


class KafkaClient:
    def __init__(self, bootstrap_servers, group_id=None):
        if not (bootstrap_servers or group_id):
            raise ValueError('Either bootstrap_servers or group_id must be provided')

        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.producer_config = {'bootstrap.servers': self.bootstrap_servers}
        self.producer = Producer(self.producer_config)

        if self.group_id:
            self.consumer_config = {
                'bootstrap.servers': self.bootstrap_servers,
                'group.id': self.group_id,
                'auto.offset.reset': 'earliest',
            }
            self.consumer = Consumer(self.consumer_config)
        else:
            self.consumer = None

    @classmethod
    def create_from_env(cls):
        bootstrap_servers = os.environ.get('bootstrap_servers')
        group_id = os.environ.get('group_id')

        params = {
            'bootstrap_servers': bootstrap_servers,
            'group_id': group_id,
        }

        for param_name, param_value in params.items():
            if param_value is None:
                raise EnvironmentVariableNotFoundError(param_name)

        return cls(bootstrap_servers, group_id)

    def produce(self, topic, message):
        try:
            msg = json.dumps(message, default=str, ensure_ascii=False).encode('utf-8')
            self.producer.produce(topic, msg, callback=self.delivery_report)
            self.producer.flush()
            return True
        except Exception as e:
            self.logger.error(f'Failed to produce message to {topic}: {e}')
            return False

    def delivery_report(self, err, msg):
        if err is not None:
            self.logger.error(f'Message delivery failed: {err=}, {msg=}')
        else:
            self.logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

    def subscribe(self, topics):
        if self.consumer:
            self.consumer.subscribe(topics)
            self.logger.info(f'Subscribed to topics: {topics}')
        else:
            self.logger.warning('Consumer is not configured. Please provide a group_id.')

    def consume(self, timeout=-1):
        if not self.consumer:
            self.logger.error('Consumer is not configured.')
            return None

        try:
            msg = self.consumer.poll(timeout)
            if msg is None:
                return None
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    self.logger.info(f'Reached end of partition for {msg.topic()}')
                else:
                    self.logger.error(f'Consumer error: {msg.error()}')
                return None
            return msg.value().decode('utf-8')
        except Exception as e:
            self.logger.error(f'Failed to consume message: {e}')
            return None

    def close(self):
        if self.consumer:
            self.consumer.close()
            self.logger.info('Consumer closed.')
        self.producer.flush()
        self.logger.info('Producer closed.')
