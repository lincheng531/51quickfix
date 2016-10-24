#!/user/bin/env python
# encoding:utf-8
import os
import time
import json
import requests
from bson.objectid import ObjectId
from apps.base import xinge
from apps.base.logger import getlogger
from settings import DEBUG, DB, celery_app, PUSH_ANDROID, M_PUSH_ANDROID, M_PUSH_IOS, PUSH_IOS, SMSAPIKEY, ENV


logger = getlogger(__name__)


@celery_app.task(bind=True, default_retry_delay=60, max_retries=3)
def send_sms(self, mobile, text):
    try:
        query = {'apikey':SMSAPIKEY,'mobile':mobile, 'text':text}
        r = requests.post('http://yunpian.com/v1/sms/send.json', query)
        if r.status_code <> 200:
            raise
    except Exception as e:
        self.retry(args=[mobile, text], exc=e, countdown=2)
        return False
    return True


def _push_message_to_android(device_token, category, content, data={}):
    try:
        logger.info("content:{}".format(content))
        device_token    = device_token.replace(' ','')
        msg = xinge.Message()
        style = xinge.Style(1,1,1,1)
        msg.style = style
        msg.type = 1
        msg.content = content
        msg.action = xinge.ClickAction(1,activity='')    
        if data and len(data) > 0:       
            msg.custom = data
        msg.expireTime = 3600
        logger.info(u"push_message_to_android@%s;content:%s;data:%s;category:%s,ENV:%s" % (device_token, content, str(data), category, 2 if ENV in ['TEST', 'TEST2'] else 1 ))
        if category == '1':
            result = M_PUSH_ANDROID.PushSingleDevice(device_token, msg)
        else:
            result = PUSH_ANDROID.PushSingleDevice(device_token, msg)
        logger.info("send xg to android:%s" % str(result))
    except Exception as e:
        logger.info("push_message_to_android:{}".format(str(e)))
        return 1, str(e)
    else:
        return result
    
    
def _push_message_to_ios(device_token, category, content, data={}):
    try:
        device_token    = device_token.replace(' ','')
        msg = xinge.MessageIOS()
        msg.alert = content
        if data and len(data) > 0:
            msg.custom = data
        msg.expireTime = 3600
        msg.sound = "default"
        logger.info("push_message_to_ios@%s;content:%s;data:%s;category:%s:env:%s" % (device_token, content, str(data), category, 2 if ENV in ['TEST', 'TEST2'] else 1))
        if category == '1':
            result = M_PUSH_IOS.PushSingleDevice(device_token, msg, 2 if ENV in ['TEST', 'TEST2'] else 1)
        else:
            result = PUSH_IOS.PushSingleDevice(device_token, msg, 2 if ENV in ['TEST', 'TEST2'] else 1)
        logger.info("send xg to iphone:%s" % str(result))
    except Exception as e:
        logger.info("push_message_to_ios:{}".format(str(e)))
        return 1, str(e)
    else:
        return result

@celery_app.task(bind=True, default_retry_delay=60, max_retries=3)
def push_message(self, user_oid, message, data={}):
    user = DB.user.find_one({'_id':user_oid},fields=['username','device_token','platform', 'category'])

    if not user:
        logger.info('user:{} does not exists'.format(user_oid))
        return None

    device_token = user.get('device_token')
    platform     = user.get('platform','').lower()
    username     = user.get('username')
    category     = user.get('category')

    if not device_token:
        logger.error('user:{},device_token:{}'.format(username,device_token))
        return None

    for k, v in data.items():
        data[k] = str(v)

    try:
        if platform == 'android':
            status, msg = _push_message_to_android(device_token, category, message, data=data)
        else:
            status, msg = _push_message_to_ios(device_token, category, message, data=data)
        if status <> 0:
            raise
    except Exception as e:
        logger.info(str(e))
        self.retry(args=[user_oid, message, data], exc=e, countdown=2)
        return False
    return True



if __name__ == '__main__':
    celery_app.send_task('sync.sync.send_sms',['15017935316', 'hello sync'])





