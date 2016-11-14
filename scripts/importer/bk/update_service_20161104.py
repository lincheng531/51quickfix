# -*- encoding: utf-8 -*-
import copy
import xlrd
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


def main():
    item_template1 = {
        u'head_type': 2,
        u'password': u'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs=',
        u'source': u'易芳',
        u'city': u'上海市',
        u'area': u'华东区',
        u'company': u'易芳',
        u'is_staff': False,
        u'is_active': 1,
        u'is_superuser': 3,  # 注意替换
        u'is_update': False,
        u'create_time': dt.now(),
        u'date_joined': dt.now(),
    }

    area_manager = copy.deepcopy(item_template1)
    area_manager['name'] = u'张芳'
    area_manager['screen_name'] = u'张芳'
    area_manager['username'] = '13671995028'
    area_manager['mobile'] = '13671995028'
    area_manager['category'] = '2'
    manager = User(**area_manager).save()
    print 'area_manager:', manager.id

    main_manager = copy.deepcopy(item_template1)
    main_manager['name'] = u'闫军锋'
    main_manager['screen_name'] = u'闫军锋'
    main_manager['username'] = '18918726265'
    main_manager['mobile'] = '18918726265'
    main_manager['category'] = '6'
    main_manager_user = User(**main_manager).save()
    print 'main_manager:', main_manager_user.id

    for repair_item in [(u'刘宝', '15900823675'), (u'阎军辉', '13816276916')]:
        repair = copy.deepcopy(item_template1)
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
            'store': '汉堡王',
        }).save().id

        print Member(**{
            'opt_user': main_manager_user,
            'user': repair_user,
            'category': main_manager_user.head_type,
            'area': main_manager_user.area,
            'city': main_manager_user.city,
            'company': main_manager_user.company,
            'head_type': main_manager_user.head_type,
            'store': '汉堡王',
        }).save().id

    manager = User.objects.get(mobile='18916765521')
    manager.category = '2';
    manager.is_superuser = 3;
    manager.company = u'张军'
    manager.save()

    item_template2 = {
        u'head_type': 2,
        u'password': u'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs=',
        u'source': u'张军',
        u'city': u'上海市',
        u'area': u'华东区',
        u'company': u'张军',
        u'is_staff': False,
        u'is_active': 1,
        u'is_superuser': 3,  # 注意替换
        u'is_update': False,
        u'create_time': dt.now(),
        u'date_joined': dt.now(),
    }


    main_manager = copy.deepcopy(item_template2)
    main_manager['name'] = u'陈军'
    main_manager['screen_name'] = u'陈军'
    main_manager['username'] = '13916020737'
    main_manager['mobile'] = '13916020737'
    main_manager['category'] = '6'
    main_manager_user = User(**main_manager).save()
    print 'main_manager:', main_manager_user.id

    for repair_item in [(u'应士良', '13611629201'),]:
        repair = copy.deepcopy(item_template2)
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
            'store': '汉堡王',
        }).save().id

        print Member(**{
            'opt_user': main_manager_user,
            'user': repair_user,
            'category': main_manager_user.head_type,
            'area': main_manager_user.area,
            'city': main_manager_user.city,
            'company': main_manager_user.company,
            'head_type': main_manager_user.head_type,
            'store': '汉堡王',
        }).save().id

def update_sh_provider():
    sheet = xlrd.open_workbook(u'/Users/ethan/Desktop/update_bk_sh_provider.xls')
    table = sheet.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols

    count = 0
    no_devices = {}
    has_devices = []
    has_calls = {}
    stores = Store.objects.filter(no__in=['15983', '15309', '16997', '19596', '20084'])
    providers = [u'易芳', u'张军']


    for i in xrange(nrows):
        if i < 4:
            continue

        category = table.cell(i, 1).value.replace(u'类', '')
        efcategory = table.cell(i, 2).value
        name = table.cell(i, 4).value
        brand_name = table.cell(i, 5).value
        model = table.cell(i, 6).value

        warrant_in =table.cell(i, 15).value
        warrant_out =table.cell(i, 16).value

        if name in (u'制冰机, 1000磅', u'汽水机, 甜品站', u'滤水系统，主店3M'):
            if name == u'滤水系统，主店3M':
                name = name.split(u'，')[0]
            else:
                name = name.split(u',')[0]

        for store in stores:
            print category, efcategory, name, brand_name, model, warrant_in, warrant_out, store.name
            result = Device.objects.filter(category = category, efcategory=efcategory, name=name, store=store, brand=brand_name)
            if result.count() < 1:
                result = Device.objects.filter(category = category, efcategory=efcategory, name=name, store=store)
            if result.count() < 1:
                if warrant_in in providers or warrant_out in providers:
                    if i not in no_devices:
                        no_devices[i] = (i, category, efcategory, name, result.count(), warrant_in, warrant_out)
            else:
                has_devices.append(i)

                if warrant_in in providers or warrant_out in providers:
                    for device in result:
                        product = device.product
                        has_calls.setdefault(str(device.id), [])
                        has_calls[str(device.id)].append([str(store.id)])

                        if Call.objects.filter(device=device).count():
                            continue
                        Call(**{
                            'head_type': device.head_type,
                            'city': device.city,
                            'product': product,
                            'device': device,
                            'name': product.name,
                            'brand': product.brand,
                            'model': product.model,
                            'specification': product.specification,
                            'warranty_in': warrant_in,
                            'warranty_out1': warrant_out,
                        }).save()
                        count += 1


    print '===================>'
    diff_devices = set(no_devices.keys()) - set(has_devices)

    for i in diff_devices:
        item = no_devices[i]
        print item[0], item[1], item[2], item[3], item[4], item[5] or 'xxx', item[6] or 'xxx'

    print 'diff:', len(diff_devices)
    print 'new:', count


def create_push():
    head_type = 2
    oc = User.objects.get(username='13671995028')
    area = oc.area
    city = oc.city
    area_manager = User.objects.get(username='18918726265')
    provider_user = User.objects.get(username='13671995028')
    provider = str(provider_user.id)

    print Push(
        area = area,
        city = city,
        head_type = head_type,
        provider = provider,
        company = provider_user.company,
        area_manager = [area_manager.name, area_manager.mobile], #二级推送
        manager = [provider_user.name, provider_user.mobile],
        hq = ["周文辉","13585753381"]
    ).save().id

    head_type = 2
    oc = User.objects.get(username='18916765521')
    area = oc.area
    city = oc.city
    area_manager = User.objects.get(username='13916020737')
    provider_user = User.objects.get(username='18916765521')
    provider = str(provider_user.id)

    print Push(
        area = area,
        city = city,
        head_type = head_type,
        provider = provider,
        company = provider_user.company,
        area_manager = [area_manager.name, area_manager.mobile], #二级推送
        manager = [provider_user.name, provider_user.mobile],
        hq = ["周文辉","13585753381"]
    ).save().id

if __name__ == '__main__':
    main()
    update_sh_provider()
    create_push()
