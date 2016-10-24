#!/user/bin/env python
# encoding:utf-8

import xlrd
from pymongo import Connection
from bson.objectid import ObjectId
import time
from datetime import datetime as dt

from pypinyin import pinyin, lazy_pinyin
import pypinyin

def format_status(status, val):
	status_type, status_time1, status_time2 = 0, 0, 0
	if status.find(u'修复') > -1:
		status_time2 = val
	else:
		status_time1 = val
	if status.find(u'紧急') > -1:
		status_type = 1
	else:
		status_type = 2

if __name__ == '__main__':
	conn   = Connection()
	DB     = conn['51quickfix']

	data   = xlrd.open_workbook(u'doc/call.xls')
	areas  = [u'华东区', u'华南区', u'华北区', u'加盟区']
	for tab in range(1):
		table  = data.sheets()[tab] 
		nrows  = table.nrows
 		ncols  = table.ncols
 		
 		
 		provices, citys, store_counts, person_counts = [], [], [], []
 		ccity  = None
 		for i in range(nrows):
 			provice = table.cell(i,0).value.strip()
 			city  = table.cell(i, 1).value.strip()
 			store_count = table.cell(i, 2).value
 			if isinstance(store_count, float):store_count = int(store_count)
 			person_count = table.cell(i, 3).value
 			if isinstance(person_count, float):person_count = int(person_count)
 			provices.append(provice)
 			if city in areas:
 				ccity = city

 			citys.append(u"{} {}".format(ccity, city))
 			store_counts.append(store_count)
 			person_counts.append(person_count)

		for i3 in range(2, nrows):
			provider, city, store_count, person_count  =  provices[i3], citys[i3], store_counts[i3], person_counts[i3]
	
			area, city =  city.split(' ')
			franchisee = None
			if city.find(u'（') > -1:
				city, franchisee = city.split(u'（')
				franchisee = franchisee.replace(u'）','')[0]
			city = city if u'市' in city  else u"{}市".format(city)
			providers = provider.split(' ')
			#print provice, providers, len(providers)
			if len(providers) == 3:
				providerc, sub_provider = providers[0], providers[-1] 
			else:
				providerc, sub_provider = providers[0], None  		
 		
			for i2 in range(4, ncols):
				name   = table.cell(0, i2).value.strip().split('|')
				parent_name = None
				if len(name) == 2:
					name, parent_name = name 
				else:
					name = name[0]
			
				status = table.cell(1, i2).value
			


				val = table.cell(i3, i2).value

				print city, name, status, val
			
			
				if isinstance(person_count, int):
					item = {
								'head_type':2,
								'name':name,
								'parent_name':parent_name,
								'provider':providerc,
								'sub_provider':sub_provider,
								'franchisee':franchisee,
								'city':city,
								'area':area,
								'store_count':int(store_count) if isinstance(person_count, float) else 0,
								'person_count':int(person_count),
								#'status_time2':status_time2,
								#'status_type':status_type,
								'create_time':dt.now(),
								'update_time':dt.now()
							}
					val = table.cell(i3, i2).value

					if val:
					
						val = int(val)
						if status.find(u'修复') > -1:
							item['status_time2'] = val
						else:
							item['status_time1'] = val
						if status.find(u'紧急') > -1:
							item['status_type'] = 1
						else:
							item['status_type'] = 2
						print item.get('city'),item.get('status_type'), item.get('name')
					
						cal = DB.call.find_one({'name':name, 'provider':providerc, 'city':city, 'status_type':item['status_type']})
	 					print name, providerc, city, item['status_type'], 1 if cal else 0
	 					if cal:
	 						DB.call.update({'_id':cal['_id']},{'$set':item})
	 					else:
	 						DB.call.save(item)
	 					#time.sleep(1)

	 	
	 	



