#!/user/bin/env python
# encoding:utf-8

import xlrd
from pymongo import Connection



def format(value):
	if isinstance(value, (float, int)):
		return value
	if value:
		return value.strip()
	return value

if __name__ == '__main__':
	conn   = Connection()
	DB     = conn['51quickfix']

	data   = xlrd.open_workbook(u'doc/push/设备对应服务商.xlsx')
	table  = data.sheets()[0] 
	nrows  = table.nrows
	ncols  = table.ncols

	data = []
	for r in range(1, nrows):
		items = {}
		keys  = ['item', 'barcode', 'purchase_code', 'category', 'efcategory', 'ecategory',  'name', 'description', 'specification', 'brand', 'model', 'supplier', 'warranty_in', 'warranty_out1', 'warranty_out2', 'warranty_out3']	
 		for c in range(ncols):
 			key, value = keys[c], format(table.cell(r, c).value)
 			items.update({key:value})
 		brand = DB.brand.find_one({'name':items['brand']})
 		if not brand:
 			print 1, r, items['brand']
 		
 		else:
 			query = {'name':items['name'].strip(), 'brand':brand['_id']}

 			DB.call.save({
			 				'head_type':2,
			 				'city':u'上海市',
			 				#'product':product['_id'],
			 				'name':items['name'],
			 				'brand':brand['_id'],
			 				'model':items['model'],
			 				'warranty_in':items['warranty_in'],
			 				'warranty_out1':items['warranty_out1'],
			 				'warranty_out2':items['warranty_out2'],
			 				'warranty_out3':items['warranty_out3']
 				})
			








 	