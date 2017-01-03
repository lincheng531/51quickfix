# -*- encoding: utf-8 -*-
import copy
import os, sys

reload(sys)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.setdefaultencoding('utf-8')
BASEDIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(BASEDIR + '../../../..'))

from bson.objectid import ObjectId
from apps.base.utils import to_excel
from apps.base.models.base import Role, UserRole
from apps.base.models.store_schemas import *
from apps.base.models.schemas import *
import xlrd

HEAD_TYPE = 3


def create_store_user(data, store):
    item_template = {
        u'head_type': 3,
        u'password': u'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs=',
        u'source': store.brand,
        u'city': store.city,
        u'area': store.area,
        u'company': store.brand,
        u'is_staff': False,
        u'is_active': 1,
        u'is_superuser': 2,  # 注意替换
        u'is_update': False,
        u'create_time': dt.now(),
        u'date_joined': dt.now(),
    }
    pass

    if data.get('store_manager'):
        store_manager = copy.deepcopy(item_template)
        store_manager['name'] = data['store_manager']
        store_manager['screen_name'] = data['store_manager']
        store_manager['username'] = data['store_manager_mobile']
        store_manager['mobile'] = data['store_manager_mobile']
        if store.tel:
            store_manager['tel'] = [store.tel]
        store_manager['category'] = '1'  # 1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员，6：维修工区域经理

        store_manager['address'] = store.address
        store_manager['store_id'] = str(store.id)
        store_manager['store'] = store.name
        uid = User(**store_manager).save().id
        pass #print 'store manager:', uid
        #
        # if data.get('area_manager'):
        #     area_manager = copy.deepcopy(item_template)
        #     area_manager['name'] = data['area_manager']
        #     area_manager['screen_name'] = data['area_manager']
        #     area_manager['username'] = data['area_manager_mobile']
        #     area_manager['mobile'] = data['area_manager_mobile']
        #     area_manager['category'] = '3'  # 1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员，6：维修工区域经理
        #     try:
        #         pass #print 'area_manager:', User(**area_manager).save().id
        #     except:
        #         pass
        #
        # if data.get('oc'):
        #     oc = copy.deepcopy(item_template)
        #     oc['name'] = data['oc']
        #     oc['screen_name'] = data['oc']
        #     oc['username'] = data['oc_mobile']
        #     oc['mobile'] = data['oc_mobile']
        #     oc['category'] = '4'  # 1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员，6：维修工区域经理
        #     try:
        #         pass #print 'oc:', User(**oc).save().id
        #     except:
        #         pass


def create_sh_stores():
    sheet = xlrd.open_workbook(os.path.join(BASEDIR, u'dml_store_20161205.xlsx'))
    table = sheet.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    error_users = []

    for i in xrange(nrows):
        pass #print 'row: ', i + 1
        if i % 2 or i == 0:
            continue

        user_data = {}
        store = Store()
        store.head_type = 3
        store.brand = u'达美乐'
        store.city = u'上海市'
        store.area = u'华东区'

        if u'杭州' in table.cell(i, 0).value:
            continue

        for j in xrange(ncols):
            cell = table.cell(i, j)
            data = cell.value

            if data:
                pass #print j, data
            else:
                continue

            if j == 0:
                store.name = data.strip()
            if j == 1:
                store.no = str(int(data)).strip()
            if j == 2:
                store.opening_time = datetime.datetime(*xlrd.xldate.xldate_as_tuple(data, 0))
            if j == 5:
                try:
                    store.tel = str(int(data))
                except ValueError:
                    store.tel = data
            if j == 7:
                store.email = table.cell(i + 1, j).value or data
            if j == 8:
                store.address = data

            if j == 6:
                store.store_manager = data
                user_data['store_manager'] = data
                user_data['store_manager_mobile'] = str(int(table.cell(i + 1, j).value))

                # if field_map[j] == u'店经理':
                #     store.store_manager = data
                #     user_data['store_manager'] = data
                #
                # if field_map[j] == u'店经理手机':
                #     store.mobile = str(int(data))
                #     user_data['store_manager_mobile'] = str(int(data))

                # if field_map[j] == u'区域经理':
                #     user_data['area_manager'] = data
                # if field_map[j] == u'区域经理手机号':
                #     store.phone = str(int(data))
                #     user_data['area_manager_mobile'] = str(int(data))

                # if field_map[j] == u'OC（营运督导）':
                #     user_data['oc'] = data
                # if field_map[j] == u'OC 手机号':
                #     user_data['oc_mobile'] = str(int(data))

        if store.name in (u'汇融店', u'蓝村路店'):
            continue

        pass #print store.name,
        pass #print store.no,
        pass #print store.opening_time,
        pass #print store.tel,
        pass #print store.email,
        pass #print store.address

        store.save()
        user_data['store_id'] = str(store.id)
        user_data['store'] = store.name
        pass #print json.dumps(user_data, ensure_ascii=False)
        try:
            create_store_user(user_data, store)
        except Exception as e:
            user_data['error_msg'] = e
            error_users.append(user_data)
        pass #print
        pass #print

    pass #print 'error users:', len(error_users)
    for u in error_users:
        pass #print u


