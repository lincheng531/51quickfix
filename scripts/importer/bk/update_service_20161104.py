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
        u'is_superuser': 0,  # 注意替换
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

    item_template2 = {
        u'head_type': 2,
        u'password': u'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs=',
        u'source': u'张军',
        u'city': u'上海市',
        u'area': u'华东区',
        u'company': u'张军',
        u'is_staff': False,
        u'is_active': 1,
        u'is_superuser': 0,  # 注意替换
        u'is_update': False,
        u'create_time': dt.now(),
        u'date_joined': dt.now(),
    }

    for repair_item in [(u'应士良', '13611629201'), (u'陈军', '13916020737')]:
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


if __name__ == '__main__':
    main()
