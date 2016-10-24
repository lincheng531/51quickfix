#!/user/bin/env python
#encoding:utf-8
import os
import time
import requests
from bson.objectid import ObjectId
from datetime import datetime as dt
from pymongo import Connection


DB = Connection()['51quickfix']


if __name__ == '__main__':
	user = DB.user.find_and_modify({'username':'13585753381'},{'$set':{'category':'5'}})
	roles = [
				{'name':u'权限控制','code':'apps_store_role_list'},
				{'name':u'盘点列表', 'code':'apps_store_inventory_list'},
				{'name':u'固定资产列表', 'code':'apps_store_assets_list'},
				{'name':u'用户中心', 'code':'apps_store_account_list'},
				{'name':u'维修列表', 'code':'apps_store_repair_list'},
				{'name':u'创建账户', 'code':'apps_store_account_append'},
				{'name':u'更新权限', 'code':'apps_store_role_edit'},
				{'name':u'查看餐厅', 'code':'apps_store_assets_store'},
				{'name':u'编辑餐厅', 'code':'apps_store_assets_store_edit'},  
				{'name':u'查看资产', 'code':'apps_store_assets_detail'},
				{'name':u'编辑资产', 'code':'apps_store_assets_edit'}, 
				{'name':u'申请盘点', 'code':'apps_store_inventory_append'},
				{'name':u'盘点明细', 'code':'apps_store_inventory_detail'}

			]
	for i in roles:
		role =  DB.role.find_one({'code':i['code']})
		if not role:
			role_id = DB.role.save({'create_time':dt.now(), 'update_time':dt.now(), 'name':i['name'], 'code':i['code']})
		else:
			DB.role.update({'_id':role['_id']},{'$set':i})
			role_id = role['_id']

		DB.user_role.save({'user':user['_id'], 'role':role_id, 'create_time':dt.now(), 'update_time':dt.now()})




