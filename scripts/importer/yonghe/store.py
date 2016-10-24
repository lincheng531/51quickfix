# -*- encoding: utf-8 -*-
from bson.objectid import ObjectId
from apps.base.utils import to_excel
import xlrd

def generate_rid():
    sheet   = xlrd.open_workbook(u'10家餐厅固定资产记录-160921.xlsx')
    table  = sheet.sheets()[0]
    nrows  = table.nrows
    ncols  = table.ncols

    col_map = {
        '6': '门店编号',
        '7': '门店名称',
        '14': '门店地址',
        'rid': '门店对应二维码链接',
    }

    stores = []

    for i in xrange(nrows):
        if i < 2:
            continue

        item = {}

        for j in xrange(ncols):
            cell = table.cell(i, j)
            data = cell.value
            key = str(j)
            if key in col_map:
                item[key] = str(data)

        item['rid'] = str(ObjectId())
        stores.append(item)

    order = col_map.keys()
    trans_order = col_map.values()
    f_object = to_excel(stores, order, trans_order)

    with open('餐厅二维码打印20160928.xls', 'wb') as f:
        f.write(f_object.read())

generate_rid()


