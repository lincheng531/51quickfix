#!/user/bin/env python
# encoding:utf-8

import xlrd
import random
from pymongo import Connection
from bson.objectid import ObjectId
import time
from datetime import datetime as dt


if __name__ == '__main__':
	conn   = Connection()
	db     = conn['51quickfix']

	for store in db.store.find():
		if db.store.find({'no':store['no']}).count() > 1:
			for store1 in db.store.find({'no':store['no']}):
				pass
