#!/user/bin/env python
#encoding:utf-8
import os
import time
import requests
import datetime
from datetime import datetime as dt
from bson.objectid import ObjectId

import settings
from settings import REDIS, ENV, DB, SMSAPIKEY, AREA_CONNECTOR, SERVICE_COMPANY
from apps.base.sms import send_sms
from apps.base.push import push_message
from apps.base.logger import getlogger
from apps.base.utils import pf3


logger = getlogger(__name__)

if ENV <> 'PRO':
	def send_sms(to_mobile, msg):
		logger.info("send_sms:{}:{}".format(to_mobile, msg))

message1 = '【51快修】维修编号{},时间{}.{}餐厅 {}店(编号{}).设备 {},故障 {},状态 {}。'
message  = '【51快修】维修编号{},时间{}.{}餐厅 {}店(编号{}).设备 {},故障 {},状态 {}.已在{}通知 {},电话{},请尽快处理。'
message2 = '【51快修】维修编号{},时间{}.{}餐厅 {}店(编号{}).设备 {},故障 {},状态 {}。当前无人接单，请速处理。'
message3 = '【51快修】维修编号{},时间{}.{}餐厅 {}店(编号{}).设备 {},故障 {},状态 {}。当前无人接单，如需转单请回复:维修编号+ 转+维修商。'


