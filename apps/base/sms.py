#!/user/bin/env python
#encoding:utf-8


from settings import celery_app
from apps.base.logger import getlogger

logger = getlogger(__name__)

def send_sms(mobile, text, extend=None):
	logger.info("sms:{}:{}:{}".format(mobile, text, extend)) 
	celery_app.send_task('sync.sync.send_sms',[mobile, text])


