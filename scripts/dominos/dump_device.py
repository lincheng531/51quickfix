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

	data   = xlrd.open_workbook(u'doc/20160627达美乐汇融店和蓝村店的数据2.xlsx')
	keys   = ['item', 'rid', 'supplier', 'category', 'efcategory', 'ecategory', 'po',  'name', 'description', 'brand', 'model', 'specifications', 'psnumber', 'provider', 'price', 'purchase_date', 'expiration_date', 'installation_date', 'expiration_date', 'tax_rate', 'tax', 'remarks', 'scrap_time']		
	
	for tab in range(1, 57):
		table  = data.sheets()[tab]
		nrows  = table.nrows
	 	ncols  = table.ncols			
	 	for i in range(5, nrows):
			item = {'head_type':3,'area':u'华东区','city':u'上海市'}
	 		for i2 in range(ncols):
	 			key   = keys[i2]
	 			cell  = table.cell(i,i2).value
	 			item.update({key:cell})
		 	if item.get('name'):
		 		item['name'] = item['name'].strip()
		 		item['initial'] = get_pinyin_initials(item['name'])

		 	store = DB.store.find_one({'no':table.name, 'head_type':3})

		 	if item.get('initial') and item.get('name') and store and item.get('rid') and store['no'] in ['049', '016']:
		 		item['store'] = store['_id']
		 		supplier_name = item.get('supplier')
		 		supplier = DB.supplier.find_one({'name':supplier_name})
		 		if not supplier:
		 			item['supplier'] = DB.supplier.save({
					 						'name':supplier_name,
					 						'initial':get_pinyin_initials(supplier_name),
					 						'create_time':dt.now(),
					 						'update_time':dt.now()
					 				})
		 		else:
		 			item['supplier'] = supplier['_id']
		 		brand_name = item.get('brand')
		 		if brand_name:
		 			brand = DB.brand.find_one({'name':brand_name})
		 			if not brand:
		 				brand_id = DB.brand.save({
			 					'update_time': dt.now(),
								'name': brand_name,
								'initial': get_pinyin_initials(brand_name),
								'create_time': dt.now()
		 					})
		 			else:
		 				brand_id = brand['_id']
		 		product_query = {'name':item.get('name')}
		 		if item.get('brand'):
		 			product_query['brand_name'] = item.get('brand')
		 			product_query['brand'] = brand_id
		 		if item.get('model'):
		 			product_query['model'] = item.get('model')
		 		if item.get('specification'):
		 			product_query['specification'] = item.get('specifications')
		 		product = DB.product.find_one(product_query)
		 		if product:
		 			item['product'] = product['_id']
		 		else:
		 		    item['product'] = DB.product.save({
		 		    						'head_type':3,
						 		    		'category': item.get('category'),
											'initial': get_pinyin_initials(item.get('name')),
											'description': item.get('description'),
											'ecategory': item.get('ecategory'),
											'brand':  brand_id,
											'barcode': item.get('barcode'),
											'brand_name': brand_name,
											'purchase_code': item.get('purchase_code'),
											'name': item.get('name'),
											'item': item.get('item'),
											'supplier': item['supplier'],
											'model': item.get('model'),
											'specification':item.get('specifications'), 
											'efcategory': item.get('efcategory')
						 		    	})

		 		DB.device.save(item)
		 		
 		 		
		 		
		 		
		 			
		 			