def reset_push(mobile, code, status):
	maintenance  = DB.maintenance.find_one({'code':code, 'status':{'$in':[0, 1]}})
	if maintenance:
	    company = status.replace(u'转','')
	    users   = list(DB.user.find({'company':company,'city':maintenance['city']}))
	    if len(users) > 0:
	    	'''
	    	转单不需要更新报修编号
	        now = dt.now()
	        send_time = now.strftime('%H:%M')
	        send_day  = now.strftime('%Y%m%d')
	        start_send_day = dt.strptime('{} 00:00:01'.format(send_day), '%Y%m%d %H:%M:%S')
	        end_send_day   = dt.strptime('{} 23:59:59'.format(send_day), '%Y%m%d %H:%M:%S')

	        send_count     = DB.maintenance.find({'create_time':{'$lte':end_send_day,'$gte':start_send_day}}).count() + 1
	        if send_count < 10:
	            send_counts = "{}00{}".format(send_day, send_count)
	        elif send_count < 100:
	            send_counts = '{}0{}'.format(send_day, send_count)
	        else:
	            send_counts = '{}{}'.format(send_day, send_count)
	        '''
	        DB.maintenance.update({'_id':maintenance['_id']},{'$set':{'status':-1, 'message':u'转单'}})
	        
	        #DB.maintenance_users.update({'maintenance':maintenance['_id']},{'$set':{'status':-1}}, upsert=True, multi=True)
	        #maintenance_user = DB.maintenance_users.find_one({'maintenance':maintenance['_id']})

	        del maintenance['_id']
	        del maintenance['members']
	        maintenance['status'] = 0
	        #maintenance['code'] = send_counts
	        maintenance['company'] = company
	        maintenance['create_time'] = dt.now()
	        maintenance['update_time'] = dt.now()
	        maintenance['must_time'] = dt.now() + datetime.timedelta(hours=maintenance['must_range'])
	        maintenance['members'] = [str(i['_id']) for i in users if i.get('category') == '0']
	        maintenance['message'] = u'转单'
	        maintenance_id = DB.maintenance.save(maintenance)
	        
	        store = DB.store.find_one({'_id':ObjectId(maintenance['store'])})
	        device = DB.device.find_one({'_id':ObjectId(maintenance['device'])})
	        
	        push = DB.push.find_one({'city':maintenance['city'], 'company':maintenance['company'], 'head_type':maintenance['head_type']},{'provider':1, 'area_manager':1, 'manager':1, 'hq':1})
	        call_provider = DB.user.find_one({'_id':ObjectId(push['provider'])},{'username':1,'name':1})

	        if store and device and push and call_provider:
	            provider_manager, manager, hq = ["|".join(push.get(i,[])) for i in ['area_manager', 'manager', 'hq']]
	            REDIS.hset('call_pool', str(maintenance_id), "{}|{}|0|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(time.time(), u'非紧急' if maintenance['state']==2 else u'非紧急', maintenance['code'], send_time, SERVICE_COMPANY.get(maintenance['head_type']), maintenance['store'], store['no'], device['name'], maintenance['content'], send_time, call_provider['name'], call_provider['username'], provider_manager, manager, hq))
	        
	        sdata = {'type': 0, 'oid': str(maintenance_id)}
	        title = '{}:{}需要维修，赶快去接单吧！'.format(maintenance['store_name'], maintenance['product'])
	        for user in users:
	            push_message(user['_id'], title, sdata)
	            '''
	            if user.get('category') == '0':
	                if maintenance_user.get('_id'):del maintenance_user['_id']
	                maintenance_user['code'] = send_counts
	                maintenance_user['user'] = user['_id']
	                maintenance_user['create_time'] = dt.now()
	                maintenance_user['update_time'] = dt.now()
	                maintenance_user['status'] = 0
	                maintenance_user['must_time'] = dt.now() + datetime.timedelta(hours=maintenance['must_range'])
	                maintenance_user['maintenance'] = maintenance_id
	                DB.maintenance_users.save(maintenance_user)
	            '''
	    else:
	    	send_sms(mobile, u'不存在该服务商')
	else:
		send_sms(mobile, u'不存在该code')

def push1(oid, state, send_counts, send_time, company, store_name, store_no, name, error, to_mobile):
	msg = message1.format(send_counts, send_time, company, store_name, store_no, name, error, state)
	send_sms(to_mobile, msg)
			
def push2(oid, state, send_counts, send_time, company, store_name, store_no, name, error, recive_time, send_name, send_mobile, to_mobile, to_name):
	msg = message.format(send_counts, send_time, company, store_name, store_no, name, error, state, recive_time, send_name, send_mobile)
	send_sms(to_mobile, msg)
	DB.push_history.save({'to_name':to_name, 'to_mobile':to_mobile, 'maintenance':oid,'title':msg,'head_type':0,'category':2,'status':1,'active':0,'create_time':dt.now(),'update_time':dt.now()})
	
	mtce = DB.maintenance.find_one({'_id':ObjectId(oid)})
	if mtce:
		users = mtce.get('members')
		opt_users  = [m.get('opt_user') for m in DB.member.find({'user':{'$in':users}}) if m.get('opt_user')]
		push_users = [p.get('username') for p in DB.user.find({'_id':{'$in':opt_users}})]
		for p_mobile in push_users:
			msg2 = message2.format(send_counts, send_time, company, store_name, store_no, name, error, state)
			send_sms(p_mobile, msg2)
	
def push3(oid, state, send_counts, send_time, company, store_name, store_no, name, error, recive_time, send_name, send_mobile, to_mobile, to_name):
	msg = message.format(send_counts, send_time, company, store_name, store_no, name, error, state, recive_time, send_name, send_mobile)	
	send_sms(to_mobile, msg)
	DB.push_history.save({'to_name':to_name, 'to_mobile':to_mobile, 'maintenance':oid,'title':msg,'head_type':0,'category':3,'status':1,'active':0,'create_time':dt.now(),'update_time':dt.now()})

def push4(oid, state, send_counts, send_time, company, store_name, store_no, name, error, recive_time, send_name, send_mobile, to_mobile, to_name):
	msg = message.format(send_counts, send_time, company, store_name, store_no, name, error, state, recive_time, send_name, send_mobile)
	send_sms(to_mobile, msg)
	DB.push_history.save({'to_name':to_name, 'to_mobile':to_mobile, 'maintenance':oid,'title':msg,'head_type':0,'category':4,'status':1,'active':0,'create_time':dt.now(),'update_time':dt.now()})
	mtce = DB.maintenance.find_one({'_id':ObjectId(oid)})
	if mtce:
		push_message(mtce['user'], u'{}该叫修单无人接单,快去联系相关负责人员吧'.format(name), {'type':21, 'id':oid})

def push5(oid, state, send_counts, send_time, company, store_name, store_no, name, error, recive_time, send_name, send_mobile, to_mobile, to_name):
	msg = message3.format(send_counts, send_time, company, store_name, store_no, name, error, state)
	send_sms(to_mobile, msg)

while True:
	data = REDIS.hgetall('call_pool')
	curr_time = time.time()
	for oid, content in data.iteritems():
		ps = 0
		mtce = DB.maintenance.find_one({'_id':ObjectId(oid)})
		befor_time, states, head_type, send_counts, send_time, company, store_name, store_no, name, error, recive_time, provider, provider_mobile, provider_manager, provider_manager_mobile, manager, manager_mobile, hq, hq_mobile = content.split('|') 
		if head_type == '0':
			ps = 1
			push1(oid, states, send_counts, send_time, company, store_name, store_no, name, error, hq_mobile)
		elif head_type == '1' and curr_time - float(befor_time) > 600:
			ps = 1
			push2(oid, states, send_counts, send_time, company, store_name, store_no, name, error, recive_time, provider, provider_mobile, provider_manager_mobile, provider_manager)
		elif head_type == '2' and curr_time - float(befor_time) > 600:
			ps = 1 
			push3(oid, states, send_counts, send_time, company, store_name, store_no, name, error, recive_time, provider_manager, provider_manager_mobile, manager_mobile, manager)
		elif head_type == '3' and curr_time - float(befor_time) > 900 and mtce.get('head_type') <> 3:
			ps = 1
			push4(oid, states, send_counts, send_time, company, store_name, store_no, name, error, recive_time, manager, manager_mobile, hq_mobile, hq)
		elif (head_type == '4' and curr_time - float(befor_time) > 3600 and mtce.get('head_type') <> 3) or \
										(head_type=='3' and curr_time - float(befor_time) > 900 and mtce.get('head_type') == 3):
			push5(oid, states, send_counts, send_time, company, store_name, store_no, name, error, recive_time, manager, manager_mobile, hq_mobile, hq)
			REDIS.hdel('call_pool', oid)
		if ps:
			recive_time = dt.now().strftime('%H:%M')
			REDIS.hset('call_pool', oid, "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(curr_time, states, int(head_type)+1, send_counts, send_time, company, store_name, store_no, name, error, recive_time, provider, provider_mobile, provider_manager, provider_manager_mobile, manager, manager_mobile, hq, hq_mobile))


	try:
		if ENV <> 'PRO':
			body = {'msg':'ERROR', 'sms_reply':[{'mobile':'15017935316', 'text':u'20160503010 转高友2'}]}
		else:
			r = requests.post('http://yunpian.com/v1/sms/pull_reply.json',{'apikey':SMSAPIKEY})
			if r.status_code <> 200:raise
			body = r.json()
		if body.get('msg') == 'OK':
			content = body.get('sms_reply', [])
			for c in content:
				mobile, text = [c.get(i) for i in ['mobile', 'text']]
				if mobile and text:
					try:
						code, status = text.strip().split(' ')
						if status and status[0] == u'转':
							logger.info('reset_push')
							reset_push(mobile, code, status)			
						else:
							
							maintenance  = DB.maintenance.find_one({'code':code, 'status':{'$in':[1, 3]}})
							status = 0 if status.upper() == 'Y'  else -2
							if maintenance:
								query = {'stop':status}
								if status == 0: 
									query['status']  = 6
								DB.maintenance.update({'_id':maintenance['_id']},{'$set':query})
								send_sms(mobile, u'【51快修】编号:{},确认成功,谢谢'.format(code))
								
								users = []
								members = maintenance.get('members', [])
								for member in members:
									users.append(ObjectId(member))
									m = DB.member.find_one({'user':ObjectId(member)})
									if m: users.append(m['opt_user'])

								users.append(maintenance['user'])
								users.append(maintenance['grab_user'])

								if status == -2:
									title = u'{}:{}拒绝维修暂停!'.format(maintenance.get('store_name'), maintenance.get('product'))
								else:
									title = u'{}:{}维修暂停!'.format(maintenance.get('store_name'), maintenance.get('product'))
									REDIS.hset('stop_pool', str(maintenance['maintenance']), "{}|{}|{}|{}|{}|{}".format(time.mktime(maintenance['stop_day'].timetuple()), ','.join([str(user_id) for user_id in users]), maintenance['company'], maintenance['store_name'], maintenance['product'], maintenance['stop_day'].strftime('%H:%M')))
								for user in list(set(users)):
									push_message(user, title, {'type':12 if status==0 else 13, 'id':str(maintenance['maintenance']), 'product':maintenance.get('product')})

					except Exception as e:
						logger.info(str(e))
	except Exception as e:
		logger.info(str(e))

	#暂停即将结束推送提醒通知
	curr_time2 = time.time()
	data2 = REDIS.hgetall('stop_pool')

	for oid, content2 in data2.iteritems():
		befor_time2, user_ids, company_name, store_name, product, revice_time = content2.split('|') 
		if float(befor_time2) - float(curr_time2)  < 7200:
			for user_id in user_ids.split(','):
				push_message(ObjectId(user_id), u'暂停即将结束!', {'type':11,'id':oid ,'product':product, 'revice_time':revice_time})
			REDIS.hdel('stop_pool', oid)
	
	data3 = REDIS.hgetall('control_pool')

	#预计迟到提醒，到店扫码，离店填写工单
	curr_time3 = time.time()
	data3 = REDIS.hgetall('control_pool')
	for oid, content3 in data3.iteritems():
		logger.info(content3)
		befor_time3, code, grab_user_name, company_name, store_name, store_no, oid, opt_user_id, user_id, parent_user_id, come_time, come_time_status, work_time, work_time_status = content3.split('|')
		
		title = '{}{}({})'.format(company_name, store_name, store_no)

		if float(come_time) - curr_time3 < 1800 and come_time_status == '0':
			come_dt_time = pf3(dt.fromtimestamp(float(come_time)))
			try:
				push_message(ObjectId(user_id), u'{}{}({})正在等待你的维修，请在{}前到店。'.format(company_name, store_name, store_no, come_dt_time), {'type':18,'id':oid})
				push_message(ObjectId(parent_user_id), u'{}师傅未到达{}{}({}),请务必在{}前到店维修.'.format(grab_user_name, company_name, store_name, store_no, come_dt_time), {'type':24,'id':oid})
			except Exception as e:
				logger.info(str(e))
			come_time_status = 1
		
		
		if float(come_time) - curr_time3 < 100 and come_time_status == '1':
			try:
				for uid in [opt_user_id, user_id, parent_user_id]:
					push_message(ObjectId(uid), u'{}到店请扫描二维码签到!'.format(title), {'type':19,'id':oid})
			except Exception as e:
				logger.info(str(e))
			come_time_status = 2


		if float(work_time) - curr_time3 < 0 and work_time_status == '0':
			try:
				push_message(ObjectId(user_id), u'报修{}已过维修时效，请上传维修工单。'.format(title), {'type':20,'id':oid})
				push_message(ObjectId(parent_user_id), u'报修{}已过维修时效，{}师傅还未上传维修工单。'.format(title, grab_user_name), {'type':25,'id':oid})
			except Exception as e:
				logger.info(str(e))
			work_time_status = 1
			REDIS.hdel('control_pool', oid)

		if work_time_status <> 1:
			REDIS.hset('control_pool', oid, '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(curr_time3, code, grab_user_name, company_name, store_name, store_no, oid, opt_user_id, user_id, parent_user_id, come_time, come_time_status, work_time, work_time_status))

	#24小时自动确认修单
	curr_time4 = time.time()
	data4 = REDIS.hgetall('confirm_pool')
	for oid, content4 in data4.iteritems():
		befor_time4, user_id, status, title = content4.split('|')

		if curr_time4 - float(befor_time4)  > 3600*22 and status == '0':
			push_message(ObjectId(user_id), u'{}修单还没确认快去确认吧'.format(title), {'type':21, 'id':oid})
			REDIS.hset('confirm_pool', oid, '{}|{}|{}|{}'.format(befor_time4, user_id, 1, title))

		if curr_time4 - float(befor_time4)  > 3600*24 and status == '1':
			push_message(ObjectId(user_id), u'{}修单将会自动确认'.format(title), {'type':22, 'id':oid})
			REDIS.hdel('confirm_pool', oid)
			#确认维修单和报价单
			mtce = DB.maintenance.find_one({'_id':ObjectId(oid)})
			
			if mtce:
				mtce['status'] = 2 
				mtce['update_time'] = dt.now()
				mtce['message'] = '{} {}'.format(mtce.get('message',''), u'系统自动确认')
				DB.maintenance.save(mtce)
				bills = DB.bill.find({'maintenance':mtce['_id']})
				for bill in bills:
					if mtce.get('head_type') >1 :
						bill['status'] = 1 
						bill['message'] = '{} {}'.format(bill.get('message',''), u'系统自动确认')
	        			bill['confirm_time'] = dt.now()
        			DB.bill.save(bill)

	time.sleep(10) 




