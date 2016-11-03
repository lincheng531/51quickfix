# -*- encoding: utf-8 -*-
import copy
import os, sys
reload(sys)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.setdefaultencoding('utf-8')
BASEDIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(BASEDIR + '../../..'))

from bson.objectid import ObjectId
from apps.base.models.store_schemas import *
from apps.base.models.schemas import *

def generate_rid():
    model = Device
    need = 1000
    total = 0
    rids = []

    while total < need:
        rid = str(ObjectId())

        if getattr(model, 'objects').filter(rid=rid):
            continue

        rids.append(rid)
        total += 1
        print len(rids), rid

    with open('blank_qrcode.txt', 'wb') as f:
        f.write('\n'.join(rids))



if __name__ == '__main__':
    generate_rid()