def create_bj_stores():
    table = sheet.sheets()[1]
    nrows = table.nrows
    ncols = table.ncols
    error_users = []

    for i in xrange(nrows):
        pass #print 'row: ', i + 1
        if i % 3 != 2:
            continue

        user_data = {}
        store = Store()
        store.head_type = 3
        store.brand = u'达美乐'
        store.city = u'北京市'
        store.area = u'华北区'

        for j in xrange(ncols):
            cell = table.cell(i, j)
            data = cell.value

            if data:
                pass #print j, data
            else:
                continue

            if j == 0:
                store.name = data
            if j == 1:
                store.no = str(int(data))
            if j == 2:
                store.opening_time = datetime.datetime(*xlrd.xldate.xldate_as_tuple(data, 0))
            if j == 4:
                try:
                    store.tel = str(int(data))
                except ValueError:
                    store.tel = data
            if j == 6:
                store.email = data
            if j == 7:
                store.address = data
            if j == 5:
                store.store_manager = data
                user_data['store_manager'] = data
                try:
                    user_data['store_manager_mobile'] = str(int(table.cell(i + 1, j).value))
                except:
                    user_data['store_manager_mobile'] = str((table.cell(i + 1, j).value).replace(' ', ''))

                    # if field_map[j] == u'店经理':
                    #     store.store_manager = data
                    #     user_data['store_manager'] = data
                    #
                    # if field_map[j] == u'店经理手机':
                    #     store.mobile = str(int(data))
                    #     user_data['store_manager_mobile'] = str(int(data))

                    # if field_map[j] == u'区域经理':
                    #     user_data['area_manager'] = data
                    # if field_map[j] == u'区域经理手机号':
                    #     store.phone = str(int(data))
                    #     user_data['area_manager_mobile'] = str(int(data))

                    # if field_map[j] == u'OC（营运督导）':
                    #     user_data['oc'] = data
                    # if field_map[j] == u'OC 手机号':
                    #     user_data['oc_mobile'] = str(int(data))

        if store.name in (u'汇融店', u'蓝村路店'):
            continue

        pass #print store.name,
        pass #print store.no,
        pass #print store.opening_time,
        pass #print store.tel,
        pass #print store.email,
        pass #print store.address

        store.save()
        user_data['store_id'] = str(store.id)
        user_data['store'] = store.name
        pass #print json.dumps(user_data, ensure_ascii=False)
        try:
            create_store_user(user_data, store)
        except Exception as e:
            user_data['error_msg'] = e
            error_users.append(user_data)
        pass #print
        pass #print

    pass #print 'error users:', len(error_users)
    for u in error_users:
        pass #print u


from collections import OrderedDict, defaultdict


