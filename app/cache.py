import redis
import json
import logging

logger = logging.getLogger(__name__)

redis_client = redis.Redis(host='localhost', 
                           port=6379, 
                           db=0, 
                           decode_responses=True)

def get_cache(key : str):
    try:
        value = redis_client.get(key)
        if value:
            logger.info(f"CACHE HIT: {key}")
            return json.loads(value)
        logger.info(f"CACHE MISS: {key}")
        return None
    except redis.exceptions.RedisError as e:
        logger.warning(f"CACHE ERROR (GET) {key}: {e}")
        return None
    
def set_cache(key : str, value, ttl: int = 60):
    try:
        redis_client.setex(key, ttl, json.dumps(value))
        logger.info(f"CACHE SET: {key} (TTL: {ttl}s)")
    except redis.exceptions.RedisError as e:
        logger.warning(f"CACHE ERROR (SET) {key}: {e}")

def delete_cache(key : str):
    try:
        redis_client.delete(key)
        logger.info(f"CACHE DELETE: {key}")
    except redis.exceptions.RedisError as e:
        logger.warning(f"CACHE ERROR (DELETE) {key}: {e}")