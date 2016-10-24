#!/user/bin/env python
#encoding:utf-8


import os
import time
import traceback
import random
import json
import lxml.html
from datetime import datetime as dt
from bson.objectid import ObjectId
from settings import DB, REDIS, ENV
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate
from apps.base.common import json_response, get_json_data, get_user, login_required
from apps.base.models import User
from apps.base.messages import *
from apps.base.logger import getlogger
from apps.base.utils import login 
from settings import DEBUG, HOST_NAME, ENV
from apps.base.sms import send_sms
from apps.base.uploader import upload as _upload
from django.shortcuts import render_to_response as render


logger = getlogger(__name__)

def list(request):
    """ 文章列表

    :uri: /api/v1/article/list

    :GET params:
        * type 1 为通知通告 2为消防知识

    """

    resp = {'status':1, 'info':{}, 'alert':''}
    data = get_json_data(request) or request.GET.dict()
    head_type = int(data.get('type', 1))
    articles = None
    if head_type == 1:
        articles = DB.article.find({'category':u'通知通告'}).sort('_id', -1)
    elif head_type == 2:
        articles = DB.article.find({'category':u'消防知识'}).sort('_id', -1)
    logger.info("debug:{}:{}".format(articles.count(), head_type))
    results = []
    if articles:
        for article in articles:
            results.append({
                'title':article.get('title'),
                'content':article.get('content'), 
                'source':article.get('source'),
                'create_time':article.get('create_time'),
                'category':article.get('category')
            })
    resp['info']['results'] = results
    return  json_response(resp)
    
def detail(request,aid):
    """ 文章详情

    :uri: '/api/v1/article/detail/<aid>'

    :params GET: null

    """


    resp = {'status':1,'info':{},'alert':''}

    oid = ObjectId(aid)
    article = DB.article.find_and_modify({'_id':oid}, {'$inc':{'view_count':1}})
    resp['info']['article'] = article
    
    # lazy load image
    try:
        tree = lxml.html.fromstring(article['content'])
        for img  in tree.xpath('.//img'):
            src = img.get('src', '')
            if src:
                img.set('data-original', src)
                img.set('class', 'lazy')
            else:
                # remove empty img tag
                img.getparent().remove(img)   

        html = lxml.html.tostring(tree)
        article['content'] = html
    except Exception, e:
        pass

    return render('article2mobile.html',locals())