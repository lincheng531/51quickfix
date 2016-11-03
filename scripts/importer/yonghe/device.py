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
        pass#print item
    print
    print 'no suppliers:'
    for item in no_suppliers:
        pass#print item


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
        pass#print item, product_error_count[item]
        print
    print 'no brand ==========>'
    for item in brand_error:
        pass#print item


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


def relate_device_rid():
    Device.objects(head_type=4, no='SH031X001005').update(set__rid='57eb353c52d8ff5ee9ef743a')
    Device.objects(head_type=4, no='SH031X001010').update(set__rid='57eb353c52d8ff5ee9ef743b')
    Device.objects(head_type=4, no='SH031X001011').update(set__rid='57eb353c52d8ff5ee9ef743c')
    Device.objects(head_type=4, no='SH031X001012').update(set__rid='57eb353c52d8ff5ee9ef743d')
    Device.objects(head_type=4, no='SH031X001013').update(set__rid='57eb353c52d8ff5ee9ef743e')
    Device.objects(head_type=4, no='SH031X001018').update(set__rid='57eb353c52d8ff5ee9ef743f')
    Device.objects(head_type=4, no='SH031X001017').update(set__rid='57eb353c52d8ff5ee9ef7440')
    Device.objects(head_type=4, no='SH031X001002').update(set__rid='57eb353c52d8ff5ee9ef7441')
    Device.objects(head_type=4, no='SH031X004001').update(set__rid='57eb353c52d8ff5ee9ef7442')
    Device.objects(head_type=4, no='SH031X001006').update(set__rid='57eb353c52d8ff5ee9ef7443')
    Device.objects(head_type=4, no='SH031X001014').update(set__rid='57eb353c52d8ff5ee9ef7444')
    Device.objects(head_type=4, no='SH031X001015').update(set__rid='57eb353c52d8ff5ee9ef7445')
    Device.objects(head_type=4, no='SH031X001009').update(set__rid='57eb353c52d8ff5ee9ef7446')
    Device.objects(head_type=4, no='SH031X001016').update(set__rid='57eb353c52d8ff5ee9ef7447')
    Device.objects(head_type=4, no='SH031X001007').update(set__rid='57eb353c52d8ff5ee9ef7448')
    Device.objects(head_type=4, no='SH031X001008').update(set__rid='57eb353c52d8ff5ee9ef7449')
    Device.objects(head_type=4, no='SH031X001004').update(set__rid='57eb353c52d8ff5ee9ef744a')
    Device.objects(head_type=4, no='SH031X001013').update(set__rid='57eb353c52d8ff5ee9ef744b')
    Device.objects(head_type=4, no='SH031X001001').update(set__rid='57eb353c52d8ff5ee9ef744c')
    Device.objects(head_type=4, no='SH031X001003').update(set__rid='57eb353c52d8ff5ee9ef744d')
    Device.objects(head_type=4, no='SH046X001011').update(set__rid='57eb353c52d8ff5ee9ef744f')
    Device.objects(head_type=4, no='SH046X001012').update(set__rid='57eb353c52d8ff5ee9ef7450')
    Device.objects(head_type=4, no='SH046X001017').update(set__rid='57eb353c52d8ff5ee9ef7451')
    Device.objects(head_type=4, no='SH046X001022').update(set__rid='57eb353c52d8ff5ee9ef7452')
    Device.objects(head_type=4, no='SH046X001026').update(set__rid='57eb353c52d8ff5ee9ef7453')
    Device.objects(head_type=4, no='SH046X001027').update(set__rid='57eb353c52d8ff5ee9ef7454')
    Device.objects(head_type=4, no='SH046X004001').update(set__rid='57eb353c52d8ff5ee9ef7455')
    Device.objects(head_type=4, no='SH046X001013').update(set__rid='57eb353c52d8ff5ee9ef7456')
    Device.objects(head_type=4, no='SH046X001010').update(set__rid='57eb353c52d8ff5ee9ef7457')
    Device.objects(head_type=4, no='SH046X001016').update(set__rid='57eb353c52d8ff5ee9ef7458')
    Device.objects(head_type=4, no='SH046X001014').update(set__rid='57eb353c52d8ff5ee9ef7459')
    Device.objects(head_type=4, no='SH046X001001').update(set__rid='57eb353c52d8ff5ee9ef745a')
    Device.objects(head_type=4, no='SH046X001002').update(set__rid='57eb353c52d8ff5ee9ef745b')
    Device.objects(head_type=4, no='SH046X001009').update(set__rid='57eb353c52d8ff5ee9ef745c')
    Device.objects(head_type=4, no='SH046X001003').update(set__rid='57eb353c52d8ff5ee9ef745d')
    Device.objects(head_type=4, no='SH048X001016').update(set__rid='57eb353c52d8ff5ee9ef745f')
    Device.objects(head_type=4, no='SH048X001017').update(set__rid='57eb353c52d8ff5ee9ef7460')
    Device.objects(head_type=4, no='SH048X001021').update(set__rid='57eb353c52d8ff5ee9ef7461')
    Device.objects(head_type=4, no='SH048X001001').update(set__rid='57eb353c52d8ff5ee9ef7462')
    Device.objects(head_type=4, no='SH048X001002').update(set__rid='57eb353c52d8ff5ee9ef7463')
    Device.objects(head_type=4, no='SH048X001007').update(set__rid='57eb353c52d8ff5ee9ef7464')
    Device.objects(head_type=4, no='SH048X004001').update(set__rid='57eb353c52d8ff5ee9ef7465')
    Device.objects(head_type=4, no='SH048X001008').update(set__rid='57eb353c52d8ff5ee9ef7466')
    Device.objects(head_type=4, no='SH048X001018').update(set__rid='57eb353c52d8ff5ee9ef7467')
    Device.objects(head_type=4, no='SH048X001011').update(set__rid='57eb353c52d8ff5ee9ef7468')
    Device.objects(head_type=4, no='SH048X001022').update(set__rid='57eb353c52d8ff5ee9ef7469')
    Device.objects(head_type=4, no='SH048X001004').update(set__rid='57eb353c52d8ff5ee9ef746a')
    Device.objects(head_type=4, no='SH048X001005').update(set__rid='57eb353c52d8ff5ee9ef746b')
    Device.objects(head_type=4, no='SH048X001010').update(set__rid='57eb353c52d8ff5ee9ef746c')
    Device.objects(head_type=4, no='SH048X001003').update(set__rid='57eb353c52d8ff5ee9ef746d')
    Device.objects(head_type=4, no='SH048X001009').update(set__rid='57eb353c52d8ff5ee9ef746e')
    Device.objects(head_type=4, no='SH048X001006').update(set__rid='57eb353c52d8ff5ee9ef746f')
    Device.objects(head_type=4, no='SH052X001012').update(set__rid='57eb353c52d8ff5ee9ef7471')
    Device.objects(head_type=4, no='SH052X001017').update(set__rid='57eb353c52d8ff5ee9ef7472')
    Device.objects(head_type=4, no='SH052X001019').update(set__rid='57eb353c52d8ff5ee9ef7473')
    Device.objects(head_type=4, no='SH052X001020').update(set__rid='57eb353c52d8ff5ee9ef7474')
    Device.objects(head_type=4, no='SH052X001022').update(set__rid='57eb353c52d8ff5ee9ef7475')
    Device.objects(head_type=4, no='SH052X001023').update(set__rid='57eb353c52d8ff5ee9ef7476')
    Device.objects(head_type=4, no='SH052X001029').update(set__rid='57eb353c52d8ff5ee9ef7477')
    Device.objects(head_type=4, no='SH052X001007').update(set__rid='57eb353c52d8ff5ee9ef7478')
    Device.objects(head_type=4, no='SH052X001008').update(set__rid='57eb353c52d8ff5ee9ef7479')
    Device.objects(head_type=4, no='SH052X004001').update(set__rid='57eb353c52d8ff5ee9ef747a')
    Device.objects(head_type=4, no='SH052X001009').update(set__rid='57eb353c52d8ff5ee9ef747b')
    Device.objects(head_type=4, no='SH052X001001').update(set__rid='57eb353c52d8ff5ee9ef747c')
    Device.objects(head_type=4, no='SH052X001021').update(set__rid='57eb353c52d8ff5ee9ef747d')
    Device.objects(head_type=4, no='SH052X001028').update(set__rid='57eb353c52d8ff5ee9ef747e')
    Device.objects(head_type=4, no='SH052X001011').update(set__rid='57eb353c52d8ff5ee9ef747f')
    Device.objects(head_type=4, no='SH052X001003').update(set__rid='57eb353c52d8ff5ee9ef7480')
    Device.objects(head_type=4, no='SH052X001005').update(set__rid='57eb353c52d8ff5ee9ef7481')
    Device.objects(head_type=4, no='SH052X001006').update(set__rid='57eb353c52d8ff5ee9ef7482')
    Device.objects(head_type=4, no='SH052X001010').update(set__rid='57eb353c52d8ff5ee9ef7483')
    Device.objects(head_type=4, no='SH052X001002').update(set__rid='57eb353c52d8ff5ee9ef7484')
    Device.objects(head_type=4, no='SH052X001004').update(set__rid='57eb353c52d8ff5ee9ef7485')
    Device.objects(head_type=4, no='SH055X001012').update(set__rid='57eb353c52d8ff5ee9ef7487')
    Device.objects(head_type=4, no='SH055X001013').update(set__rid='57eb353c52d8ff5ee9ef7488')
    Device.objects(head_type=4, no='SH055X001014').update(set__rid='57eb353c52d8ff5ee9ef7489')
    Device.objects(head_type=4, no='SH055X001028').update(set__rid='57eb353c52d8ff5ee9ef748a')
    Device.objects(head_type=4, no='SH055X001029').update(set__rid='57eb353c52d8ff5ee9ef748b')
    Device.objects(head_type=4, no='SH055X001002').update(set__rid='57eb353c52d8ff5ee9ef748c')
    Device.objects(head_type=4, no='SH055X001003').update(set__rid='57eb353c52d8ff5ee9ef748d')
    Device.objects(head_type=4, no='SH055X001008').update(set__rid='57eb353c52d8ff5ee9ef748e')
    Device.objects(head_type=4, no='SH055X001011').update(set__rid='57eb353c52d8ff5ee9ef748f')
    Device.objects(head_type=4, no='SH055X004001').update(set__rid='57eb353c52d8ff5ee9ef7490')
    Device.objects(head_type=4, no='SH055X001015').update(set__rid='57eb353c52d8ff5ee9ef7491')
    Device.objects(head_type=4, no='SH055X001007').update(set__rid='57eb353c52d8ff5ee9ef7492')
    Device.objects(head_type=4, no='SH055X001022').update(set__rid='57eb353c52d8ff5ee9ef7493')
    Device.objects(head_type=4, no='SH055X001023').update(set__rid='57eb353c52d8ff5ee9ef7494')
    Device.objects(head_type=4, no='SH055X001017').update(set__rid='57eb353c52d8ff5ee9ef7495')
    Device.objects(head_type=4, no='SH055X001005').update(set__rid='57eb353c52d8ff5ee9ef7496')
    Device.objects(head_type=4, no='SH055X001006').update(set__rid='57eb353c52d8ff5ee9ef7497')
    Device.objects(head_type=4, no='SH055X001016').update(set__rid='57eb353c52d8ff5ee9ef7498')
    Device.objects(head_type=4, no='SH055X001004').update(set__rid='57eb353c52d8ff5ee9ef7499')
    Device.objects(head_type=4, no='SH055X001010').update(set__rid='57eb353c52d8ff5ee9ef749a')
    Device.objects(head_type=4, no='SH055X001009').update(set__rid='57eb353c52d8ff5ee9ef749b')
    Device.objects(head_type=4, no='SH055X001001').update(set__rid='57eb353c52d8ff5ee9ef749c')
    Device.objects(head_type=4, no='SH059X001012').update(set__rid='57eb353c52d8ff5ee9ef749e')
    Device.objects(head_type=4, no='SH059X001001').update(set__rid='57eb353c52d8ff5ee9ef749f')
    Device.objects(head_type=4, no='SH059X001024').update(set__rid='57eb353c52d8ff5ee9ef74a0')
    Device.objects(head_type=4, no='SH059X001027').update(set__rid='57eb353c52d8ff5ee9ef74a1')
    Device.objects(head_type=4, no='SH059X001029').update(set__rid='57eb353c52d8ff5ee9ef74a2')
    Device.objects(head_type=4, no='SH059X001005').update(set__rid='57eb353c52d8ff5ee9ef74a3')
    Device.objects(head_type=4, no='SH059X001006').update(set__rid='57eb353c52d8ff5ee9ef74a4')
    Device.objects(head_type=4, no='SH059X001011').update(set__rid='57eb353c52d8ff5ee9ef74a5')
    Device.objects(head_type=4, no='SH059X001003').update(set__rid='57eb353c52d8ff5ee9ef74a6')
    Device.objects(head_type=4, no='SH059X004001').update(set__rid='57eb353c52d8ff5ee9ef74a7')
    Device.objects(head_type=4, no='SH059X001010').update(set__rid='57eb353c52d8ff5ee9ef74a8')
    Device.objects(head_type=4, no='SH059X001026').update(set__rid='57eb353c52d8ff5ee9ef74a9')
    Device.objects(head_type=4, no='SH059X001028').update(set__rid='57eb353c52d8ff5ee9ef74aa')
    Device.objects(head_type=4, no='SH059X001014').update(set__rid='57eb353c52d8ff5ee9ef74ab')
    Device.objects(head_type=4, no='SH059X001015').update(set__rid='57eb353c52d8ff5ee9ef74ac')
    Device.objects(head_type=4, no='SH059X001008').update(set__rid='57eb353c52d8ff5ee9ef74ad')
    Device.objects(head_type=4, no='SH059X001009').update(set__rid='57eb353c52d8ff5ee9ef74ae')
    Device.objects(head_type=4, no='SH059X001013').update(set__rid='57eb353c52d8ff5ee9ef74af')
    Device.objects(head_type=4, no='SH059X001030').update(set__rid='57eb353c52d8ff5ee9ef74b0')
    Device.objects(head_type=4, no='SH059X001007').update(set__rid='57eb353c52d8ff5ee9ef74b1')
    Device.objects(head_type=4, no='SH059X001002').update(set__rid='57eb353c52d8ff5ee9ef74b2')
    Device.objects(head_type=4, no='SH059X001004').update(set__rid='57eb353c52d8ff5ee9ef74b3')
    Device.objects(head_type=4, no='SH074X001017').update(set__rid='57eb353c52d8ff5ee9ef74b5')
    Device.objects(head_type=4, no='SH074X001001').update(set__rid='57eb353c52d8ff5ee9ef74b6')
    Device.objects(head_type=4, no='SH074X001019').update(set__rid='57eb353c52d8ff5ee9ef74b7')
    Device.objects(head_type=4, no='SH074X001020').update(set__rid='57eb353c52d8ff5ee9ef74b8')
    Device.objects(head_type=4, no='SH074X001021').update(set__rid='57eb353c52d8ff5ee9ef74b9')
    Device.objects(head_type=4, no='SH074X001003').update(set__rid='57eb353c52d8ff5ee9ef74ba')
    Device.objects(head_type=4, no='SH074X001004').update(set__rid='57eb353c52d8ff5ee9ef74bb')
    Device.objects(head_type=4, no='SH074X001016').update(set__rid='57eb353c52d8ff5ee9ef74bc')
    Device.objects(head_type=4, no='SH074X004001').update(set__rid='57eb353c52d8ff5ee9ef74bd')
    Device.objects(head_type=4, no='SH074X001005').update(set__rid='57eb353c52d8ff5ee9ef74be')
    Device.objects(head_type=4, no='SH074X001015').update(set__rid='57eb353c52d8ff5ee9ef74bf')
    Device.objects(head_type=4, no='SH074X001014').update(set__rid='57eb353c52d8ff5ee9ef74c0')
    Device.objects(head_type=4, no='SH074X001018').update(set__rid='57eb353c52d8ff5ee9ef74c1')
    Device.objects(head_type=4, no='SH074X001012').update(set__rid='57eb353c52d8ff5ee9ef74c2')
    Device.objects(head_type=4, no='SH074X001006').update(set__rid='57eb353c52d8ff5ee9ef74c3')
    Device.objects(head_type=4, no='SH074X001007').update(set__rid='57eb353c52d8ff5ee9ef74c4')
    Device.objects(head_type=4, no='SH074X001010').update(set__rid='57eb353c52d8ff5ee9ef74c5')
    Device.objects(head_type=4, no='SH074X001011').update(set__rid='57eb353c52d8ff5ee9ef74c6')
    Device.objects(head_type=4, no='SH074X001002').update(set__rid='57eb353c52d8ff5ee9ef74c7')
    Device.objects(head_type=4, no='SH074X001013').update(set__rid='57eb353c52d8ff5ee9ef74c8')
    Device.objects(head_type=4, no='SH074X001008').update(set__rid='57eb353c52d8ff5ee9ef74c9')
    Device.objects(head_type=4, no='SH074X001009').update(set__rid='57eb353c52d8ff5ee9ef74ca')
    Device.objects(head_type=4, no='SH077X001014').update(set__rid='57eb353c52d8ff5ee9ef74cc')
    Device.objects(head_type=4, no='SH077X001004').update(set__rid='57eb353c52d8ff5ee9ef74cd')
    Device.objects(head_type=4, no='SH077X001015').update(set__rid='57eb353c52d8ff5ee9ef74ce')
    Device.objects(head_type=4, no='SH077X001016').update(set__rid='57eb353c52d8ff5ee9ef74cf')
    Device.objects(head_type=4, no='SH077X001022').update(set__rid='57eb353c52d8ff5ee9ef74d0')
    Device.objects(head_type=4, no='SH077X001005').update(set__rid='57eb353c52d8ff5ee9ef74d1')
    Device.objects(head_type=4, no='SH077X001006').update(set__rid='57eb353c52d8ff5ee9ef74d2')
    Device.objects(head_type=4, no='SH077X001013').update(set__rid='57eb353c52d8ff5ee9ef74d3')
    Device.objects(head_type=4, no='SH077X004001').update(set__rid='57eb353c52d8ff5ee9ef74d4')
    Device.objects(head_type=4, no='SH077X004002').update(set__rid='57eb353c52d8ff5ee9ef74d5')
    Device.objects(head_type=4, no='SH077X001007').update(set__rid='57eb353c52d8ff5ee9ef74d6')
    Device.objects(head_type=4, no='SH077X001021').update(set__rid='57eb353c52d8ff5ee9ef74d7')
    Device.objects(head_type=4, no='SH077X001020').update(set__rid='57eb353c52d8ff5ee9ef74d8')
    Device.objects(head_type=4, no='SH077X001012').update(set__rid='57eb353c52d8ff5ee9ef74d9')
    Device.objects(head_type=4, no='SH077X001008').update(set__rid='57eb353c52d8ff5ee9ef74da')
    Device.objects(head_type=4, no='SH077X001009').update(set__rid='57eb353c52d8ff5ee9ef74db')
    Device.objects(head_type=4, no='SH077X001017').update(set__rid='57eb353c52d8ff5ee9ef74dc')
    Device.objects(head_type=4, no='SH077X001018').update(set__rid='57eb353c52d8ff5ee9ef74dd')
    Device.objects(head_type=4, no='SH077X001001').update(set__rid='57eb353c52d8ff5ee9ef74de')
    Device.objects(head_type=4, no='SH077X001002').update(set__rid='57eb353c52d8ff5ee9ef74df')
    Device.objects(head_type=4, no='SH077X001003').update(set__rid='57eb353c52d8ff5ee9ef74e0')
    Device.objects(head_type=4, no='SH077X001019').update(set__rid='57eb353c52d8ff5ee9ef74e1')
    Device.objects(head_type=4, no='SH077X001010').update(set__rid='57eb353c52d8ff5ee9ef74e2')
    Device.objects(head_type=4, no='SH077X001011').update(set__rid='57eb353c52d8ff5ee9ef74e3')
    Device.objects(head_type=4, no='SH079X001016').update(set__rid='57eb353c52d8ff5ee9ef74e5')
    Device.objects(head_type=4, no='SH079X001006').update(set__rid='57eb353c52d8ff5ee9ef74e6')
    Device.objects(head_type=4, no='SH079X001017').update(set__rid='57eb353c52d8ff5ee9ef74e7')
    Device.objects(head_type=4, no='SH079X001018').update(set__rid='57eb353c52d8ff5ee9ef74e8')
    Device.objects(head_type=4, no='SH079X001023').update(set__rid='57eb353c52d8ff5ee9ef74e9')
    Device.objects(head_type=4, no='SH079X001024').update(set__rid='57eb353c52d8ff5ee9ef74ea')
    Device.objects(head_type=4, no='SH079X001007').update(set__rid='57eb353c52d8ff5ee9ef74eb')
    Device.objects(head_type=4, no='SH079X001008').update(set__rid='57eb353c52d8ff5ee9ef74ec')
    Device.objects(head_type=4, no='SH079X001013').update(set__rid='57eb353c52d8ff5ee9ef74ed')
    Device.objects(head_type=4, no='SH079X001015').update(set__rid='57eb353c52d8ff5ee9ef74ee')
    Device.objects(head_type=4, no='SH079X004001').update(set__rid='57eb353c52d8ff5ee9ef74ef')
    Device.objects(head_type=4, no='SH079X001009').update(set__rid='57eb353c52d8ff5ee9ef74f0')
    Device.objects(head_type=4, no='SH079X001022').update(set__rid='57eb353c52d8ff5ee9ef74f1')
    Device.objects(head_type=4, no='SH079X001021').update(set__rid='57eb353c52d8ff5ee9ef74f2')
    Device.objects(head_type=4, no='SH079X001001').update(set__rid='57eb353c52d8ff5ee9ef74f3')
    Device.objects(head_type=4, no='SH079X001010').update(set__rid='57eb353c52d8ff5ee9ef74f4')
    Device.objects(head_type=4, no='SH079X001019').update(set__rid='57eb353c52d8ff5ee9ef74f5')
    Device.objects(head_type=4, no='SH079X001029').update(set__rid='57eb353c52d8ff5ee9ef74f6')
    Device.objects(head_type=4, no='SH079X001014').update(set__rid='57eb353c52d8ff5ee9ef74f7')
    Device.objects(head_type=4, no='SH079X001020').update(set__rid='57eb353c52d8ff5ee9ef74f8')
    Device.objects(head_type=4, no='SH079X001011').update(set__rid='57eb353c52d8ff5ee9ef74f9')
    Device.objects(head_type=4, no='SH079X001012').update(set__rid='57eb353c52d8ff5ee9ef74fa')
    Device.objects(head_type=4, no='SH092X001001').update(set__rid='57eb353c52d8ff5ee9ef74fc')
    Device.objects(head_type=4, no='SH092X001002').update(set__rid='57eb353c52d8ff5ee9ef74fd')
    Device.objects(head_type=4, no='SH092X001003').update(set__rid='57eb353c52d8ff5ee9ef74fe')
    Device.objects(head_type=4, no='SH092X001004').update(set__rid='57eb353c52d8ff5ee9ef74ff')
    Device.objects(head_type=4, no='SH092X001005').update(set__rid='57eb353c52d8ff5ee9ef7500')
    Device.objects(head_type=4, no='SH092X001006').update(set__rid='57eb353c52d8ff5ee9ef7501')
    Device.objects(head_type=4, no='SH092X001007').update(set__rid='57eb353c52d8ff5ee9ef7502')
    Device.objects(head_type=4, no='SH092X001008').update(set__rid='57eb353c52d8ff5ee9ef7503')
    Device.objects(head_type=4, no='SH092X001009').update(set__rid='57eb353c52d8ff5ee9ef7504')
    Device.objects(head_type=4, no='SH092X001010').update(set__rid='57eb353c52d8ff5ee9ef7505')
    Device.objects(head_type=4, no='SH092X001011').update(set__rid='57eb353c52d8ff5ee9ef7506')
    Device.objects(head_type=4, no='SH092X001012').update(set__rid='57eb353c52d8ff5ee9ef7507')
    Device.objects(head_type=4, no='SH092X001013').update(set__rid='57eb353c52d8ff5ee9ef7508')
    Device.objects(head_type=4, no='SH092X001014').update(set__rid='57eb353c52d8ff5ee9ef7509')
    Device.objects(head_type=4, no='SH092X001015').update(set__rid='57eb353c52d8ff5ee9ef750a')
    Device.objects(head_type=4, no='SH092X001022').update(set__rid='57eb353c52d8ff5ee9ef750b')
    Device.objects(head_type=4, no='SH092X001023').update(set__rid='57eb353c52d8ff5ee9ef750c')
    Device.objects(head_type=4, no='SH092X001024').update(set__rid='57eb353c52d8ff5ee9ef750d')
    Device.objects(head_type=4, no='SH092X001025').update(set__rid='57eb353c52d8ff5ee9ef750e')
    Device.objects(head_type=4, no='SH092X004001').update(set__rid='57eb353c52d8ff5ee9ef750f')
    Device.objects(head_type=4, no='SH092X001026').update(set__rid='57eb353c52d8ff5ee9ef7510')
    Device.objects(head_type=4, no='SH092X001027').update(set__rid='57eb353c52d8ff5ee9ef7511')
    Device.objects(head_type=4, no='SH092X001028').update(set__rid='57eb353c52d8ff5ee9ef7512')


if __name__ == '__main__':
    # generate_rid()
    #create_products()
    #create_devices()
    #create_spares()
    create_errorcodes()
    #relate_device_rid()
    # TODO brand, supplier, product, device initial, device product重合