def create_product():
    sheet = xlrd.open_workbook(os.path.join(BASEDIR, u'dml_products.xlsx'))
    meta_table = sheet.sheets()[1]
    nrows = meta_table.nrows
    ncols = meta_table.ncols
    store_dict = OrderedDict()
    error_brands = defaultdict(int)
    error_suppliers = defaultdict(int)

    for i in xrange(nrows):
        store_dict[meta_table.cell(i, 0).value] = meta_table.cell(i, 1).value

    for k, v in store_dict.iteritems():
        pass #print k, v

    for one_sheet in sheet.sheets():
        if one_sheet.name not in store_dict:
            continue

        table = one_sheet
        nrows = table.nrows
        ncols = table.ncols
        store_name = store_dict[one_sheet.name].strip()

        store = Store.objects.filter(head_type=HEAD_TYPE, name=store_name).first()
        if not store:
            if u'路' not in store_name:
                store_name = store_name.replace(u'店', u'路店')
                store = Store.objects.filter(head_type=HEAD_TYPE, name=store_name).first()
                if not store:
                    raise Exception('store error:' + store_name)
            else:
                if u'店' in store_name:
                    store_name = store_name.replace(u'店', '')
                    store = Store.objects.filter(head_type=HEAD_TYPE, name=store_name).first()
                    if not store:
                        store_name = store_name.replace(u'路', u'店')
                        store = Store.objects.filter(head_type=HEAD_TYPE, name=store_name).first()
                        if not store:
                            raise Exception('store error:' + store_name)
                else:
                    store_name = store_name + u'店'
                    store = Store.objects.filter(head_type=HEAD_TYPE, name=store_name).first()
                    if not store:
                        store_name = store_name.replace(u'路店', u'店')
                        store = Store.objects.filter(head_type=HEAD_TYPE, name=store_name).first()
                        if not store:
                            raise Exception('store error:' + store_name)

        pass #print '================>'
        pass #print table.name

        for i in xrange(nrows):
            pass #print '\nrow: ', i + 1

            if i < 5:
                continue

            # for j in xrange(ncols):
            #     cell = table.cell(i, j)
            #     data = cell.value
            #
            #     if data:
            #         pass #print j, data
            #     else:
            #         continue

            brand = None
            brand_name = table.cell(i, 8).value.strip()
            try:
                if u'品牌' in brand_name:
                    if table.name == '017':
                        continue
                if brand_name:
                    brand_name = brand_name.strip()
                    brand = Brand.objects.get(Q(name=brand_name) or Q(name2=brand_name))
            except Exception:
                error_brands[brand_name] += 1
                # raise Exception('error brand:' + brand_name)

            supplier = None
            supplier_name = str(table.cell(i, 1).value)
            if supplier_name:
                try:
                    supplier_name = supplier_name.strip()
                    supplier = Supplier.objects.get(Q(name=supplier_name) or Q(name2=supplier_name))
                except:
                    error_suppliers[supplier_name] += 1

            name = table.cell(i, 6).value.strip()
            if not name:
                continue

            item = {
                'head_type': HEAD_TYPE,
                # 'no': table.cell(i, 0).value.strip(),
                'category': table.cell(i, 2).value.strip(),
                'efcategory': table.cell(i, 3).value.strip(),
                'ecategory': table.cell(i, 4).value.strip(),
                'name': name,
                'description': table.cell(i, 7).value,
                'brand_name': (brand_name or '').strip(),
                'brand': brand,
                'model': str(table.cell(i, 9).value).replace('-', '').strip(),
                'specification': str(table.cell(i, 10).value).replace('-', '').strip(),
                # 'psnumber': str(table.cell(i, 11).value),
                # 'manufacturer': str(table.cell(i, 12).value),
                # 'installation_date': str(table.cell(i, 14).value),
                # 'provider': supplier_name,
                'supplier': supplier,
            }
            for k, v in item.iteritems():
                pass #print k, v

            filter_dict = {'name': item['name']}
            if item.get('category'):
                filter_dict['category'] = item['category']
            if item.get('efcategory'):
                filter_dict['efcategory'] = item['efcategory']
            if item.get('ecategory'):
                filter_dict['ecategory'] = item['ecategory']
            if item.get('brand_name'):
                filter_dict['brand_name'] = item['brand_name']
            if item.get('model') and item['model'] != '-':
                filter_dict['model'] = item['model']
            if item.get('specification') and item['specification'] != '-':
                filter_dict['specification'] = item['specification']

            products = Product.objects.filter(**filter_dict)
            if not products.count():
                product = Product(**item).save()
                Call(**{
                    'head_type': HEAD_TYPE,
                    'city': store.city,
                    'product': product,
                    'name': product.name,
                    'brand': product.brand,
                    'model': product.model,
                    'specification': product.specification,
                    'warranty_in': product.supplier and product.supplier.name,
                    'warranty_out1': product.supplier and product.supplier.name,
                }).save()
            else:
                product = products.first()

            device_item = {
                'head_type': HEAD_TYPE,
                'store': store,
                'no': table.cell(i, 0).value.strip(),
                'restaurant_name': store.name,
                'restaurant_no': store.no,
                'name': product.name,
                'area': store.area,
                'city': store.city,
                'description': product.description,
                'provider': supplier_name,
                'model': product.model,
                'category': product.category,
                'efcategory': product.efcategory,
                'ecategory': product.ecategory,
                'brand': product.brand and product.brand.name,
                'manufacturer': supplier_name,
                'specifications': product.specification,
                'scrap_time': table.cell(i, 21).value and str(int(table.cell(i, 21).value)).strip(),  # 注意修改
                'supplier': supplier,
                'product': product,
            }

            Device(**device_item).save()

    pass #print 'error_brands:', len(error_brands)
    pass #print json.dumps(error_brands, ensure_ascii=False)

    pass #print 'error_suppliers:', len(error_suppliers)
    pass #print json.dumps(error_suppliers, ensure_ascii=False)

