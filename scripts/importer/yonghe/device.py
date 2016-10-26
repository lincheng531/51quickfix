# -*- encoding: utf-8 -*-
import copy
import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
BASEDIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(BASEDIR + '../../../..'))

from bson.objectid import ObjectId
from apps.base.utils import to_excel
from apps.base.models.store_schemas import *
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


def create_products():
    sheet = xlrd.open_workbook(BASEDIR + u'/10家餐厅固定资产记录-160921.xlsx')
    table = sheet.sheets()[5]
    nrows = table.nrows
    ncols = table.ncols

    product_field_map = {}
    no_brands = set()
    no_suppliers = set()

    for i in xrange(nrows):
        print 'row: ', i
        if i < 2:
            continue

        brand_name = table.cell(i, 6).value
        supplier_name = table.cell(i, 10).value
        brand = None
        supplier = None

        try:
            if brand_name:
                brand = Brand.objects.get(Q(name=brand_name) or Q(name2=brand_name))
        except:
            no_brands.add(brand_name)
            brand = Brand(**{
                'name': brand_name,
                'name2': brand_name,
            }).save()

        try:
            if supplier_name:
                supplier = Supplier.objects.get(Q(name=supplier_name) or Q(name2=supplier_name))
        except:
            no_suppliers.add(supplier_name)
            supplier = Supplier(**{
                'name': supplier_name,
                'name2': supplier_name,
            }).save()

        item = {
            'head_type': 4,
            'category': table.cell(i, 1).value.replace('类', ''),
            'efcategory': table.cell(i, 2).value,
            'ecategory': table.cell(i, 3).value,
            'name': table.cell(i, 4).value,
            'description': table.cell(i, 5).value,
            'brand_name': brand_name,
            'brand': brand,
            # initial             = StringField() #首字母
            'model': str(table.cell(i, 7).value),
            'specification': str(table.cell(i, 8).value),
            'supplier': supplier,
            'repair_time': int(table.cell(i, 12).value),
        }

        for k, v in item.iteritems():
            print k, v

        product = Product(**item).save()
        print product.id
        print

        Call(**{
            'head_type': 4,
            'city': '上海市',
            'product': product,
            'name': product.name,
            'brand': product.brand,
            'model': product.model,
            'specification': product.specification,
            'warranty_in': u'乐辛',
            'warranty_out1': u'乐辛',
        }).save()

    print 'no brands:'
    for item in no_brands:
        print item
    print
    print 'no suppliers:'
    for item in no_suppliers:
        print item


if __name__ == '__main__':
    #generate_rid()
    create_products()
    #TODO initial