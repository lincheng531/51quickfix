#encoding:utf-8
import os
import math
import time
import datetime
import calendar
import json
import socket
import random
import simplejson
import demjson
from functools import wraps
from datetime import datetime as dt
from bson.objectid import ObjectId
from django.http import HttpResponse,HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from settings import DEBUG
from django.core.mail import EmailMessage
from pymongo.errors import DuplicateKeyError
from apps.base.messages import LOGIN_REQUIRED
from apps.base.models import User
from settings import DB, celery_app, DEBUG
from apps.base.logger import getlogger
from apps.base.sms import send_sms

from pypinyin import pinyin, lazy_pinyin
import pypinyin

logger = getlogger(__name__)


def get_full_pinyin_initials(text):
    res = lazy_pinyin(text)
    return u''.join(res)
    

def get_pinyin_initials(text):
    if not text:return ""
    pinyin_text = ''.join([s[0] for s in lazy_pinyin(text) if len(s) > 0])
    #fixlist = [(u'单', 's'), (u'褚', 'c'), (u'解', 'x')]
    fixlist =  [(u'乘','C'),(u'乘','C'),(u'适','K'),(u'句','G'),(u'阚','K'),(u'车','C'),(u'叶','Y'),(u'合','H'),(u'冯','F'),(u'陶','T'),(u'汤','T'),(u'尾','W'),(u'贾','J'),
        (u'系','X'),(u'将','J'),(u'谷','G'),(u'宿','S'),(u'祭','Z'),(u'氏','S'),(u'石','S'),(u'盛','S'),(u'於','Y'),(u'强','Q'),(u'艾','A'),(u'塔','T'),(u'丁','D'),(u'种','Z'),(u'单','S'),
        (u'解','X'),(u'查','Z'),(u'区','O'),(u'繁','P'),(u'仇','Q'),(u'沈','S'),(u'宁','N'),(u'褚','C'),(u'适','K'),(u'句','G'),(u'阚','K'),(u'焦','J'),
        (u'车','C'),(u'叶','Y'),(u'合','H'),(u'冯','F'),(u'陶','T'),(u'汤','T'),(u'尾','W'),(u'贾','J'),(u'系','X'),(u'将','J'),(u'谷','G'),(u'宿','S'),(u'祭','Z'),(u'氏','S'),(u'石','S'),
        (u'盛','S'),(u'於','Y'),(u'强','Q'),(u'艾','A'),(u'塔','T'),(u'丁','D'),(u'种','Z'),(u'单','S'),(u'解','X'),(u'查','Z'),(u'区','O'),(u'繁','P'),(u'仇','Q'),(u'沈','S'),(u'宁','N'),(u'褚','C')
    ]

    res = []

    for i, j in zip(text, pinyin_text):
        for _i, _j in fixlist:
            if i == _i:
                j  = _j
        res.append(j.upper())

    return u''.join(res)


def get_json_data(request):
    if hasattr(request,'body') and request.body:
        data = {}
        try:
            data = simplejson.loads(request.body)
        except:
            try:
                data = demjson.decode(request.body)
            except Exception,e:
                return  request.POST.dict()

        return data
    return {}


def get_user(id_or_request):
    _type = type(id_or_request)
    if _type is str:
        oid = ObjectId(id_or_request)
    elif _type is WSGIRequest:
        return id_or_request.user
    elif _type is ObjectId:
        oid = id_or_request
    return User.objects.get(id=oid)


def json_format(data):
    if type(data) is dict:
        for k,v in data.items():

            if k.startswith('_'):
                del data[k]
                k = k[1:] 
            
            if k in ['cls','types']:continue

            data[k] = json_format(v)

        return data
    elif type(data) is ObjectId:
        return str(data)
    elif type(data) is datetime.datetime:
        return data.isoformat().rsplit(':',1)[0].replace('T',' ')
    elif type(data) is list:
        return [json_format(i) for i in data]
    else:
        return data


def json_response(data,callback=None):
    """ Return json response
    """
    if type(data) is dict:

        data = json_format(data)
    elif type(data) is list:
        data = [json_format(d) for d in data]

    if callback:
        data = json.dumps(data)
        data = u'{}({});'.format(callback,data)
        response = HttpResponse(data, mimetype='application/javascript;charset=utf-8',status=200)
    else:
        response = HttpResponse(json.dumps(data), mimetype='application/json;charset=utf-8',status=200)

    # response['Access-Control-Allow-Origin'] = '*'
    # response["Access-Control-Allow-Credentials"] = True
    # response['Access-Control-Allow-Methods'] = 'POST, GET, PUT, OPTIONS'
    # response['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, Key, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, Access-Control-Allow-Headers"
    return response

def base_login_required(category,is_active=1): 
    def decorte(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]
            if  request.user.is_authenticated():
                if (isinstance(category, list) and request.user.category in category) or \
                    (isinstance(category, basestring) and request.user.category == category) or not category:
                    
                    if request.user.is_active == is_active or is_active == 2:
                        return  func(*args,**kwargs)
            return json_response({'status':0,'alert':u'没该权限或请登录!'})
        return wrapper
    return decorte


def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        request = args[0]
        if  request.user.is_authenticated():
            return  func(*args,**kwargs)
        else:
            resp = {'status':0,'info':{}}
            resp['status'],resp['alert'] = LOGIN_REQUIRED
            return json_response(resp)
    return wrapper

    
def admin_login_required(head_type): 
    def decorte(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]
            if  request.user.is_authenticated():
                if request.user.is_superuser == head_type:  
                    return  func(*args,**kwargs)
            return HttpResponseRedirect('/admin/login')
        return wrapper
    return decorte



def send_email(subject,html,receivers):
    # TODO send email
    try:
        assert type(receivers) is list
        if DEBUG:
            email = EmailMessage(subject, html, to=receivers)
            email.content_subtype = 'html'
            email.send()
        else:
            celery_app.send_task('tasks.tasks.send_email',[subject,html,receivers])
        return True,email
    except Exception,e:
        logger.error('debug:{},msg:{}'.format(DEBUG,e))
        return False

    
def last_near(p):
    p = int(p)
    bm = p/100
    km = p/1000
    if km > 0:
        return u'%d公里' % km
    if bm > 0:
        return u'%d00米' % bm
    return u'%d米' % p
    
    
def last_login_time(login_time):
    t = dt.now() - login_time
    days = t.days
    years = days/356
    if years > 0:
        return u'%d年' % years
    month = days/30
    if month > 0:
        return u'%d月' % month
    if days > 0:
        return u'%d天' % days
    seconds = t.seconds
    hours = seconds/3600
    if hours >0:
        return u'%d小时' % hours
    minute = seconds/60
    if minute > 0:
        return u'%d分钟' % minute
    if seconds > 0:
        return u'%d秒' % seconds
    
    
    
def gen_token():
    return str(random.randrange(1000,9999))
    
    
if __name__ == '__main__':
    push_message('7d3d6bb5 f9fcc25d 02420186 d564d007 d212d0da 9466a284 f24061f3 8c2409bf','hello2')
