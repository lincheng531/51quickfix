#encoding:utf-8
import os
from shutil import copyfile
from datetime import datetime as dt
from bson.objectid import ObjectId as _id 
from apps.base.common import json_response, get_json_data
from settings import DEBUG,ROOT_PATH,DB,ENV,STATIC_ROOT
from apps.base.uploader import base_upload as _upload
from apps.base.common import login_required
from apps.base.logger import getlogger

logger = getlogger(__name__)


def upload(request):
    """ 统一的上传文件接口,以后所有需要上传文件的请求建议都以使用这个接口,方便统一管理
    
    :uri: /api/v1/upload/

    :Post Params:
        * imgFile 图片文件,必填，也可以用file字段 #测试数据 /logo/32/3e/9d/323e9d1227632e8ad82e82c715e8dbef.png
        * category 头像为logo 证书为 card

    """
    logger.info("start upload")
    resp = {'info':{},'status':0, 'alert':''}
    error, url = _upload(request)
    
    if error == 0:
        resp['error'] = 0
        resp['status']  = 1
        key = '{}_url'.format(request.REQUEST.get('category')) 
        resp['info'][key] = url
    else:
        resp['alert']  = u'上传文件失败'
    resp['url'] = url
    return json_response(resp)
    
