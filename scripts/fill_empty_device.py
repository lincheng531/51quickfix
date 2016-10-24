# -*- encoding: utf-8 -*-
from pymongo import Connection
from bson import ObjectId

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

conn = Connection()
DB = conn['51quickfix']
count = 0

devices = list(DB.device.find({'store':ObjectId('566a5ef7437f577c0979d5e0')}))
for item in devices:
    item['test'] = True

for company in DB.store.find({'head_type': 2}):
    if not DB.device.find({'store': company['_id']}).count():
        count += 1
        print company['name'].encode('utf-8'), company['no'], company['city'].encode('utf-8')

        for item in devices:
            del item['_id']
            item['store'] = company['_id']

        DB.device.insert(devices)

print count