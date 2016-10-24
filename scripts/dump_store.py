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

	data   = xlrd.open_workbook(u'doc/store_20160825.xlsx')

	keys = ['index',u'no',u'store_manager',u'delivery_time', 'mobile', u'tel', 'city',u'address',u'zip',u'email']
	AREA = {'1':u'华东区', '2':u'华南区', '3':u'华北区', 3:u'华东区'}
	for tab_index in [1]:
		table  = data.sheets()[tab_index] 
		nrows  = table.nrows
 		ncols  = table.ncols
 		for i in range(nrows):
 			if i > 1:
 				items = {}
	 			for i2 in range(9):
                                        #print i2
	 				key   = keys[i2]
	 				val   = table.cell(i,i2).value
			 		val = val.strip() if isinstance(val, basestring) else val
			 		items.update({key:val})
			 	#if len(items) > 2:
                                items['area'] = AREA.get(items['index'])
                                items['name'] = items['no'][5:].replace('\n','').replace('\t','').replace(' ', '')
                                items['no'] = items['no'][0:5]
                                #print 'u\'{}\','.format( items['no'])
                                #print DB.store.find_one({'no':items['no']})
		 		items['city'] = items['city'] if u'市' in items['city'] else u"{}市".format(items['city'])
                                if DB.store.find_one({'no':items['no']}):
                                    pass
                                else:
                                    print items['no']
                                    if 1:
		 			items['no']   = str(int(items['no']))
		 			try:
		 				items['mobile'] = str(int(items['mobile']))
		 			except Exception as e:
		 				pass
		 				#print str(e)
		 			try:
		 				items['opening_time'] = dt.strptime(items['opening_time'], '%Y/%m/%d')
		 			except Exception as e:
                                                pass
		 			 	#print str(e)
		 				#del items['opening_time']
		 			try:
		 				items['delivery_time'] = dt.strptime(items['delivery_time'], '%Y/%m/%d')
		 			except Exception as e:
		 				pass
                                                #print str(e)
		 				#del items['delivery_time']
		 			try:
		 				items['close_time'] = dt.strptime(items['close_time'], '%Y/%m/%d')
		 			except Exception as e:
		 				pass
                                                #print str(e)
		 				#del items['close_time']
		 			items['city'] = items['city'] if u'市' in items['city'] else u"{}市".format(items['city'])
		 			items['initial'] = get_pinyin_initials(items['name'])
		 			items['head_type'] = 2
		 			del items['index']
		 			DB.store.save(items)
		 		#else:
		 		#    print items.get('city'), items.get('name')

                                






