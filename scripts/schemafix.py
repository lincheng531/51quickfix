# -*- encoding: utf-8 -*-
from datetime import datetime as dt
from pymongo import Connection
from bson.objectid import ObjectId
import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from apps.base.models import Maintenance, MaintenanceHistory, MaintenanceCollection

def migrate_collection():
    for item in Maintenance.objects():

        mhid = MaintenanceHistory(**{
            'grab_users': [item.grab_user] if item.grab_user else [],
            'user': item.user,
            'maintenances': [item.id],
            'create_time': item.create_time,
            'update_time': item.update_time,
            'source': 'migrate',
            'members': item.members,
        }).save()

        mcid = MaintenanceCollection(**{
            'grab_users': [item.grab_user] if item.grab_user else [],
            'user': item.user,
            'histories': [mhid],
            'create_time': item.create_time,
            'update_time': item.update_time,
            'source': 'migrate',

            'store_name': item.store_name,
            'store': item.store,
            'store_no': item.store_no,
            'address': item.address,
            'state': item.state,
            'must_time': item.must_time,
            'members': item.members,
        }).save()


if __name__ == '__main__':
    migrate_collection()