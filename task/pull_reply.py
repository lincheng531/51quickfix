#!/user/bin/env python
#encoding:utf-8
import os
import time
import requests
from datetime import datetime as dt

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


def call_pool():
	results = {}
	data = REDIS.hgetall('call_pool')
	for oid, content in data.iteritems():
		befor_time, states, head_type, send_counts, send_time, company, store_name, store_no, name, error, recive_time, provider, provider_mobile, provider_manager, provider_manager_mobile, manager, manager_mobile, hq, hq_mobile = content.split('|') 
		if int(head_type) == 4:
			if results.get(hq_mobile):
				results[hq_mobile].append({send_counts:oid})
			else:
				results.update({hq_mobile:[{send_counts:oid}]})
	return results

def pull():
	'''
	msg 编号 名称 手机号码
	'''
    for i in range(3):
        try:
            r = requests.post('http://yunpian.com/v1/sms/pull_reply.json',{'apikey':SMSAPIKEY})
            if r.status_code <> 200:raise
            body = r.json()
           	if body.get('msg') == 'OK':
           		content = body.get('sms_reply', [])
           		for c in content:
           			mobile, text = [content.get(i) for i in ['mobile', 'text']]
           			descr = call_pool().get(mobile)
           			if descr:
           				try:
           					code, name, phone = [i.strip() for i in text.split(' ')]
           					dec = descr.get(no)
           					if dec:
           						user = DB.user.find_one({'username':phone})
           						if user:
           							mt = DB.maintenance.find_one({'code':code})
           							if mt:
           								mtu = DB.maintenance_users.find_one({'maintenance':mt['_id']})
           								if not mtu:
           									del mtu['_id']
           									mtu['create_time'] = dt.now()
           									mtu['update_time'] = dt.now()
           									mtu['user'] = user['_id']
           									DB.maintenance_users.save(mtu)
           									title = '{}:{}需要维修，赶快去接单吧！'.format(mtu.get('store_name'), mtu.get('product'))
            								sdata = {'type': 0, 'oid': str(mt['_id'])}
           									push_message(user['_id'], title, sdata)
           						else:
           							pass
           							'''
           							items = {
           								device_token 66255ab54f77384743a6a3fcf847f617efccfd7e
										tel [u'021-2395629']
										store_id 56382169c0828e69438a50f0
										electrician_no 36028119900318400000
										is_staff True
										platform android
										user_permissions []
										category 1
										city 上海市
										area 徐汇区
										refrigeration_no 有
										is_superuser 1
										last_login 2015-12-02 14:50:07.994000
										avatar_img /static/upload/2015/11/23/5652bbb98180cf61f9d00aec.jpg
										head_type 2
										store 日月光店
										username 11111111111
										update_time 2015-10-29 16:09:55.436000
										is_update True
										loc [31.220048, 121.426101]
										company_logo /static/img/store/2.png
										company 汉堡王
										is_active 1
										address 上海市徐汇区漕河泾新兴技术开发区虹梅路1523号
										password pbkdf2_sha256$12000$Gld2R6H1WLz1$ftuGiMCxggl5D7utqdzCn/KXPLsaFEm//Xdyw6DlHBE=
										source Bonny
										works [u'\u7535\u5de5\u8bc1', u'\u5236\u51b7\u6b63']
										name ni y yi w j l
										mobile 11111111111
										create_time 2015-10-29 16:09:55.436000
										_cls User.User
										_id 5631e640c0828e14832f1c11

           							}
           							'''
           				except Exception as e:
           					logger.info(str(e))
        except Exception as e:
            logger.info(str(e))
        else:
            loggger.info('send success')
            break


if __name__ == '__main__':
	while  True:
		pull()


