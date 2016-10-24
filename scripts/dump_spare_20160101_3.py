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

	data   = xlrd.open_workbook(u'doc/push/零配件表.xlsx')

	
	keys = ['idx', u'pp',u'sb',u'xh',u'no',u'name',u'brand', u'price', u'warranty1',u'warranty2',u'warranty3',u'content']
	
	for tab in range(30):
		print tab
		table  = data.sheets()[tab] 
		nrows  = table.nrows
	 	ncols  = table.ncols

	 	for r in range(nrows):
	 		if r >2:
		 		items = {'create_time':dt.now(), 'update_time':dt.now()}
		 		for c in range(ncols):
		 			key, val = keys[c], table.cell(r, c).value
		 			val = val.strip() if isinstance(val, basestring) else val
		 			if key <> 'idx':
		 				if key == 'no' and val:
		 					val = str(int(val)) if isinstance(val, (float, int)) else val
		 				if key in ['warranty1', 'warranty2', 'warranty3']:
		 					if isinstance(val, (int, float)):
		 						pass
		 					elif u'年' in val:
		 						val = int(val.replace(u'年','')) * 12
		 					elif u'个月' in val:
		 						val = int(val.replace(u'个月',''))
		 					elif u'月' in val:
		 						val = int(val.replace(u'月', ''))
		 					elif u'根据整机保固时效' == val:
		 						val = ''
		 				if key == 'price':
		 					val = float(val) if val else 0
		 				if val or val in [0, '0']:
		 					items.update({keys[c]:val})
		 		'''
		 		pp, sbc, xhc = [items.get(i) for i in ['pp', 'sb', 'xh']]
		 		xhs = [i.strip() for i in xhc.split('|')] if xhc else ''
		 		if not sbc:continue
		 		sbs = sbc.split('|')
		 		for sb in sbs:
			 		for xh in xhs:
				 		brand = DB.brand.find_one({'name':pp})
				 		if not brand:
				 			print pp 
				 			raise
				 		bkc = DB.product.find_one({'name':sb.strip(), 'brand':brand['_id']})
				 		if not bkc:
				 			print tab, r, sb, xh, brand['_id']
				 		else:
				 			#print tab, r, sb, xh, brand['_id'], items
				 			items['product'] = bkc['_id']
				 			if items.get('pp'):del items['pp']
				 			if items.get('xh'):del items['xh']
				 			if items.get('sb'):del items['sb']
							#if not DB.spare.find_one({'product':bkc['_id'], 'no':items.get('no'), 'name':items.get('name'), 'brand':items.get('brand')}) and items.get('name'):
				 			items['price'] = round(items.get('price', 0), 2)
				 			if items.get('name') and items.get('name') <> items['no']:
				 				DB.spare.save({
				 					'product_name':sb,
				 					'product':items['product'],
				 					'brand':brand['_id'],
				 					'create_time':items['create_time'],
				 					'name':items['name'],
				 					'no':items['no'],
				 					'price':items['price'],
				 					'update_time':items['update_time']
				 				})
				 			else:
				 				print '>>>>> no name', tab
				'''



