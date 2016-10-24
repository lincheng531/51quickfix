#!/user/bin/env python
# encoding:utf-8

import xlrd
from pymongo import Connection
from bson.objectid import ObjectId
from datetime import datetime as dt

from pypinyin import pinyin, lazy_pinyin
import pypinyin


def get_pinyin_initials(text):
    if not text:return ""
    pinyin_text = ''.join([s[0] for s in lazy_pinyin(text) if len(s) > 0])
    #fixlist = [(u'单', 's'), (u'褚', 'c'), (u'解', 'x')]
    fixlist =  [(u'乘','C'),(u'乘','C'),(u'适','K'),(u'句','G'),(u'阚','K'),(u'车','C'),(u'叶','Y'),(u'合','H'),(u'冯','F'),(u'陶','T'),(u'汤','T'),(u'尾','W'),(u'贾','J'),
        (u'系','X'),(u'将','J'),(u'谷','G'),(u'宿','S'),(u'祭','Z'),(u'氏','S'),(u'石','S'),(u'盛','S'),(u'於','Y'),(u'强','Q'),(u'艾','A'),(u'塔','T'),(u'丁','D'),(u'种','Z'),(u'单','S'),
        (u'解','X'),(u'查','Z'),(u'区','O'),(u'繁','P'),(u'仇','Q'),(u'沈','S'),(u'宁','N'),(u'褚','C'),(u'适','K'),(u'句','G'),(u'阚','K'),(u'焦','J'),
        (u'车','C'),(u'叶','Y'),(u'合','H'),(u'冯','F'),(u'陶','T'),(u'汤','T'),(u'尾','W'),(u'贾','J'),(u'系','X'),(u'将','J'),(u'谷','G'),(u'宿','S'),(u'祭','Z'),(u'氏','S'),(u'石','S'),
        (u'盛','S'),(u'於','Y'),(u'强','Q'),(u'艾','A'),(u'塔','T'),(u'丁','D'),(u'种','Z'),(u'单','S'),(u'解','X'),(u'查','Z'),(u'区','O'),(u'繁','P'),(u'仇','Q'),(u'沈','S'),(u'宁','N'),(u'褚','C')
    ]

    res = []

    for i, j in zip(text, pinyin_text):
        for _i, _j in fixlist:
            if i == _i:
                j  = _j
        res.append(j.upper())

    return u''.join(res)


if __name__ == '__main__':
	conn   = Connection()
	DB     = conn['51quickfix'] 

	data   = xlrd.open_workbook(u'doc/push/餐厅联系人2.xlsx')
	table  = data.sheets()[1] 
	nrows  = table.nrows
	ncols  = table.ncols
	for index in range(1, nrows):
		no = str(int(table.cell(index, 0).value))
		name = table.cell(index, 2).value
		mobile = str(int(table.cell(index, 3).value))
		print no, name, mobile
		store = DB.store.find_one({'no':no})
		print store
		items = {
				u'store_id': str(store['_id']),
				u'is_staff': False, 
				u'user_permissions': [], 
				u'category': u'1', 
				u'city': store['city'], 
				u'area': u'华东区', 
				u'avatar_img': u'/static/img/store/2.png', 
				u'head_type': 2, 
				u'store': store['address'], 
				u'username': mobile, 
				u'company_logo': u'/static/img/store/2.png', 
				u'company': u'汉堡王', 
				u'is_active': 1,
				u'password': u'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs=', 
				u'source': u'汉堡王',
				u'name': name, 
				u'mobile': mobile, 
				u'create_time': dt.now(),
				u'_cls': u'User.User'
				}
		if not DB.user.find_one({'username':mobile}):
			DB.user.save(items)
		else:
			DB.user.update({'username':mobile},{'$set':items})









