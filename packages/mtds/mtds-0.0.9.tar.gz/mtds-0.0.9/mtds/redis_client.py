import json
import math
import os
from numbers import Number

import redis
from redis.exceptions import AuthenticationError
from redis.exceptions import ConnectionError

from mtds.common.errors import EnvironmentVariableNotFoundError
from mtds.common.errors import WrongProgressTypeError


class RedisClient:
    def __init__(self, redis_host=None, redis_port=None, redis_db=None, redis_password=None):
        self.validate_params(redis_host, redis_port, redis_db, redis_password)

        self.r = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            socket_connect_timeout=15,
        )

        try:
            self.r.ping()
        except AuthenticationError:
            raise Exception('Redis authentication failed')
        except ConnectionError as e:
            raise Exception(f'Redis connection failed, {e}')
        except Exception as e:
            raise Exception(f'Redis error {e}')

    @classmethod
    def create_from_env(cls):
        redis_host = os.environ.get('redis_host')
        redis_port = os.environ.get('redis_port')
        redis_db = os.environ.get('redis_db')
        redis_password = os.environ.get('redis_password')

        cls.validate_params(redis_host, redis_port, redis_db, redis_password)

        return cls(redis_host, int(redis_port), int(redis_db), redis_password)

    @staticmethod
    def validate_params(redis_host, redis_port, redis_db, redis_password):
        params = {
            'redis_host': redis_host,
            'redis_port': redis_port,
            'redis_db': redis_db,
            'redis_password': redis_password,
        }

        for param_name, param_value in params.items():
            if param_value is None:
                raise EnvironmentVariableNotFoundError(param_name)

    def refresh_progress(self, task_id, progress):
        if not isinstance(progress, int) or not (0 <= progress <= 100):
            raise WrongProgressTypeError()

        self.r.hset(f'model_status:{task_id}', 'progress', progress)

    def get_progress(self, task_id):
        progress = self.r.hget(f'model_status:{task_id}', 'progress')
        return int(progress) or -1
