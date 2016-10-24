#!/user/bin/env python
# encoding:utf-8

import xlrd
from pymongo import Connection
from bson.objectid import ObjectId
from datetime import datetime as dt

from pypinyin import pinyin, lazy_pinyin
import pypinyin


def format(value):
	if isinstance(value, (int, float)):
		return value
	if value:
		return value.strip()
	return value


if __name__ == '__main__':
	conn   = Connection()
	DB     = conn['51quickfix']
	DB.product.find_and_modify({'_id':ObjectId('567e475e437f573362ae19bc')},{'$set':{'name':u'滤水系统，主店'}})

	data   = xlrd.open_workbook(u'doc/push/最新的标准设备表时效表.xls')
	table  = data.sheets()[0] 
	nrows  = table.nrows
 	ncols  = table.ncols
 	keys   = ['_id', 'category', 'name', 'ecategory', 'brand', 'purchase_code', 'description', 'supplier', 'model', 'specification', 'efcategory', 'repair_time']						
 	for i in range(1, nrows):
 		items = {}
 		for i2 in range(ncols):
 			key = keys[i2]
 			value = format(table.cell(i,i2).value)
 			if key == 'repair_time':
 				print key
 				value = int(value)
 			items.update({key:value})

 		oid = items.get('_id')
 		if not oid:
 			brand = DB.brand.find_one({'name':items['brand']})
 			supplier = DB.supplier.find_one({'name2':items['brand']})
 			items['brand'] = brand['_id']
 			items['brand_name'] = brand['name']
 			items['supplier'] = supplier['_id']
 			items['update_time'] = dt.now()
 			items['create_time'] = dt.now()
 			del items['_id']
 			print 'add-----',DB.product.save(items)
 		else:
 			DB.product.update({'_id':ObjectId(oid)},{'$set':{'repair_time':items['repair_time']}})



		 			
		 			