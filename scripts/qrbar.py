#!/user/bin/env python
#encoding:utf-8

import os  
import sys
import xlrd
import xlwt
#import qrcode  
from PIL import Image  
from PIL import ImageDraw
from PIL import ImageFont
from bson.objectid import ObjectId as _id
 

def write(string):
	font = ImageFont.truetype('msyh.ttf',18)
	im   = Image.new("RGBA",(600,400),(255,255,255))
	draw = ImageDraw.Draw(im)
	for index, txt in enumerate(string):
		draw.text( (10,44*index), txt, font=font, fill=(0,0,0))
	del draw
	return im


def gen_qrcode(string, path, logo="data/bk_logo.png"):
	im = write(string)
	qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=6, border=1)
	qr.add_data(string)
	qr.make(fit=True)
	img = qr.make_image()
	img = img.convert("RGBA")
	if logo and os.path.exists(logo):
		icon = Image.open(logo)
		img_w, img_h = img.size
		factor = 4
		size_w = int(img_w / factor)
		size_h = int(img_h / factor)
		icon_w, icon_h = icon.size
		if icon_w > size_w:
			icon_w = size_w
		if icon_h > size_h:
			icon_h = size_h
		icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
		w = int((img_w - icon_w) / 2)
		h = int((img_h - icon_h) / 2)
		icon = icon.convert("RGBA")
		img.paste(icon, (w, h), icon)
	#im.paste(img, (300, 70), img)
	img.save(path)


def create1():
 	data1   = xlrd.open_workbook(u'data/餐厅信息.xlsx')
 	columns = [ u'使用部门编号',
 				u'使用部门',
 				u'地址',
 				u'电话',
 				u'传真',
 				u'邮箱',
 				u'联系人',
 				u'地区',
 				u'城市',
 				u'开店日期',
 				u'关店日期',
 				u'保固日期',
 				u'服务商',
 				u'冷库服务商（保固期外）',
 				u'冷库服务商（保固期内）',
 				u'联系人',
 				u'联系人手机号码',
 				u'省	',
 				u'区域',
 				u'公司',
 				u'管理部门']
 	table1  = data1.sheets()[0] 
 	nrows 	= table1.nrows
 	ncols 	= table1.ncols
 	result1 = {}
 	for i in range(nrows):
 		if i > 1:
 			item = {}
	 		for i3 in range(ncols):
	 			key = columns[i3]
	 			cell   = table1.cell(i,i3).value
	 			item.update({key:cell})
	 		result1.update({item[u'使用部门编号']:item})

 	data2      = xlrd.open_workbook(u'data/设备信息.xlsx')
 	table2     = data2.sheets()[0] 
 	name, code =  table2.cell(1,23).value, table2.cell(1,24).value
 	columns = [	
 				u"汇总",
 				u"B",
 				u"区域", 
 				u"D",
 				u"E",
 				U"F",
 				u'设备设施名称',
 				u'Description',
 				u"I",
 				u"J",
 				u"K",
 				u"供应商",
 				u"数量",
 				u"单价",
 				u"合计",
 				u"安装费",
 				u"运输费",
 				u"其它费用",
 				u"合计",
 				u"备注",
 				u"提供者",
 				u"型号",
 				u"生产日期",
 				u"安装日期",
 				u"过期日期",
 				u"类别",
 				u"设备设施类别",
 				u"设备类别",
 				u"品牌",
 				u"固定资产编号",
 				u"财富类别代码",
 				u"制作厂商",
 				u"规格",
 				u"设备出厂序列号",
 				u"使用状态",
 				u"存放地",
 				u"购置日期",
 				u"单位",
 				u"报废时限",
 				u"每月折旧金额"]

 	nrows 	= table2.nrows
 	ncols 	= table2.ncols
 	result2 = []
 	for i2 in range(nrows):
 		if i2 > 3:
 			item = {u'使用部门编号':code, u'使用部门':name}
	 		for i4 in range(len(columns)):
	 			key  = columns[i4]
	 			cell = table2.cell(i2,i4).value
	 			item.update({key:cell})
	 		result2.append(item)

	for item2 in result2:
		code =  item2.get(u'使用部门编号')
		item2.update(result1.get(code))
		keys = [u'固定资产编号',u'设备设施名称',u'制作厂商',u'型号',u'规格',u'管理部门',u'使用部门',u'使用部门编号',u'设备出厂序列号']
		data = []
		for key in keys:
			v = item2.get(key)
			if isinstance(v, (float, int)):
				v = str(int(v))
			data.append(u"{}：{}".format(key, v))
		gen_qrcode(data, 'logo/{}.jpg'.format(item2.get(u'固定资产编号')))


