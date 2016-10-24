#!/user/bin/env python
#encoding:utf-8

from settings import REDIS


def call_poll(oid):
    REDIS.hset('call_poll', str(oid), "{}|1".format(time.time()))