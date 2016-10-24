#!/user/bin/env python
# encoding:utf-8

import xlrd
from pymongo import Connection
from bson.objectid import ObjectId
from datetime import datetime as dt


if __name__ == '__main__':
	conn   = Connection()
	DB     = conn['51quickfix']

	data   = xlrd.open_workbook(u'doc/charge.xlsx')

	keys = ['company','area','status', 'time_slot','fix_time','quickfix','quickfix1','quickfix2','quickfix3','quickfix4', 'traffic1','traffic2','traffic3']
	
	table  = data.sheets()[0] 
	nrows  = table.nrows
 	ncols  = table.ncols


 	for r in range(nrows):
 		if r >1:
	 		items = {'create_time':dt.now(), 'update_time':dt.now()}
	 		for c in range(ncols):
	 			key, val = keys[c], table.cell(r, c).value
	 			if not key in ['company', 'area', 'time_slot'] and val:
	 				print val
	 				val = int(val)
	 			items.update({key:val})
	 		time_slot =  items.get('time_slot')
	 		if time_slot:
	 			if items.get('status') == 1:
	 				sta, end = [int(i.replace(':00','')) for i in time_slot.split('-')]
	 				if sta == 8 and end == 20:
	 					items.update({'fix_time_type':1})
	 				else:
	 					items.update({'fix_time_type':2})
	 			else:
	 				items.update({'fix_time_type':3})
	 		if items.get('status') in [1,2]:
	 			items['head_type'] = 2
 	 			DB.charge.save(items)



