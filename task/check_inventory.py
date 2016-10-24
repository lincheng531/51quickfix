#!/user/bin/env python
#encoding:utf-8
import os
import time
import requests
from datetime import datetime as dt
from bson.objectid import ObjectId

try:
	import settings
	from settings import REDIS, DB, SMSAPIKEY
	from apps.base.sms import send_sms
	from apps.base.logger import getlogger
	from apps.base.push import push_message
except Exception as e:
	import pymongo, redis
	DB = getattr(pymongo.MongoClient(host='localhost'),'51quickfix')
	REDIS = redis.Redis(host='localhost', port=6379, db=1)


logger = getlogger(__name__)


if __name__ == '__main__':
	data = REDIS.hgetall('inventory_pool')
	for oid, content in data.iteritems():
		send_time, uid, title, start_time, end_time, count = content.split('|')
		count = int(count)
		if (time.time() - float(send_time) > 86400 * 30 and count == 0) or (time.time() - float(send_time) > 86400 and count > 1):
			push_message(ObjectId(uid), title, {'type':10, 'start_time':start_time, 'end_time':end_time})
			REDIS.hset('inventory_pool', oid, "{}|{}|{}|{}|{}|{}".format(time.time(), uid, title, start_time, end_time, count+1))

