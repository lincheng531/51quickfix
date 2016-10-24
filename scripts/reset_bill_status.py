#!/user/bin/env python
#encoding:utf-8

import time
from datetime import datetime as dt
from datetime import timedelta
try:
	from settings import REDIS, DB
	from apps.base.sms import send_sms
	from apps.base.logger import getlogger
	logger = getlogger(__name__)
except Exception as e:
	import pymongo, redis
	DB = getattr(pymongo.MongoClient(host='localhost'),'51quickfix')

while True:
	befor_time = dt.now() - timedelta(days=1)
	bills  = DB.bill.find({'state':1, 'create_time':{'$gte':befor_time}})
	for b in bills:
		DB.bill.update({'_id':b['_id']},{'$set':{'state':2}})
		DB.maintenance.update({'_id':b['maintenance']},{'$set':{'status':5})
		DB.maintenance_users.update({'maintenance':b['_id'], 'status':{'$in':[1, 2, 3, 4, 5]}},{'$set':{'status':5}})
	time.sleep(5)


