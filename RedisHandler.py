# encoding=utf-8
import json

import redis
import Constant
from logger import logger

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def get_all_from_z_set(key):
    logger.info(f"get_all_from_z_set key:{key}")
    return r.zrange(key, 0, -1)


def set_data_to_z_set(key, data, score):
    temp = json.dumps(data, default=lambda obj: obj.__dict__)
    logger.info(f"set_data_to_z_set key:{key},data:{temp},score:{score}")
    r.zadd(key, {temp: score})


def get_record_id():
    return r.incrby(Constant.record_id_key, 1)


def hset(key, field, value):
    temp = json.dumps(value, default=lambda obj: obj.__dict__)
    logger.info(f"hset key:{key},data:{field},score:{temp}")
    r.hset(key, field, temp)


def hget(key, field):
    field = str(field)
    logger.info(f"hget key:{key},data:{field}")
    return r.hget(key, field)
