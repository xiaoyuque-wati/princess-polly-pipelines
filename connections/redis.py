import redis
import os
from common.config import REDIS_URL

def get_redis_client():
    return redis.Redis.from_url(REDIS_URL)
