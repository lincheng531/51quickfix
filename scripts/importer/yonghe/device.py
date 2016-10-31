# -*- encoding: utf-8 -*-
import collections
import copy
import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
BASEDIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(BASEDIR + '../../../..'))

from bson.objectid import ObjectId
from apps.base.utils import to_excel
from apps.base.models.base import *
from apps.base.models.store_schemas import *
import xlrd


def generate_rid():
    sheet = xlrd.open_workbook(u'yonghe10-160921.xlsx')
    table = sheet.sheets()[2]
    nrows = table.nrows
    ncols = table.ncols

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
    sheet = xlrd.open_workbook(BASEDIR + u'/yonghe10-160921.xlsx')
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
            pass#pass#pass#pass#pass#pass#pass#pass#pass#print k, v

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


def create_devices():
    sheet = xlrd.open_workbook(BASEDIR + u'/yonghe10-160921.xlsx')
    table = sheet.sheets()[2]
    nrows = table.nrows
    ncols = table.ncols

    no_products = []

    for i in xrange(nrows):
        print 'row: ', i
        if i < 1:
            continue

        no = table.cell(i, 1).value
        if not no:
            continue

        category = table.cell(i, 4).value
        category = category.replace('类', '')
        store_no = table.cell(i, 0).value
        store = Store.objects(head_type=4, no=store_no).first()
        supplier = None
        supplier_name = table.cell(i, 3).value
        if supplier_name:
            supplier = Supplier.objects.get(Q(name=supplier_name) | Q(name2=supplier_name))

        item = {
            'head_type': 4,
            'store': store,
            'no': no,
            'restaurant_name': store.name,
            'restaurant_no': store.no,
            'name': table.cell(i, 7).value,
            'area': store.area,
            'city': store.city,
            'description': table.cell(i, 8).value,
            'price': str(table.cell(i, 14).value),
            'provider': u'乐辛',  # 注意修改,
            'model': str(table.cell(i, 10).value),
            'category': category,
            'efcategory': table.cell(i, 5).value,
            'ecategory': table.cell(i, 6).value,
            'brand': table.cell(i, 9).value,
            'manufacturer': table.cell(i, 13).value,
            'specifications': str(table.cell(i, 11).value),
            'scrap_time': u'5年',  # 注意修改
            'supplier': supplier,
        }

        product = None
        products = Product.objects.filter(name=item['name'], head_type=4, category=item['category'], efcategory=item['efcategory'],
                                         ecategory=item['ecategory'], specification=item['specifications'])

        if products.count() < 1:
            no_products.append(item)
        else:
            product = products.first()

        item['product'] = product
        print Device(**item).save().id
        for k, v in item.iteritems():
            pass#pass#pass#pass#pass#pass#pass#pass#print k, v
        print

    print 'error products count: ', len(no_products)
    pass


def create_spares():
    sheet = xlrd.open_workbook(BASEDIR + u'/yonghe10-160921.xlsx')
    table = sheet.sheets()[3]
    nrows = table.nrows
    ncols = table.ncols

    brand_error = set()
    product_error = set()
    product_error_count = collections.defaultdict(int)

    for i in xrange(nrows):
        print 'row: ', i
        if i < 2:
            continue

        brand = None
        brand_name = name=table.cell(i, 1).value
        if brand_name == '南方厨具':
            brand_name = '南厨'
        try:
            brand = Brand.objects.get(name=brand_name)
        except:
            brand_error.add(brand_name)
            brand = Brand(**{
                'name': brand_name,
                'name2': brand_name,
            }).save()

        item = {
            'head_type': 4,
            'no': table.cell(i, 6).value,
            'name': table.cell(i, 7).value,
            'product_name': table.cell(i, 3).value,
            'brand': brand,
            'brand_name': table.cell(i, 8).value,
            'content': table.cell(i, 10).value,
            'model': table.cell(i, 9).value,
            'price': table.cell(i, 11).value,
            'warranty1': int(table.cell(i, 12).value or 0),
            'warranty2': int(table.cell(i, 13).value or 0),
            'warranty3': int(table.cell(i, 14).value or 0),
        }

        product_names = item['product_name']
        if '，' in product_names:
            namelist = product_names.split('，')
        else:
            namelist = [product_names]

        for product_name in namelist:
            products = Product.objects.filter(name=product_name, ecategory=table.cell(i, 2).value, brand_name=brand_name)
            if not products.count():
                if product_name == u'磨煮一体机，磨浆机':
                    product_name = u'磨煮一体机'
                products = Product.objects.filter(name=product_name, brand_name=brand_name)
                if not products.count():
                    products = Product.objects.filter(name=product_name)
                    if not products.count():
                        key = '{}-{}-{}'.format(item['product_name'], table.cell(i, 2).value, brand_name)
                        product_error.add(key)
                        product_error_count[key] += 1

            for product in products:
                item['product'] = product
                print Spare(**item).save().id

        for k, v in item.iteritems():
            pass#pass#pass#pass#pass#pass#pass#pass#print k, v

        print

    print 'no products========>'
    for item in product_error:
        print item, product_error_count[item]
        print
    print 'no brand ==========>'
    for item in brand_error:
        print item


def create_errorcodes():
    sheet = xlrd.open_workbook(BASEDIR + u'/yonghe10-160921.xlsx')
    table = sheet.sheets()[4]
    nrows = table.nrows
    ncols = table.ncols
    product_error_count = collections.defaultdict(int)

    for i in xrange(nrows):
        print 'row: ', i
        if i < 1:
            continue

        item = {
            'head_type': 4,
            'error': table.cell(i, 7).value.strip(),
            'phen': table.cell(i, 9).value.strip(),
            'measure': table.cell(i, 10).value.strip(),
            'method': table.cell(i, 11).value.strip(),
            'status': 2,
        }

        brand_name = table.cell(i, 2).value
        product_ecat = table.cell(i, 3).value
        product_name = table.cell(i, 4).value

        products = Product.objects.filter(name=product_name, ecategory=product_ecat, brand_name=brand_name)
        if not products.count():
            products = Product.objects.filter(name=product_name, ecategory=product_ecat)
            if not products.count():
                key = '{}->{}->{}'.format(product_name, product_ecat, brand_name)
                product_error_count[key] += 1

        for product in products:
            item['product'] = product
            print ErrorCode(**item).save().id

        for k, v in item.iteritems():
            pass#pass#pass#pass#pass#pass#pass#pass#pass#print k, v
        print

    print 'no products========>'
    for k, v in product_error_count.iteritems():
        pass#pass#pass#pass#pass#pass#pass#pass#print k, v


if __name__ == '__main__':
    # generate_rid()
    create_products()
    create_devices()
    create_spares()
    create_errorcodes()
    # TODO brand, supplier, product, device initial, device product重合
