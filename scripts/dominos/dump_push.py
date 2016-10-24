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
				'head_type':3
			})
	acrea_manager = {u'华北区':[u'Ted','13564437395'],u'华东区':[u'Ted','13564437395'],u'华南区':[u'Ted','13564437395']}
	DB.push.save({
		    	'area':area, 
			    'city':city,  
			    'company':service_provider,
			    'head_type':3,          
			    'provider': str(opt_user),           
			    'service': str(user),   
			    'area_manager':[i.replace(u'）','') for i in area_manager.split(u'（')],  
			    'manager': acrea_manager.get(area),          
			    'hq':[u'michael', '13524192417']               
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
					'company_log':'/static/img/store/3.jpg',
					'avatar_img':'/static/img/store/3.jpg',
					'category':category,
					'electrician_no':electrician,
					'refrigeration_no':refrigeration,
					'is_active':1,
					'is_staff':False,
					'is_superuser':False,
					'is_update':False,
					'head_type':3,
					'create_time':dt.now(),
					'update_time':dt.now(),
					'password':u'pbkdf2_sha256$12000$Gld2R6H1WLz1$ftuGiMCxggl5D7utqdzCn/KXPLsaFEm//Xdyw6DlHBE='
				}
		uid = DB.user.save(item)
	else:
		uid = user['_id']

	return uid
	

if __name__ == '__main__':
	conn   = Connection()
	DB     = conn['51quickfix']
	data   = xlrd.open_workbook(u'doc/服务商推送通讯录.xlsx')

	keys = ['area','city','service_provider','service','provider_manager','electrician','refrigeration', 'area_manager']
	
	table  = data.sheets()[0]  
	nrows  = table.nrows
 	ncols  = table.ncols


 	for r in range(3, nrows):

 		items = {'create_time':dt.now(), 'update_time':dt.now()}
 		for c in range(ncols):
 			key, val = keys[c], table.cell(r, c).value
 			val = val.strip() if val else ''
 			items.update({key:val})
 		print items
 		if len(items) > 3:
 			#items['city'] = items['city'] if u'市' in items['city'] else "{}市".format(items['city'])
 			create_item(DB, items)







	 		