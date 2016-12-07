#!/user/bin/env python
#encoding:utf-8


import os
import time
import traceback
import pymongo
import random
import json
from datetime import datetime as dt
from bson.objectid import ObjectId
from settings import DB, REDIS, ENV, SERVICE_COMPANY
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate
from apps.base.common import base_login_required as login_required
from apps.base.common import json_response, get_json_data, get_user, get_pinyin_initials
from apps.base.models import User, Maintenance, Device, Region, Product, Brand, Store
from apps.base.messages import *
from apps.base.logger import getlogger
from apps.base.utils import login, pf2 
from settings import DEBUG, HOST_NAME, ENV
from apps.base.sms import send_sms
from apps.base.uploader import upload as _upload
from django.shortcuts import render_to_response as render

logger = getlogger(__name__)  

@login_required(0, 2)
def store(request):
    """  录入数据->餐厅选择

    :uri: /api/v1/basics/store
    :post params:
        * id 餐厅的id,根据id可以取出单独餐厅的数据
        * name 餐厅名称(返回列表)
        * no   餐厅编号
    :return:
        * id 餐厅id
        * name 餐厅名称
        * area 位置
        * city 城市
        * district 区
        * no 餐厅编号
        * delivery_time 交店时间
        * opening_time 开业时间
        * tel 固定电话
        * fax 传真
        * loc 坐标
        * brand 品牌
        * brand_logo 品牌Logo
        * store_manager 门店经理
        * mobile手机号码
        * address 地址
        * initial 餐厅首字母

    """  
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    name, no, oid  = [data.get(i) for i in ['name', 'no', 'id']]
    query = {'head_type':user.head_type}
    if name:
        query['$or'] = [{'name':{'$regex':name}},{'no':{'$regex':name}}]
    if oid:
        query['_id'] = ObjectId(oid)
    stores = Store.objects(__raw__=query)
    results = []
    for s in stores:
        initial = s.initial
        if not initial:
            initial = get_pinyin_initials(s.name)
        results.append({'id':str(s.id),
                        'rid': s.rid,
                        'name':s.name, 
                        'area':s.area,
                        'city':s.city,
                        'district':s.district,
                        'brand':SERVICE_COMPANY.get(s.head_type),
                        'brand_logo':user.company_logo,
                        'no':s.no,
                        'delivery_time':pf2(s.delivery_time),
                        'opening_time':pf2(s.opening_time),
                        'tel':s.tel,
                        'fax':s.fax,
                        'loc':s.loc,
                        'address':s.address,
                        'store_manager':s.store_manager,
                        'mobile':s.mobile,
                        'initial':initial
                        })
    resp['info']['results'] = results
    return json_response(resp)

@login_required(0, 2)
def product(request):
    """  选择大类

    :uri: /api/v1/basics/product
    :post params:
        * name 设备名称(返回列表) 
        * brand 品牌
        * model  型号
    :return:
        * id 大类设备id
        * category 设备类型
        * name 设备名称
        * brand 设备品牌
        * model 设备型号
        * specifications 规格
        * supplier 供应商id
        * supplier_name 供应商名称
        * initial 设备首字母

    """ 
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    name = data.get('name')
    query = {'head_type':user.head_type}
    if name:
        query['$or'] = [{'name':{'$regex':name}},{'model':{'$regex':name}},{'brand_name':{'$regex':name}}]
    products = Product.objects(__raw__=query)
    results  = []
    for b in products:
        results.append({
                    'id':str(b.id),
                    'category': b.category,
                    'name': b.name,
                    'brand': str(b.brand.name),
                    'model': b.model,
                    'specifications': b.specification,
                    'supplier':str(b.supplier.id),
                    'supplier_name':b.supplier.name,
                    'initial': b.initial if b.initial else get_pinyin_initials(b.name)
            })
    resp['status'], resp['info']['results'] = 1, results
    return json_response(resp)


