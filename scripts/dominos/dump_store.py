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

	data   = xlrd.open_workbook(u'doc/餐厅资料.xlsx')

	keys = ['index', u'_', u'_', u'city', u'district', u'no', u'name', u'delivery_time', u'opening_time',u'close_time',
			u'tel', u'fax', u'business_hours',u'address',u'email',
			u'store_manager', u'mobile', '_', '_', u'business_type',u'_',u'email','_']
	AREA = {2:u'华东区', 3:u'华北区'}
	for tab_index in range(0, 1):
		table  = data.sheets()[tab_index] 
		nrows  = table.nrows
 		ncols  = table.ncols
 		for i in range(1, nrows):

			items = {'area':AREA.get(tab_index)}
 			for i2 in range(ncols):
 				key   = keys[i2]
 				val   = table.cell(i,i2).value
		 		val   = val.strip() if isinstance(val, basestring) else val
		 		items.update({key:val})
		 	del items['_']
		 	
		 	if len(items) > 2:
		 		if not DB.store.find_one({'no':items.get('no')}):
		 			items['no']   = str(items['no'])
		 			try:
		 				items['mobile'] = str(int(items['mobile']))
		 			except Exception as e:
		 				print str(e)

		 			try:
		 				items['tel'] = '021-{}'.format(str(int(items['tel'])))
		 			except Exception as e:
		 				print str(e)
		 			try:
		 				items['opening_time'] = dt.strptime(items['opening_time'], '%Y/%m/%d')
		 			except Exception as e:
		 				print str(e), items['opening_time']
		 				raise
		 			try:
		 				items['delivery_time'] = dt.strptime(items['delivery_time'], '%Y/%m/%d')
		 			except Exception as e:
		 				print str(e), items['delivery_time']
		 			try:
		 				items['close_time'] = dt.strptime(items['close_time'], '%Y/%m/%d')
		 			except Exception as e:
		 				print str(e), items['close_time']
		 				#del items['close_time']
		 			items['city'] = items['city'] if u'市' in items['city'] else u"{}市".format(items['city'])
		 			items['initial'] = get_pinyin_initials(items['name'])
		 			items['head_type'] = 3
		 			del items['index']
		 			print items
		 			items['no'] = items['no'].strip()
		 			items['name'] = items['name'].strip()
		 			items['franchisee'] = u'上海达美乐比萨有限公司'
		 			DB.store.save(items)
		 		else:
		 			print items.get('city'), items.get('name')
	 		
	 		








