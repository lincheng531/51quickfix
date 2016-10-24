#!/user/bin/env python
# encoding:utf-8

import xlrd
import requests
from pymongo import Connection
from bson.objectid import ObjectId
from datetime import datetime as dt

def create_item(DB, items):
	area, city, service_provider, provider_manager, service, electrician, refrigeration, area_manager = [items.get(i) for i in ['area', 'city', 'service_provider', 'provider_manager', 'service', 'electrician', 'refrigeration', 'area_manager']]
	works = []
	if electrician:
		works.append(u'电工证')
	if refrigeration:
		works.append(u'制冷正')

	name, mobile = [i.replace(u'）','') for i in provider_manager.split(u'（')]
	opt_user = create_user(DB, name, mobile, '2', works, area, city, electrician, refrigeration, service_provider)
	name, mobile = [i.replace(u'）','') for i in service.split(u'（')]
	user = create_user(DB, name, mobile, '0', works, area, city, electrician, refrigeration, service_provider)

	if not DB.member.find_one({'opt_user':opt_user, 'user':user}):
		DB.member.save({
				'category':2,
				'update_time':dt.now(),
				'area':area,
				'city':city,
				'company':service_provider,
				'opt_user':opt_user,
				'create_time':dt.now(),
				'user':user,
				'active':1,
				'head_type':2,
				'store':u'汉堡王'
			})
	acrea_manager = {u'华北区':[u'周文辉','13585753381'],u'华东区':[u'邱渊','18221168715'],u'华南区':[u'周文辉','13585753381'],u'加盟区':[u'周文辉','13585753381']}
	DB.push.save({
		    	'area':area,
			    'city':city,  
			    'company':service_provider,
			    'head_type':2,          
			    'provider': str(opt_user),           
			    'service': str(user),   
			    'area_manager':[i.replace(u'）','') for i in area_manager.split(u'（')],  
			    'manager': acrea_manager.get(area),          
			    'hq':[u'周文辉', '13585753381']               
		})


def create_user(DB, name, mobile, category, works, area, city, electrician, refrigeration, service_provider):

	user   = DB.user.find_one({'username':mobile})
	if not user:
		item   = {
					'_cls':'User.User',
					'user_permissions':[],
					'username':mobile,
					'name':name,
					'works':works,
					'source':service_provider,
					'area':area,
					'city':city,
					'mobile':mobile,
					'company':service_provider,
					'company_log':'/static/img/store/2.png',
					'avatar_img':'/static/img/store/2.png',
					'category':category,
					'electrician_no':electrician,
					'refrigeration_no':refrigeration,
					'is_active':1,
					'is_staff':False,
					'is_superuser':False,
					'is_update':False,
					'head_type':2,
					'create_time':dt.now(),
					'update_time':dt.now(),
					'password':u'pbkdf2_sha256$12000$Gld2R6H1WLz1$ftuGiMCxggl5D7utqdzCn/KXPLsaFEm//Xdyw6DlHBE='
				}
		uid = DB.user.save(item)
	else:
		uid = user['_id']
	'''
	text = '【51快修】您当前的登陆账号是您的手机号码，密.码:000000，您当前的职位是{}。'
	if category == '0':
		text = text.format(u'维修员')
	if category == '2':
		text = text.format(u'区域维修主管')
	if category == '1：
		text = text.format(u'餐厅负责人')
	print text
	r = requests.post('http://yunpian.com/v1/sms/send.json',{'apikey':'26235daf2cdee5c1e931205e0a939767','mobile':mobile, 'text':text})
	if r.status_code <> 200:
		print 'mobile:{}:{}'.format(mobile, text)
	'''
	return uid
	

if __name__ == '__main__':
	conn   = Connection()
	DB     = conn['51quickfix']
	data   = xlrd.open_workbook(u'doc/push/服务商人员架构.xls')

	keys = ['area','city','service_provider','service','provider_manager','electrician','refrigeration', 'area_manager']
	
	table  = data.sheets()[0]  
	nrows  = table.nrows
 	ncols  = table.ncols


 	for r in range(nrows):
 		if r >2:
	 		items = {'create_time':dt.now(), 'update_time':dt.now()}
	 		for c in range(ncols):
	 			key, val = keys[c], table.cell(r, c).value
	 			val = val.strip() if val else ''
	 			items.update({key:val})
	 		if len(items) > 3:
	 			#items['city'] = items['city'] if u'市' in items['city'] else "{}市".format(items['city'])
	 			create_item(DB, items)







	 		