def make_no(val):
    try:
        val = int(val)
    except ValueError:
        pass

    return str(val)

def create_spare():
    sheet = xlrd.open_workbook(os.path.join(BASEDIR, u'dml_spares.xlsx'))
    error_brands = defaultdict(int)
    error_products = defaultdict(int)
    error_products2 = defaultdict(int)

    for table in sheet.sheets()[:3]:
        nrows = table.nrows
        ncols = table.ncols

        pass #print '================>'
        pass #print table.name, nrows, ncols

        for i in xrange(nrows):
            if table.name == '果汁机':
                if i < 6: continue
            else:
                if i < 2: continue
            pass #print '\nrow: ', i + 1

            # for j in xrange(ncols):
            #     cell = table.cell(i, j)
            #     data = cell.value
            #
            #     if data:
            #         pass #print j, data
            #     else:
            #         continue

            brand = None
            brand_name = table.cell(i, 6).value.strip()
            try:
                if brand_name == 'CRATHCO':
                    brand_name = 'Crathco'
                brand = Brand.objects.get(Q(name=brand_name) or Q(name2=brand_name))
            except:
                error_brands[brand_name] += 1

            product_brand = table.cell(i, 1).value.strip()
            if product_brand == 'CRATHCO':
                product_brand = 'Crathco'

            product_brand = Brand.objects.get(Q(name=product_brand) or Q(name2=product_brand))
            product_name = table.cell(i, 2).value.strip()
            product_model = table.cell(i, 3).value.strip()
            product = None

            product = Product.objects.filter(head_type=HEAD_TYPE, name=product_name, model=product_model,
                                         brand=product_brand)
            if not product.count():
                error_products['{}-{}-{}-{}'.format(product_name, product_brand.name, product_model, product.count())] += 1

            product = product.first()

            # except:
            #     error_products['{}-{}-{}'.format(product_name, product_brand, product_model)] += 1
            #     try:
            #         product = Device.objects.get(head_type=HEAD_TYPE, name=product_name, model=product_model)
            #         import pdb;pdb.set_trace()
            #         product = None
            #     except:
            #         error_products2['{}-{}-{}'.format(product_name, product_brand, product_model)] += 1

            item = {
                'head_type': HEAD_TYPE,
                'no': make_no(table.cell(i, 4).value),
                'name': table.cell(i, 5).value.strip(),
                'brand_name': brand_name,
                'brand': brand,
                'price': table.cell(i, 7).value,
                'product_name': product_name,
                'product': product,
                'warranty1': 12,
                'warranty2': 12,
                'warranty3': 3,
            }

            for k, v in item.iteritems():
                pass #print k, v

            Spare(**item).save()

    pass #print 'error_brands:', len(error_brands)
    pass #print json.dumps(error_brands, ensure_ascii=False)

    pass #print 'error_products1:', len(error_products)
    pass #print json.dumps(error_products, ensure_ascii=False)

    pass #print 'error_products2:', len(error_products2)
    pass #print json.dumps(error_products2, ensure_ascii=False)


