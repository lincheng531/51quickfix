#!/user/bin/env python
#encoding:utf-8
'''
新世界 567e9351437f573af9760104 薯条站 Franke 薯条站 Fabristeel 
五角场 567e56c9437f573afc5076d6 制冰机 Scotsman 制冰机 Scotsman 
青浦吾悦广场 566123f4437f5758bec00500 速溶热饮机 Pilot 汽水机, 甜品站 Cornelius 
'''
import xlwt
import requests
from pymongo import Connection

conn = Connection()
db = conn['51quickfix']

workbook = xlwt.Workbook()
workbook.add_sheet(u'没有服务商', cell_overwrite_ok=True)
sheet = workbook.get_sheet(0)
workbook.add_sheet(u'有服务商没有维修人员', cell_overwrite_ok=True)
sheet1 = workbook.get_sheet(1)

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
           "Referer": "http://114.119.37.246/api/v1/account/signin"}
session = requests.Session()
body  = session.post('http://114.119.37.246/api/v1/account/signin',
                               data={'username':'11111111111','password':'000000'},
                               headers=headers,
                               )
index, index1 = 0, 0
for store in db.store.find({'city':u'上海市','no':'15425'}):
    for device in  db.device.find({'store':store['_id']}):
        body2 = session.post('http://114.119.37.246/api/v1/merchant/scan',data={'no':device.get('rid')},headers=headers)
        scan =  body2.json()
        body3 = session.post('http://114.119.37.246/api/v1/merchant/call',data={
                'cid':scan['info'].get('assets'),
                'error':u'错误描述',
                'state':1,
                'type':2
            }, headers=headers)
        
        call =  body3.json()
        print call.get('alert') 
        if call.get('alert') not in  [u'派单成功！请耐心等候维修工回复吧！',u'该区域未找到相应的维修人员']:
            if call.get('alert') == u'没有找到维修该设备的服务商，请联系管理员' and device.get('brand') not in ['HEC','Cornelius'] and device.get('name') <> u'保险箱':
                index += 1
                product = db.product.find_one({'_id':device['product']})
                brand = db.brand.find_one({'_id':product['brand']})
                print store['name'], device.get('_id'), device.get('name'), device.get('brand'), product['name'], brand['name'], call['alert']
                sheet.write(index, 1, store['name'])
                sheet.write(index, 2, store['no'])
                sheet.write(index, 3, device.get('name'))
                sheet.write(index, 4, device.get('brand'))
            if call.get('alert') == u'该区域未找到相应的维修人员' and device.get('brand') not in ['HEC','Cornelius'] and device.get('name') <> u'保险箱':
                index1 += 1
                product = db.product.find_one({'_id':device['product']})
                brand = db.brand.find_one({'_id':product['brand']})
                print store['name'], device.get('_id'), device.get('name'), device.get('brand'), product['name'], brand['name'], call['alert']
                sheet1.write(index+1, 1, store['name'])
                sheet1.write(index+1, 2, store['no'])
                sheet1.write(index+1, 3, device.get('name'))
                sheet1.write(index+1, 4, device.get('brand'))

workbook.save('apps/test.xls')
        
