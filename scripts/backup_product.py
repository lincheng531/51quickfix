#!/user/bin/env python
#encoding:utf-8

import xlrd, xlwt
from pymongo import Connection
from bson.objectid import ObjectId
from datetime import datetime as dt

from pypinyin import pinyin, lazy_pinyin
import pypinyin 


if __name__ == '__main__':
	conn   = Connection()
	DB     = conn['51quickfix2']

	workbook = xlwt.Workbook()
	workbook.add_sheet('1', cell_overwrite_ok=True)
	sheet = workbook.get_sheet(0)

	products = DB.product.find().sort('name', -1)
	keys = ['_id', 'category', 'name', 'ecategory', 'brand', 'purchase_code', 'description', 'supplier', 'model', 'specification', 'efcategory']
	sheet.row(0).height_mismatch = True
	sheet.row(0).height  = 600
	headers = [u'ID请不要修改', u'分类', u'设备名称', u'类别', u'品牌', u'采购码', u'描述', u'供应商',  u'型号', u'规格', u'设备/设施类别']
	for count, header in enumerate(headers):
		sheet.col(0).width   = 6000
		sheet.write(0, count, header, xlwt.easyxf("pattern: pattern solid, fore_color red;font: color white;align: wrap on,vertical center, horizontal center;"))
	for index, product in enumerate(products):
		sheet.col(index+1).width   = 6000
		for index2, key in enumerate(keys):
			val = product.get(key)
			if key == 'supplier':
				val = DB.supplier.find_one({'_id':val}).get('name')
			elif key == 'brand':
				val = DB.brand.find_one({'_id':val}).get('name')
			elif key == '_id':
				val = str(val)
			sheet.write(index+1, index2, val)




	workbook.save('/apps/2.xls')

