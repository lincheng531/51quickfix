#!/user/bin/env python
#encoding:utf-8

from datetime import datetime as dt
from pymongo import Connection
from bson.objectid import ObjectId as _id

conn = Connection()
db   = conn['51quickfix']

for product in db.product.find():
	product['head_type'] = 2 
	db.product.save(product)

for spare in db.spare.find():
	spare['head_type'] = 2 
	db.spare.save(spare)

for store in db.store.find():
	if not store.get('head_type'):
		store['head_type'] = 2 
		db.store.save(store)

for user in db.user.find():
	if not user.get('city'):
		user['city'] = u'上海市'
	if not user.get('area'):
		user['area'] = u'华东区'
	db.user.save(user)

user = db.user.find_one({'username':'33333333333'})
if not user:
	user_id = db.user.save({u'tel': [], 
				u'is_staff': False, 
				u'user_permissions': [], 
				u'date_joined': dt.now(), 
				u'category': u'5', 
				u'loc': [], 
				u'is_superuser': 2, 
				u'source': u'达美乐', 
				u'last_login': dt.now(), 
				u'avatar_img': u'/static/img/store/3.png', 
				u'head_type': 3, 
				u'username': u'33333333333', 
				u'update_time': dt.now(), 
				u'is_update': False, 
				u'company_logo': u'/static/img/store/3.png', 
				u'company': u'达美乐', 
				u'is_active': 1, 
				u'train': [], 
				u'password': u'pbkdf2_sha256$12000$31TYMzGC6TZx$qb/riJIhDdKYqSCyFz424Ja7pb+qfvxuNmTXihzO1wU=', 
				u'name': u'\u6f58\u8fdc', 
				u'mobile': u'33333333333', 
				u'create_time': dt.now(), 
				u'_cls': u'User.User', 
				u'works': [], 
				u'train_desc': []
				})
else:
	user_id = user['_id']

for role in db.role.find():
	db.user_role.save({
						u'create_time': dt.now(), 
						u'update_time': dt.now(), 
						u'role': role['_id'], 
						u'user': user_id
					})

for m in db.maintenance.find():
	if not m.get('grab_user'):
		mu = db.maintenance_users.find_one({'maintenance':m['_id'], 'status':{'$in':[1, 2, 3, 4, 5, 6]}, 'opt_user':m['user']})
		if mu:
			m['grab_user'] = mu['user']
			db.maintenance.save(m)


for store in [
				[u'蓝村店', '049', 'LCD', u'苗威', '13651616773', u'2015/5/6', '58387712', u'浦东新区东方路1498号（近蓝村路)', 'lancun@dominos.com.cn', '575e4d960da60b069e5a33c6', '31.217124,121.533741'],
				[u'汇融店', '016', 'HRD', u'王关菲', '13661818760', u'2013/12/6', '52699209', u'普陀区白玉路38、40号（靠近曹杨路)', 'huirong@dominos.com.cn', '575e4d960da60b069e5a338d', '31.243156,121.425452']
			 ]:
	store_item = {
			'business_type': u'直营', 
			'city': u'上海市', 
			'business_hours': u'(9:00-23:00)', 
			'name': store[0], 
			'area': u'华东区', 
			'mobile': store[4], 
			'head_type': 3, 
			'initial': store[2], 
			'no': store[1],
			'store_manager': store[3], 
			'address': store[7], 
			'opening_time': dt.strptime(store[5], '%Y/%m/%d'), 
			'tel': store[6], 
			'operation_supervision': u'ted',
			'franchisee': u'上海达美乐比萨有限公司', 
			'email': store[8],
			'rid': store[9],
			'loc':[float(i) for i in store[10].split(',')]
			}
	if not db.store.find_one({'name':store[0], 'no':store[1]}):
		store_id = db.store.save(store_item)
	else:
		store_id = db.store.find_one({'name':store[0], 'no':store[1]})['_id']
	if not db.store.find_one({'username':store[4]}):

		user_item = db.user.save({
									'device_token': u'', 
									'store_id': str(store_id), 
									'is_staff': False, 
									'user_permissions': [], 
									'category': u'1', 
									'city': u'上海市', 
									'area': u'华东区', 
									'avatar_img': u'/static/img/store/3.png', 
									'head_type': 3, 
									'store': store[0], 
									'username': store[4], 
									'company_logo': u'/static/img/store/3.png', 
									'company': u'达美乐', 
									'is_active': 1, 
									'password': u'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs=', 
									'source': u'达美乐', 
									'name': store[3], 
									'mobile': store[4], 
									'create_time': dt.now(), 
									'_cls': u'User.User'
								})




