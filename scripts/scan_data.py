#!/user/bin/env python
#encoding:utf-8

from pymongo import Connection
from bson.objectid import ObjectId as _id


if __name__ == '__main__':
	conn = Connection()
	db = conn['51quickfix']

	print u'------------------没有开业时间的餐厅'
	for i in db.store.find():
		if not i.get('opening_time'):
			print i.get('name'), i.get('no')

	print u'------------------没有餐厅的设备'
	for i in db.device.find():
		if not i.get('store'):
			print i.get('_id')

		if not db.store.find_one({'_id':i.get('store')}):
			print i.get('_id')

	print u'-----------------没有标准设备的设备'
	for i in db.device.find():
		product =  db.product.find_one({'_id':i['product']})
		if not product:
			print i.get('_id')

	print u'-----------------没有零件的设备'
	for i in db.product.find():
		if db.spare.find({'product_name':i['name'], 'brand':i['brand']}).count() == 0:
			print i.get('name'), i.get('model'), i.get('brand_name')


	print u'----------------没有对应的服务服务商'
	for store in db.store.find({'city':u'上海市'}):
		for device in db.device.find({'store':store['_id']}):
			product = db.product.find_one({'_id':device['product']})

			if not db.call.find_one({'name':product['name'], 'brand':product['brand'], 'city':store['city']}):
				print i.get('name'), i.get('brand_name'), i.get('brand')







