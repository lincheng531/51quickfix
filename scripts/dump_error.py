#!/user/bin/env python
# encoding:utf-8

import xlrd
from pymongo import Connection
from bson.objectid import ObjectId
from datetime import datetime as dt

from pypinyin import pinyin, lazy_pinyin
import pypinyin



if __name__ == '__main__':
	conn   = Connection()
	DB     = conn['51quickfix']

	data   = xlrd.open_workbook(u'doc/error.xls')
	table  = data.sheets()[0] 
	nrows  = table.nrows
 	ncols  = table.ncols

 	keys   = ['brand', 'name', 'model', 'error', 'code',  'phen', 'spare', 'spare_code', 'status']								
 	for i in range(1, nrows):
 		items = {'head_type':2}
	 	for i2 in range(1, ncols):
	 		key = keys[i2-1]
	 		cell  = table.cell(i,i2).value
	 		items[key] = cell
	 	if len(items) > 6:
	 		brand = DB.brand.find_one({'name':items['brand']})
	 		if  brand: 
	 			product = DB.product.find_one({'name':items['name'], 'brand':brand['_id'], 'model':items['model']})
	 			if product:
	 				if items['status'] == u'非紧急':
	 					items['status'] = 2
	 				else:
	 					items['status'] = 1
	 				items['product'] = product['_id']
	 				DB.error_code.save(items)
	 			else:
	 				print items['name']
	 		else:
	 			print brand



























		 			
		 			