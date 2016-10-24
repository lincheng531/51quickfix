#!/user/bin/env python
#encoding:utf-8
import xlrd
from datetime import datetime as dt
from pymongo import Connection
from bson.objectid import ObjectId as _id

if __name__ == '__main__':
	conn = Connection()
	db   = conn['51quickfix']
	data   = xlrd.open_workbook(u'push/dump_oc_20160219.xlsx')

	data1, data2 = {}, {}
	for tab_index in range(9):

		table  = data.sheets()[tab_index] 
		nrows  = table.nrows
 		ncols  = table.ncols
 		for index in range(nrows):
 			items = []
 			for index2 in range(ncols):
 				items.append(table.cell(index,index2).value)
 			
 			if tab_index in [2, 3, 4] and len(items) > 5 and items[0] and items[0].strip() == 'Operation':
 				name, mobile = items[2].split(u'（')[0].strip(), str(items[4]).replace(' ','').replace('.0', '').strip()
 				data1.update({name:mobile})
 				
 	 		
 			if tab_index in [5, 6, 7, 8] and  len(items) > 7 and  items[7] and items[7].strip().startswith('bk'):
 				items[1] = items[1].strip()[:5]
 				no, name = items[1], items[8].split(' ')[0].split(u'（')[0].strip()
 				if data2.get(name):
 					data2[name].append(no)
 				else:
 					data2.update({name:[no]})

 	print len(data1), len(data2)
	for name, no in data2.iteritems():
		if data1.get(name):
			mobile = data1.get(name)
			stores = []
			for n in no:
				store =  db.store.find_one({'no':n})
				if store:
					stores.append(store)
			items = {
						'_cls': u'User.User',
			            'is_staff': False, 
			            'user_permissions': [], 
			            'category': '4', 
			            'avatar_img': '/static/img/store/2.png', 
			            'head_type': 2, 
			            'username': mobile, 
			            'company_logo': '/static/img/store/2.png', 
			            'company':u'汉堡王', 
			            'is_active': 1,
			            'source': u'汉堡王',
			            'name': name, 
			            'mobile': mobile,
			            'is_superuser':2,
			            'store_id':','.join([str(i['_id']) for i in stores]),
			            'store':','.join([i.get('name') for i in stores]),
			            'create_time':dt.now(),
			            'update_time':dt.now(),
			            'password':'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs='
			            }
			if not db.user.find_one({'username':items['username']}):
				print '>'*10
				db.user.save(items)




		else:
			print "debug2:", name, no
	


 
 	


