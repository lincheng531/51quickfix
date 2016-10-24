#!/user/bin/env python
#encoding:utf-8


import os
import time
import traceback
import random
import json
from datetime import datetime as dt
from bson.objectid import ObjectId
from settings import DB, REDIS, ENV
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate
from django.shortcuts import render_to_response as render
from apps.base.common import json_response, get_json_data, get_user, login_required, get_pinyin_initials
from apps.base.models import User, Maintenance, Device, Region, Product, Brand, Store, InventoryHeader, InventoryDetail
from apps.base.messages import *
from apps.base.logger import getlogger
from apps.base.utils import login, pf2 
from settings import DEBUG, HOST_NAME, ENV
from apps.base.sms import send_sms
from apps.base.uploader import upload as _upload
from apps.base.common import base_login_required as login_required


logger = getlogger(__name__)  

'''
    盘点通知：{'type':9, 'start_time':开始时间, 'end_time':结束时间, 'oid':盘点id}
    盘点快结束通知：{'type':10, 'start_time':开始时间, 'end_time':结束时间}

'''

@login_required('1')
def list(request):
    """  任务列表

    :uri: /api/v1/task/list
    :return:
        * id            盘点活动id
        * type          类型 0:为盘点
        * total         总共盘点数
        * complete      已经完成盘点数
        * lost          缺失数
        * status        状态 0为未开始 1为进行中 2为已经完成
        * title         标题
        * start_time    开始时间
        * end_time      截止时间
        * publis_time   发布时间
    """ 

    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    headers = InventoryHeader.objects.filter(__raw__={'store':user.store_id}).order_by('-create_time')
    results = []
    store = Store.objects.filter(id=ObjectId(user.store_id)).first()
    for header in headers:
        total = InventoryDetail.objects.filter(header=header,store=store).count()
        complete = InventoryDetail.objects.filter(header=header,store=store,status__in=[1, 2]).count()
        lost  = InventoryDetail.objects.filter(header=header,store=store,status=1).count()
        status = 0
        if complete == 0:
            status = 0 
        elif complete < total:
            status = 1
        else:
            status = 2
        results.append({
                'id':str(header.id),
                'total':total,
                'type':0,
                'complete':complete,
                'lost':lost,
                'status':status,
                'title':header.title,
                'start_time':header.start_time,
                'end_time':header.end_time,
                'publis_time':header.create_time
        })
    resp['info']['results'] = results
    return json_response(resp)



@login_required('1')
def inventory(request, oid):
    """  盘点数据列表

    :uri: /api/v1/task/inventory/<oid:盘点活动id>
    :return:
        * id            盘点id
        * complete      已经完成盘点数
        * total         所有盘点数
        * lost          缺失数
        * device        设备名称
        * device_id     设备id
        * uid           流水号
        * no            固定资产编号
        * product_no    供应商
        * brand         品牌
        * model         型号
        * specifications 规格
        * supplier      供应商
        * psnumber      序列号
        * rid           二维码随机字符串
        * scrap_time    过期时间
        * category      0为手工盘点 1为自动盘点
        * status        0为未盘点 1为缺失 2为存在
        * content       使用说明
    """  
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    header  = InventoryHeader.objects.get(id=ObjectId(oid))
    results = []
    resp['info']['title'] = header.title
    store = Store.objects.get(id=ObjectId(user.store_id))
    details = InventoryDetail.objects.filter(header=header,store=store)
    complete, total, lost = 0, details.count(), 0
    for detail in details: 
        device = detail.device
        if detail.status == 2: complete += 1
        if detail.status == 1: lost+=1
        results.append({'id':str(detail.id), 
                        'device':device.name, 
                        'device_id':str(device.id),
                        'uid':device.uid,
                        'no':device.no,
                        'psnumber':device.psnumber,
                        'product_no':device.product_no,
                        'brand':device.brand,
                        'rid':device.rid,
                        'model':device.model,
                        'specifications':device.specifications,
                        'supplier':device.provider,
                        'status':device.status,
                        'scrap_time':device.scrap_time,
                        'status':detail.status,
                        'category':detail.cate,
                        'content':detail.content,
                        'initial':device.initial})
    resp['info']['complete'] = complete + lost
    resp['info']['total'] = total
    resp['info']['lost'] = lost
    resp['info']['results'] = results
    logger.info(resp)
    return json_response(resp)


@login_required('1')
def check(request, oid):
    """  手动盘点

    :uri: /api/v1/task/check/<oid:盘点id>
    :post:
        * status 资产状态 1为缺失 2为存在
        * content 使用说明
        * logo 上传图片，多个请用“,”隔开
    :return:
        * status 整个盘点活动:1为已经完成 0为未完成
    """  
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    logger.info("debug1:{}".format(data))
    user = get_user(request)
    status, content, logo = [data.get(i) for i in ['status', 'content', 'logo']]
    inventory = InventoryDetail.objects.filter(id=ObjectId(oid), status=0).first()
    if not inventory:
        resp['alert'] = u'该盘点不存在，或者该盘点已经盘点了'
        return  json_response(resp)
    inventory.status = int(status)
    inventory.content = content
    inventory.logo  = logo.split(',')
    inventory.cate = 0
    inventory.save()
    header = inventory.header
    resp['info']['status'] = 1 if InventoryDetail.objects.filter(store=inventory.store, header=inventory.header, status=0).count() == 0 else 0
    header.status = 1
    if resp['info']['status'] == 1:
        header.complete += 1 
        if header.complete == header.total:
            header.status = 2
    header.save()
    resp['status'] = 1
    return json_response(resp)


@login_required('1')
def scan(request, oid):
    """  扫码盘点

    :uri: /api/v1/task/scan/<oid:二维码数据>
    :post:
        * hid  盘点活动id
    :return:
        * id 盘点id
        * checked 1:为已经盘点 0:为未盘点
        * status 整个盘点活动:1为已经完成 0为未完成
    """  
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    hid  = data.get('hid') 
    device = Device.objects.filter(rid=oid).first()
    if not device:
        resp['alert'] = u'该设备不存在'
        return json_response(resp)
    store = Store.objects.get(id=ObjectId(user.store_id))
    header    = InventoryHeader.objects.get(id=ObjectId(hid), store=user.store_id)
    inventory = InventoryDetail.objects.filter(header=header, device=device, store=store).first()
    if inventory.status == 0:
        inventory.cate = 1
        inventory.status = 2 
        resp['info']['checked'] = 0
        inventory.save()
    else:
        resp['info']['checked'] = 1
        resp['alert'] = u'该设备已经盘点'
        return json_response(resp)
    header.status = 1
    resp['info']['id'] = str(inventory.id)
    resp['info']['status'] = 1 if InventoryDetail.objects.filter(store=device.store, header=header, status=0).count() == 0 else 0
    if resp['info']['status'] == 1:
        header.complete += 1 
        if header.complete == header.total:
            header.status = 2 
    header.save()
    resp['status'] = 1 
    return json_response(resp)
    



    