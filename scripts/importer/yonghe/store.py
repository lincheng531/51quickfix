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
from apps.base.models.store_schemas import *
from apps.base.models.schemas import *
import xlrd

sheet = xlrd.open_workbook(os.path.join(BASEDIR, u'yonghe10-160921.xlsx'))
table = sheet.sheets()[0]
nrows = table.nrows
ncols = table.ncols


def generate_rid():
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


field_map = {}


def create_stores():
    for i in xrange(nrows):
        print 'row: ', i
        if i == 0:
            continue

        user_data = {}
        store = Store()
        store.head_type = 4
        store.brand = u'永和大王'

        for j in xrange(ncols):
            cell = table.cell(i, j)
            data = cell.value

            if i == 1:
                field_map[j] = data
                continue

            if data:
                print j#, data
            else:
                continue

            if field_map[j] == u'地区':
                store.area = data + u'区'
            if field_map[j] == u'城市':
                store.city = data + u'市'
            if field_map[j] == u'餐厅编号':
                store.no = data
            if field_map[j] == u'餐厅名称':
                store.name = data
                if not store.name.endswith(u'店'):
                    store.name += u'店'
            if field_map[j] == u'开业日期':
                store.opening_time = datetime.datetime(*xlrd.xldate.xldate_as_tuple(data, 0))
            if field_map[j] == u'餐厅电话':
                store.tel = str(int(data))
            if field_map[j] == u'营业时间':
                store.business_hours = data
            if field_map[j] == u'详细地址':
                store.address = data
            if field_map[j] == u'邮箱':
                store.email = data
            if field_map[j] == u'店经理':
                store.store_manager = data
                user_data['store_manager'] = data
            if field_map[j] == u'直营/加盟':
                store.business_type = data
            if field_map[j] == u'所属公司':
                store.company = data

            if field_map[j] == u'店经理手机':
                store.mobile = str(int(data))
                user_data['store_manager_mobile'] = str(int(data))
            if field_map[j] == u'区域经理':
                user_data['area_manager'] = data
            if field_map[j] == u'区域经理手机号':
                store.phone = str(int(data))
                user_data['area_manager_mobile'] = str(int(data))
            if field_map[j] == u'OC（营运督导）':
                user_data['oc'] = data
            if field_map[j] == u'OC 手机号':
                user_data['oc_mobile'] = str(int(data))

        if i > 1:
            store.save()
            user_data['store_id'] = str(store.id)
            user_data['store'] = store.name
            print 'id: ', store.id

        print user_data
        create_store_user(user_data, store)
        print
        print

    # for k, v in field_map.iteritems():
    #     print k, v


