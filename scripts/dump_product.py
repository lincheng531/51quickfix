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

	data   = xlrd.open_workbook(u'doc/product.xlsx')
	table  = data.sheets()[0] 
	nrows  = table.nrows
 	ncols  = table.ncols
 	keys   = ['item', 'barcode', 'purchase_code', 'category', 'efcategory', 'ecategory',  'name', 'description', 'specification', 'brand', 'model', 'supplier']								
 	for i in range(nrows):
 		if i > 0:
 			item = {}
	 		for i2 in range(ncols):
	 			if len(keys) >= i2:
		 			key   = keys[i2]
		 			cell  = table.cell(i,i2).value
		 			item.update({key:cell})
		 	if item.get('name'):
		 		item['initial'] = get_pinyin_initials(item['name'])
		 	if item.get('initial'):
		 		brand_name = item.get('brand')
		 		supplier_name =  item.get('supplier')
		 		supp =  DB.supplier.find_one({'name':supplier_name})
		 		if not supp:
		 			supp = DB.supplier.save({'name':supplier_name, 'name2':brand_name, 'initial':get_pinyin_initials(supplier_name), 'create_time':dt.now(), 'update_time':dt.now()})
		 			item['supplier'] = supp
		 		else:
		 			item['supplier'] = supp['_id']

		 		brand   = DB.brand.find_one({'name':brand_name})
		 		if not brand:
		 			item['brand'] = DB.brand.save({'name':brand_name, 'name2':supplier_name, 'initial':get_pinyin_initials(brand_name), 'create_time':dt.now(), 'update_time':dt.now()})
		 		else:
		 			item['brand'] = brand['_id']
		 		item['brand_name'] = brand_name
		 		ecategory =  item['ecategory']
		 		call =  DB.call.find_one({'name':ecategory})
		 		if not call:
		 			'''
						员工设备
						圣代机
						传送带
						热饮机
						保险箱
						商用微波炉
						不锈钢小件
						工作台
						水槽
						品牌 名称 型号 规格
						维修时效表只有bonny所有有设备缺失
		 			'''
		 			print 'not call', ecategory
		 		
		 		if not DB.product.find_one({'name':item.get('name'), 'brand':item.get('brand'), 'model':item.get('model'), 'specification':item.get('specification')}):
		 			DB.product.save(item)
		 		else:
		 			print item.get('name'), item.get('brand'), item.get('model')
		 			
		 			