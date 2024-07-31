import redis

from config.config import RedisSetting


class RedisClient:
    def __init__(self):
        redis_obj = RedisSetting()
        self._client = redis.Redis(
            host=redis_obj.REDIS_HOST,
            port=redis_obj.REDIS_PORT,
            db=redis_obj.REDIS_DB,
            decode_responses=redis_obj.REDIS_DEPRECATED,
        )

    # @property
    # def _client(self):
    #     return self._client

    def set(self, key, value, duration):
        self._client.set(key, value, ex=duration)

    def get(self, query):
        return self._client.get(query)

    def delete(self, query):
        self._client.delete(query)
