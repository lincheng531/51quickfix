# -*- encoding: utf-8 -*-
from datetime import datetime as dt
from pymongo import Connection
import sys

company_dict = {
    '2': u'汉堡王'
}


def create(store_no, name, mobile, head_type):
    conn = Connection()
    DB = conn['51quickfix']
    print store_no, name, mobile

    store = DB.store.find_one({'no':no})
    print store

    if not store:
        store = {}

    items = {
            u'store_id': str(store.get('_id')),
            u'store': store.get('name'),
            u'loc': store.get('loc'),
            u'is_staff': False,
            u'user_permissions': [],
            u'category': u'1',
            u'city': store.get('city'),
            u'area': store.get('area'),
            u'avatar_img': u'/static/img/store/{}.png'.format(head_type),
            u'head_type': head_type,
            u'address': store.get('address'),
            u'username': mobile,
            u'company_logo': u'/static/img/store/{}.png'.format(head_type),
            u'company': company_dict.get(str(head_type)),
            u'is_active': 1,
            u'is_superuser': 0,
            u'password': u'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs=',
            u'source': company_dict.get(str(head_type)),
            u'name': name,
            u'mobile': mobile,
            u'is_update': False,
            u'create_time': dt.now(),
            u'date_joined': dt.now(),
            u'_cls': u'User.User'
            }
    if not DB.user.find_one({'username':mobile}):
        DB.user.save(items)
    else:
        DB.user.update({'username':mobile},{'$set':items})

if __name__ == '__main__':
    no, name, mobile, head_type = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    create(no, name, mobile, head_type)
    #python scripts/create_account.py no  name mobile  headtype