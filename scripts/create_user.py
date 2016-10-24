#!/user/bin/env python
#encoding:utf-8
import os
import time
import requests
from bson.objectid import ObjectId
import datetime

try:
	import settings
	from settings import REDIS, DB
	from apps.base.sms import send_sms
	from apps.base.logger import getlogger
except Exception as e:
	import pymongo, redis
	DB = getattr(pymongo.MongoClient(host='localhost'),'51quickfix')
	REDIS = redis.Redis(host='localhost', port=6379, db=1)
	



def send_sms(mobile, text):
    for i in range(3):
        try:
            r = requests.post('http://yunpian.com/v1/sms/send.json',{'apikey':'26235daf2cdee5c1e931205e0a939767','mobile':mobile, 'text':text})
            if r.status_code <> 200:
                raise
        except Exception as e:
            print e
        else:
            print 'send success'
            break


if __name__ == '__main__':
	for user in DB.user.find():
		mobile, category, name, company = [user.get(i) for i in ['username', 'category', 'name', 'company']]
		if company not in [u'高友1', u'高友2', 'Bonny']:
			if category == '1':
				manager = u'餐厅版'
			else:
				manager = u'服务商版'

			message = u'【51快修】您当前的账号:{},密.码:000000(可在个人资料修改),请卸载老版本重新下载[{}],祝工作顺利！'.format(mobile, manager)
			print mobile, category, name, company, message
			send_sms(mobile, message)




