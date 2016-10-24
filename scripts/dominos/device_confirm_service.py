#!/user/bin/env python
# encoding:utf-8

import xlrd
from pymongo import Connection

if __name__ == '__main__':
	conn = Connection()
	db   = conn['51quickfix']
	p = []
	devices = db.device.find()
	for device in devices:
		name, brand_name = [device.get(i) for i in ['name', 'brand']]
		brand = db.brand.find_one({'name':brand_name})
		if brand:
			key = '{}-{}'.format(name, brand_name)
			if not db.call.find_one({'name':name, 'brand':brand['_id']}) and key not:
				print name, brand['name'], device.get('store') 
				p.append(key)
