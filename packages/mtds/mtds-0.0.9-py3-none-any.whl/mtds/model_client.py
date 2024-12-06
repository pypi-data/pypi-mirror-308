import os

from mtds.kafka_client import KafkaClient
from mtds.redis_client import RedisClient


class ModelClient:
    def __init__(self):
        self.kafka_client = KafkaClient.create_from_env()
        self.redis_client = RedisClient.create_from_env()

        self.push_topic = os.environ.get('push_topic')
        if not self.push_topic:
            raise Exception('Cannot read environment variable: "push_topic"')

    def refresh_progress(self, task_id, progress):
        self.redis_client.refresh_progress(task_id, progress)

    def get_progress(self, task_id):
        return self.redis_client.get_progress(task_id)

    def push_result(self, result):
        return self.kafka_client.produce(self.push_topic, result)