@login_required(0)
def equipment(request):
    """  选择设备,餐厅下的设备列表

    :uri: /api/v1/basics/equipment
    :post params:
        * store 店铺id有则返回该店铺下的设备，无则返回所有(必填)
        * name 设备名称(返回列表) 
    :return:
        * count 总个数
        *   id 设备id
        *   category 设备类型
        *   name 设备名称
        *   brand 设备品牌
        *   model 设备型号
        *   specifications 规格
        *   product  设备大类的id
        *   must_time         多少小时只有要到，加上当前时间用于多少前时间维修
        *   status            设备状态：1：紧急 2：非紧急
        *   initial 设备首字母
    """   
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    name, store = [data.get(i) for i in ['name', 'store']]
    query = {'head_type':user.head_type}
    if name:
        query['$or'] = [{'name':{'$regex':name}}, {'brand':{'$regex':name}}]
    if store:
        query['store'] = ObjectId(store)
    logger.info('debug:{}'.format(query))
    bkcs = Device.objects(__raw__=query)
    results = []
    for b in bkcs:
        item = {
                'id':str(b.id),
                'category': b.category,
                'name': b.name,
                'brand': b.brand,
                'model': b.model,
                'product':b.product,
                'specifications': b.specifications,
                'initial': b.initial if b.initial else get_pinyin_initials(b.name)
            }
        item.update(b.detail())
        results.append(item)
    resp['status'], resp['info']['results'] = 1, results
    resp['info']['count'] = len(results)
    return json_response(resp) 


@login_required(0, 2)
def brand(request):
    """  选择品牌

    :uri: /api/v1/basics/brand
    :post params:
        * name 品牌名称(返回列表)
    :return:
        * brand 设备品牌
        * initial 设备首字母
    """   
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    name = data.get('name')
    if name:
        brands = Brand.objects.filter(name__icontains=name)
    else:
        brands = Brand.objects.filter()
    results = []
    for b in brands:
        results.append({'id':str(b.id), 'name':b.name, 'initial':b.initial})
    resp['status'], resp['info']['results'] = 1, results
    return json_response(resp) 

def region(request):
    """ 区域

    :uri: /api/v1/basics/region
    :post params:
        * id 当前id，获取id下属区域，为空则全部
        * name 城市名称
    :return:
        * id 当前id
        * name 城市名称
        * initial 首字母
        * parent 上一级名称
    """

    resp    = {'status':1, 'info':{}, 'alert':''}
    user    = get_user(request)
    data    = get_json_data(request) or request.POST.dict()
    parent_id, name = [data.get(i) for i in ['id', 'name']]
    if parent_id:
        regions = Region.objects.filter(rid=parent_id)
    elif name:
        regions = Region.objects.filter(name__icontains=name, rid__icontains='c')
    else:
        regions = Region.objects.filter(parent_id='0')
    results = []
    for r in regions:
        subrs = Region.objects.filter(parent_id=r.rid)
        for s in subrs:
            results.append({'name':s.name, 'id':s.rid, 'initial':s.name_en, 'parent_name':r.name})
    resp['info']['results'] = results
    return json_response(resp)

@login_required(0, 2)
def history(request, oid):
    """ 资产卡片

    :uri: /api/v1/basics/history/<oid:product_id>
    :return:
        * status 2是成功 4是失败
        * content 故障描述
        * user 维修工名称
        * 维修时间

    """

    resp = {'status':1, 'info':{}, 'alert':''}
    results = []
    mtcs = Maintenance.objects.filter(product_id=ObjectId(oid), status__in=[2, 3, 4]).order_by('-create_time')
    for mt in mtcs:
        results.append({
                        'status':mt.status,
                        'content':mt.content,
                        'user':mt.user.name,
                        'create_time':mt.create_time
                        })
    resp['info']['results'] = results
    return  json_response(resp)

@login_required(None)
def device_detail(request, id):
    resp = {'status':1, 'info':{}, 'alert':''}
    user = get_user(request)
    device = Device.objects.get(id=ObjectId(id))

    if str(device.store.id) != str(user.store_id):
        resp['status'], resp['alert'] = 0, u'用户没有权限'
        return json_response(resp)

    resp['info'] = device.get_result()
    return  json_response(resp)


def brand(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    resp['info']['result'] = [item for item in DB.brand.find().sort('initial', pymongo.ASCENDING)]
    return json_response(resp)