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

sheet = xlrd.open_workbook(os.path.join(BASEDIR, u'dml_store_20161205.xlsx'))

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
        print 'store manager:', User(**store_manager).save().id
    #
    # if data.get('area_manager'):
    #     area_manager = copy.deepcopy(item_template)
    #     area_manager['name'] = data['area_manager']
    #     area_manager['screen_name'] = data['area_manager']
    #     area_manager['username'] = data['area_manager_mobile']
    #     area_manager['mobile'] = data['area_manager_mobile']
    #     area_manager['category'] = '3'  # 1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员，6：维修工区域经理
    #     try:
    #         print 'area_manager:', User(**area_manager).save().id
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
    #         print 'oc:', User(**oc).save().id
    #     except:
    #         pass


def create_sh_stores():
    table = sheet.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    error_users = []

    for i in xrange(nrows):
        print 'row: ', i+1
        if i % 2 or i == 0:
            continue

        user_data = {}
        store = Store()
        store.head_type = 3
        store.brand = u'达美乐'
        store.city = u'上海市'
        store.area = u'华东区'

        for j in xrange(ncols):
            cell = table.cell(i, j)
            data = cell.value

            if data:
                print j, data
            else:
                continue

            if j == 0:
                store.name = data
            if j == 1:
                store.no = str(int(data))
            if j == 2:
                store.opening_time = datetime.datetime(*xlrd.xldate.xldate_as_tuple(data, 0))
            if j == 5:
                try:
                    store.tel = str(int(data))
                except ValueError:
                    store.tel = data
            if j == 7:
                store.email = table.cell(i+1, j).value or data
            if j == 8:
                store.address = data

            if j == 6:
                store.store_manager = data
                user_data['store_manager'] = data
                user_data['store_manager_mobile'] = str(int(table.cell(i+1, j).value))

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

        print store.name,
        print store.no,
        print store.opening_time,
        print store.tel,
        print store.email,
        print store.address

        store.save()
        user_data['store_id'] = str(store.id)
        user_data['store'] = store.name
        print json.dumps(user_data, ensure_ascii=False)
        try:
            create_store_user(user_data, store)
        except Exception as e:
            user_data['error_msg'] = e
            error_users.append(user_data)
        print
        print

    print 'error users:', len(error_users)
    for u in error_users:
        print u


def create_bj_stores():
    table = sheet.sheets()[1]
    nrows = table.nrows
    ncols = table.ncols
    error_users = []

    for i in xrange(nrows):
        print 'row: ', i+1
        if i % 3 !=2:
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
                print j, data
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
                    user_data['store_manager_mobile'] = str(int(table.cell(i+1, j).value))
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

        print store.name,
        print store.no,
        print store.opening_time,
        print store.tel,
        print store.email,
        print store.address

        store.save()
        user_data['store_id'] = str(store.id)
        user_data['store'] = store.name
        print json.dumps(user_data, ensure_ascii=False)
        try:
            create_store_user(user_data, store)
        except Exception as e:
            user_data['error_msg'] = e
            error_users.append(user_data)
        print
        print

    print 'error users:', len(error_users)
    for u in error_users:
        print u

if __name__ == '__main__':
    # create_sh_stores()
    create_bj_stores()