def create_store_user(data, store):
    item_template = {
        u'head_type': 4,
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

    if data.get('store_manager'):
        store_manager = copy.deepcopy(item_template)
        store_manager['name'] = data['store_manager']
        store_manager['screen_name'] = data['store_manager']
        store_manager['username'] = data['store_manager_mobile']
        store_manager['mobile'] = data['store_manager_mobile']
        store_manager['tel'] = [store.tel]
        store_manager['category'] = '1'  # 1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员，6：维修工区域经理

        store_manager['address'] = store.address
        store_manager['store_id'] = str(store.id)
        store_manager['store'] = store.name
        print 'store manager:', User(**store_manager).save().id

    if data.get('area_manager'):
        area_manager = copy.deepcopy(item_template)
        area_manager['name'] = data['area_manager']
        area_manager['screen_name'] = data['area_manager']
        area_manager['username'] = data['area_manager_mobile']
        area_manager['mobile'] = data['area_manager_mobile']
        area_manager['category'] = '3'  # 1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员，6：维修工区域经理
        try:
            print 'area_manager:', User(**area_manager).save().id
        except:
            pass

    if data.get('oc'):
        oc = copy.deepcopy(item_template)
        oc['name'] = data['oc']
        oc['screen_name'] = data['oc']
        oc['username'] = data['oc_mobile']
        oc['mobile'] = data['oc_mobile']
        oc['category'] = '4'  # 1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员，6：维修工区域经理
        try:
            print 'oc:', User(**oc).save().id
        except:
            pass


def create_provider_user():
    item_template = {
        u'head_type': 4,
        u'password': u'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs=',
        u'source': u'乐辛',
        u'city': u'上海市',
        u'area': u'华东区',
        u'company': u'乐辛',
        u'is_staff': False,
        u'is_active': 1,
        u'is_superuser': 3,  # 注意替换
        u'is_update': False,
        u'create_time': dt.now(),
        u'date_joined': dt.now(),
    }

    area_manager = copy.deepcopy(item_template)
    area_manager['name'] = u'徐平'
    area_manager['screen_name'] = u'徐平'
    area_manager['username'] = '13061732239'
    area_manager['mobile'] = '13061732239'
    area_manager['category'] = '2'
    manager = User(**area_manager).save()
    print 'area_manager:', manager.id

    for repair_item in [(u'张青岭', '13764252825'), (u'张传超', '15901764709')]:
        repair = copy.deepcopy(item_template)
        repair['name'] = repair_item[0]
        repair['screen_name'] = repair_item[0]
        repair['username'] = repair_item[1]
        repair['mobile'] = repair_item[1]
        repair['category'] = '0'
        del repair['is_superuser']
        repair_user = User(**repair).save()
        print 'repair:', repair_user.id


        print Member(**{
            'opt_user': manager,
            'user': repair_user,
            'category': manager.head_type,
            'area': manager.area,
            'city': manager.city,
            'company': manager.company,
            'head_type': manager.head_type,
            'store': '永和大王',
        }).save().id

def create_push():
    head_type = 4
    # area_manager = User.objects.filter(head_type=head_type, category=3).first()
    # area = area_manager.area
    # city = area_manager.city
    # provider_user = User.objects.filter(head_type=head_type, category=2).first()
    # provider = str(provider_user.id)
    # company = provider_user.company
    # manager =
    #
    # for service in User.objects.filter(head_type=head_type, category=0):
    #
    # area_manager        = ListField(StringField()) #二级推送
    # manager             = ListField(StringField())  #汉堡王区域负责人

# USER_CATEGORY = {
#     '0': u'维修员',
#     '1': u'商户',
#     '2': u'维修服务商主管',
#     '3': u'商户区域经理',
#     '4': u'商户OC',
#     '5': u'商户管理员',
#     '6': u'维修工区域经理'
# }


if __name__ == '__main__':
    # generate_rid()
    create_stores()
    create_provider_user()

# db.store.update({head_type:4,name:'广元店'}, {$set:{rid:'57eb2ae452d8ff5b389255e4'}}, false, true);
# db.store.update({head_type:4,name:'万源店'}, {$set:{rid:'57eb2ae452d8ff5b389255e5'}}, false, true);
# db.store.update({head_type:4,name:'漕溪店'}, {$set:{rid:'57eb2ae452d8ff5b389255e6'}}, false, true);
# db.store.update({head_type:4,name:'东安店'}, {$set:{rid:'57eb2ae452d8ff5b389255e7'}}, false, true);
# db.store.update({head_type:4,name:'南方店'}, {$set:{rid:'57eb2ae452d8ff5b389255e8'}}, false, true);
# db.store.update({head_type:4,name:'漕宝店'}, {$set:{rid:'57eb2ae452d8ff5b389255e9'}}, false, true);
# db.store.update({head_type:4,name:'沪闵路店'}, {$set:{rid:'57eb2ae452d8ff5b389255ea'}}, false, true);
# db.store.update({head_type:4,name:'南站二店'}, {$set:{rid:'57eb2ae452d8ff5b389255eb'}}, false, true);
# db.store.update({head_type:4,name:'莲花南路店'}, {$set:{rid:'57eb2ae452d8ff5b389255ec'}}, false, true);
# db.store.update({head_type:4,name:'锦江乐园店'}, {$set:{rid:'57eb2ae452d8ff5b389255ed'}}, false, true);

