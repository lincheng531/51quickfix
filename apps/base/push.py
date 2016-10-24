#!/user/bin/env python
# encoding:utf-8


from apps.base.logger import getlogger
from settings import celery_app, DB


logger = getlogger(__name__)


def push_message(user_oid, message, data={}):
	logger.info("push_message:{}:{}:{}".format(user_oid, message, data))
	celery_app.send_task('sync.sync.push_message',[user_oid, message, data])

    