def create2():
 	data1   = xlrd.open_workbook(u'data/二维码信息-模板1.xlsx')
 	columns = [ 
			 	u"流水号",	
			 	u"交店日期",
			 	u"区域",	
			 	u"省市",	
			 	u"城市",
			 	u"餐厅名称",	
			 	u"餐厅编号",	
			 	u"设备使用区域",	
			 	u"类别",	
			 	u"设备名称",	
			 	u"Description",	
			 	u"品牌",
			 	u"型号",
			 	u"规格",
			 	u"供应商",	
			 	u"单位",	
			 	u"数量",
			 	u"单价",	
			 	u"合计",
			 	u"安装费厂商",	
			 	u"运输费粤中",
			 	u"其它费用",
			 	u"合计",
			 	u"备注",	
			 	u"提供者",	
			 	u"过保日期",	
			 	u"使用状态	",
			 	u"存放地",	
			 	u"报修类别	",
			 	u"设备设施类别",	
			 	u"生产序列号",	
			 	u"采购日期",
			 	u"固定资产编号",	
			 	u"财务类别代码",	
			 	u"报废时限",	
			 	u"每月折旧金额"
 	]
 	table1  = data1.sheets()[0] 
 	nrows 	= table1.nrows
 	ncols 	= table1.ncols
 	result1 = []
 	for i in range(nrows):
 		if i > 3:
 			item = {}
	 		for i3 in range(ncols):
	 			key = columns[i3]
	 			cell   = table1.cell(i,i3).value
	 			print key, cell
	 			item.update({key:cell})
	 		if item.get(u'流水号'):
	 			result1.append(item)

	print result1
	for item2 in result1:
		code =  item2.get(u'流水号')
		keys = [u'固定资产编号',u'区域',u'城市',u'餐厅名称',u'餐厅编号',u'设备名称',u'品牌',u'型号',u'规格']
		keys2 = [
				u'流水号',
				u'交店日期',
				u'区域',
				u'省市',
				u'城市',
				u'餐厅名称',
				u'餐厅编号',
				u'类别',
				u'设备名称',
				u'品牌', 
				u'型号', 
				u'规格']
		data = []
		for key in keys:
			v = item2.get(key)
			if isinstance(v, (float, int)):
				v = str(int(v))
			if key == u'固定资产编号':key=u'二维码'
			data.append(u"{}：{}".format(key, v))
		data2 = []
		for key2 in keys2:
			v2 = item2.get(key2)
			data2.append(u"{}:{}".format(key2, v2))
		print data2
		gen_qrcode(data2, 'logo/{}.jpg'.format(item2.get(u'固定资产编号')), "data/bk_logo.png", data2)


def barcode():
	w = xlwt.Workbook()
	ws = w.add_sheet('barcode')
	for i in range(10000):
		cid = str(_id())
		ws.write(i,0, cid)
	w.save('20170208.xls')

if __name__ == '__main__':
	barcode()
	'''
	for i in range(101):
		cid = str(_id())
		gen_qrcode(cid, 'logo/bk/{}.jpg'.format(cid))
	'''


		


	

	
