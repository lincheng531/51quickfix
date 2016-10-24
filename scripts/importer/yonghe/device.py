# -*- encoding: utf-8 -*-
import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'../../..'))

from bson.objectid import ObjectId
from apps.base.utils import to_excel
import xlrd

def generate_rid():
    sheet   = xlrd.open_workbook(u'10家餐厅固定资产记录-160921.xlsx')
    table  = sheet.sheets()[2]
    nrows  = table.nrows
    ncols  = table.ncols

    col_map = {
        '1': '固定资产编号',
        '7': '设备名称',
        '9': '品牌',
        '10': '型号',
        '11': '规格',
        '0': '门店编号',
        'store_name': '门店名称',
        'store_brand': '门店品牌',
        'rid': '对应二维码',
    }

    store_map = {
        'SH031': '广元',
        'SH046': '万源',
        'SH048': '漕溪',
        'SH052': '东安',
        'SH055': '南方',
        'SH059': '漕宝',
        'SH074': '沪闵路',
        'SH077': '南站二店',
        'SH079': '莲花南路',
        'SH092': '锦江乐园',
    }

    devices = []

    for i in xrange(nrows):
        if i < 1:
            continue

        item = {}

        for j in xrange(ncols):
            cell = table.cell(i, j)
            data = cell.value
            key = str(j)

            if key in col_map:
                item[key] = str(data)

        item['store_brand'] = u'永和大王'
        item['rid'] = str(ObjectId())
        devices.append(item)

    for d in devices:
        d['store_name'] = store_map[d['0']]

    order = col_map.keys()
    trans_order = col_map.values()
    f_object = to_excel(devices, order, trans_order)

    with open('设备二维码打印20160928.xls', 'wb') as f:
        f.write(f_object.read())

generate_rid()