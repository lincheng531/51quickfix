#!/user/bin/env python
# encoding:utf-8

import xlrd
import random
from pymongo import Connection
from bson.objectid import ObjectId
import time
from datetime import datetime as dt

from pypinyin import pinyin, lazy_pinyin
import pypinyin


if __name__ == '__main__':
	conn   = Connection()
	db     = conn['51quickfix']

	stores1 = db.store.find({'area':u'华东区', 'franchisee':'', 'no':{'$ne':'21158'}})
	stores2 = db.store.find({'area':u'华北区', 'franchisee':'', 'no':{'$ne':'16913'}})
	stores3 = db.store.find({'area':u'华南区', 'franchisee':'', 'no':{'$ne':'20989'}})
	stores4 = db.store.find({'franchisee':{'$ne':''},'no':{'$ne':'20082'}}) 


	store1    = db.store.find_one({'no':'21158'})
	devices1  = list(db.device.find({'store':store1['_id']}))
	for st1 in stores1:
		db.device.remove({'store':st1['_id']})
		for de1 in devices1:
			del de1['_id']
			de1['rid'] = ''
			de1['store'] = st1['_id']
			db.device.save(de1)

		for i in range(random.randint(0,5)):
			dev1 = db.device.find_one({'store':st1['_id']})
			db.device.remove({'_id':dev1['_id']})

	store2    = db.store.find_one({'no':'16913'})
	devices2  = list(db.device.find({'store':store2['_id']}))
	for st2 in stores2:
		db.device.remove({'store':st2['_id']})
		for de2 in devices2:
			del de2['_id']
			de2['rid'] = ''
			de2['store'] = st2['_id']
			db.device.save(de2)

		for i in range(random.randint(0,5)):
			dev2 = db.device.find_one({'store':st2['_id']})
			db.device.remove({'_id':dev2['_id']})

	store3    = db.store.find_one({'no':'20989'})
	devices3  = list(db.device.find({'store':store3['_id']}))
	for st3 in stores3:
		db.device.remove({'store':st3['_id']}) 
		for de3 in devices3:
			del de3['_id']
			de3['rid'] = ''
			de3['store'] = st3['_id']
			db.device.save(de3)

		for i in range(random.randint(0,5)):
			dev3 = db.device.find_one({'store':st3['_id']})
			db.device.remove({'_id':dev3['_id']})

	store4    = db.store.find_one({'no':'20082'})
	devices4  = list(db.device.find({'store':store4['_id']}))
	for st4 in stores4:
		db.device.remove({'store':st3['_id']})
		for de4 in devices4:
			del de4['_id']
			de4['rid'] = ''
			de4['store'] = st4['_id']
			db.device.save(de4)
		for i in range(random.randint(0,5)):
			dev4 = db.device.find_one({'store':st4['_id']})
			db.device.remove({'_id':dev4['_id']})



	 	
	 	