def init_brand():
    DB.brand.insert({
        "update_time": "2015-12-25T15:48:26.285Z",
        "name": "芙蓉",
        "initial": "F",
        "create_time": "2015-11-25T15:48:26.285Z",
        "name2": "芙蓉"
    })
    DB.brand.insert({
        "update_time": "2015-12-25T15:48:26.285Z",
        "name": "Delfield",
        "initial": "D",
        "create_time": "2015-11-25T15:48:26.285Z",
        "name2": "Delfield"
    })
    DB.brand.insert({
        "update_time": "2015-12-25T15:48:26.285Z",
        "name": "林肯",
        "initial": "L",
        "create_time": "2015-11-25T15:48:26.285Z",
        "name2": "林肯"
    })
    DB.brand.insert({
        "update_time": "2015-12-25T15:48:26.285Z",
        "name": "谷轮",
        "initial": "G",
        "create_time": "2015-11-25T15:48:26.285Z",
        "name2": "谷轮"
    })
    DB.brand.insert({
        "update_time": "2015-12-25T15:48:26.285Z",
        "name": "西门子",
        "initial": "X",
        "create_time": "2015-11-25T15:48:26.285Z",
        "name2": "西门子"
    })
    DB.brand.insert({
        "update_time": "2015-12-25T15:48:26.285Z",
        "name": "迪恩",
        "initial": "D",
        "create_time": "2015-11-25T15:48:26.285Z",
        "name2": "迪恩"
    })
    DB.brand.insert({
        "update_time": "2015-12-25T15:48:26.285Z",
        "name": "白雪",
        "initial": "B",
        "create_time": "2015-11-25T15:48:26.285Z",
        "name2": "白雪"
    })
    DB.brand.insert({
        "update_time": "2015-12-25T15:48:26.285Z",
        "name": "XLT",
        "initial": "X",
        "create_time": "2015-11-25T15:48:26.285Z",
        "name2": "XLT"
    })
    DB.brand.insert({
        "update_time": "2015-12-25T15:48:26.285Z",
        "name": "金城",
        "initial": "J",
        "create_time": "2015-11-25T15:48:26.285Z",
        "name2": "金城"
    })

    DB.supplier.insert({
        "update_time": "2015-12-25T15:48:26.388Z",
        "name": "大昌华嘉",
        "initial": "DCHJ",
        "create_time": "2015-12-25T15:48:26.388Z",
        "name2": "大昌华嘉"
    })
    DB.supplier.insert({
        "update_time": "2015-12-25T15:48:26.388Z",
        "name": "欣丰",
        "initial": "XF",
        "create_time": "2015-12-25T15:48:26.388Z",
        "name2": "欣丰"
    })
    DB.supplier.insert({
        "update_time": "2015-12-25T15:48:26.388Z",
        "name": "味纯",
        "initial": "WC",
        "create_time": "2015-12-25T15:48:26.388Z",
        "name2": "味纯"
    })

    DB.supplier.insert({
        "update_time": "2015-12-25T15:48:26.388Z",
        "name": "嘉侠",
        "initial": "JX",
        "create_time": "2015-12-25T15:48:26.388Z",
        "name2": "嘉侠"
    })


def show_products():
    query = Product.objects.filter(head_type=HEAD_TYPE).order_by("name")
    for item in query:
        pass #print '\n=======>'
        pass #print item.name
        pass #print item.efcategory
        pass #print item.ecategory
        pass #print item.brand_name
        pass #print item.model
        pass #print item.specification
        pass #print item.create_time

    pass #print 'total:', query.count()


if __name__ == '__main__':
    create_sh_stores()
    # create_bj_stores()
    init_brand()
    create_product()
    create_spare()

    show_products()