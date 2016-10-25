#!/user/bin/env python
# encoding:utf-8


import os
import time
import random
import json
import datetime
from mongoengine import Q
from datetime import timedelta
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from bson.son import SON
from bson.objectid import ObjectId
from settings import DB, REDIS, ENV
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate
from apps.base.common import json_response, get_json_data, get_user, get_pinyin_initials
from apps.base.common import base_login_required as login_required
from apps.base.models import User, Maintenance, MaintenanceHistory, MaintenanceCollection, Product, Supplier, Bill, \
    MaintenanceUsers, Review, Device, ErrorCode, PushHistory, Member, Spare, BSpare, Store, Call, Brand
from apps.base.messages import PUSH0, PUSH6, PUSH3, PUSH15, PUSH21
from apps.base.push import push_message
from apps.base.logger import getlogger
from apps.base.utils import login, pf8, _send_count
from settings import DEBUG, HOST_NAME, ENV, REDIS, DEVICE_TYPE, SERVICE_COMPANY, FIX_TIME
from apps.base.sms import send_sms

logger = getlogger(__name__)

'''
    test user:11111111111/000000
'''


@login_required('1', 2)
def scan(request):
    """  扫描设备并传入设备的id(适用标准版和连锁版)

    :uri: /api/v1/merchant/scan

    :POST params: 
        * no 设备的no        测试:5629a4fc421aa9032437e937 store:5631e3a0c0828e147d49584e
        * type              1 为默认 2为汉堡王 测试:2 3为达美乐
    :Return:
        * status            设备状态：1：紧急 2：非紧急（作废, 具体看must_time）
        * name              设备名
        * no                汉堡王：固定资产编号
        * rid               唯一随机字符串
        * brand             品牌
        * address           地址
        * id                设备id测试id:55ee81440da60b01a672e931
        * store             肯德基大华店
        * must_time         多少小时只有要到，加上当前时间用于多少前时间维修
                            (作废，该数据从/api/v1/merchant/fault取，如果没用则默认：紧急4小时，非紧急72小时)

        * guarantee         0为保修外 1为保修内
        * type              post type
        * head_type         1为设备 2为商铺 3为空
        * restaurant_status 店铺状态 1为完整 0为不完整 扫描二维码会出现
        * restaurant        店铺id
        * assets_status     资产 1为完整 0为不完整 扫描二维码会出现
        * assets            资产id
        * loc               坐标地址
    """

    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    head_type, no = [data.get(i) for i in ['type', 'no']]
    user = get_user(request)
    # if no and head_type:
    #    if head_type == '2':
    resp['status'] = 1
    product = Device.objects.filter(head_type=user.head_type, rid=no).first()
    if product:
        detail = product.detail()
        if detail['guarantee'] == -2:
            resp['status'], resp['alert'] = 0, u'餐厅没有开业时间，请联系管理员'
            return json_response(resp)
        if detail['guarantee'] == -1:
            resp['status'], resp['alert'] = 0, u'标准设备没有报修时间，请联系管理员'
            return json_response(resp)
        store = product.store
        detail.update({
            'rid': no,
            'store': store.name if store else '',
            'address': store.address if store else '',
            'type': user.head_type,
            'head_type': 1,
            'restaurant_status': store.over_status if store else 0,
            'restaurant': str(store.id) if store else '',
            'assets_status': product.over_status,
            'assets': str(product.id),
            'loc': ','.join([str(i) for i in store.loc]) if store else ''
        })
        resp['info'] = detail
    else:
        store = Store.objects.filter(rid=no).first()
        if store:
            resp['info'] = {
                'rid': no,
                'store': store.name,
                'address': store.address,
                'type': user.head_type,
                'head_type': 2,
                'restaurant_status': store.over_status,
                'restaurant': str(store.id),
                'loc': ','.join([str(i) for i in store.loc]) if store else ''
            }
        else:
            resp['info'] = {'rid': no, 'type': head_type, 'head_type': 3}

    return json_response(resp)


@login_required(0, 2)
def fault(request):
    """  故障描述(适用标准版和连锁版)

    :uri: /api/v1/merchant/fault

    :POST params: 
        * product 设备大类的id
    :Return:
        * content 错误描述
        * id 错误描述id 
        * status 状态1为紧急 2为非紧急
        * must_time 到修时间
        * fix_time 维修时间 
    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    product = data.get('product')
    user = get_user(request)
    if product:
        results = []
        ers = ErrorCode.objects.filter(head_type=user.head_type, product=ObjectId(product))
        for e in ers:
            results.append(e.get_result())
        resp['status'], resp['info']['results'] = 1, results
    return json_response(resp)


@login_required(0, 2)
def errors(request):
    """  error code 对应价格（作废）

    :uri: /api/v1/merchant/errors
    :post params:
        * id id 不传为返回所有 传则返回该id的
    :return:
        * id  id
        * error code 名称
        * price 价格

    """
    data = get_json_data(request) or request.GET
    oid = data.get('id')
    resp = {'status': 1, 'info': {}, 'alert': ''}
    if oid:
        item = DB.errors.find_one({'_id': ObjectId(oid)})
        resp['info'] = {'id': oid, 'no': item['no'], 'price': item['price']}
    else:
        results = []
        categorys = DB.errors.find()
        for category in categorys:
            results.append({'id': str(category['_id']), 'no': category['no'], 'price': category['price']})
        resp['info']['results'] = results
    return json_response(resp)


@login_required(0, 2)
def spares(request):
    """  配件(适用标准版和连锁版)

    :uri: /api/v1/merchant/spares
    :post params:
        * id         id不传为返回所有 传则返回该id
        * name       配件名称或者编号
        * product_id 商品Id（必填）
        * bk(device) 设备id(必填)
        * bill       工单(维修单)的id（修改维修单时候必须提交）
    :return:
        * id         id
        * name       名称
        * price      价格
        * no         编号
        * product_id 商品id 仅供测试
        * over       是否再保修期内 0为保外 1为保内
    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST
    now = dt.now()
    oid, name, no, product_id, device, bill = [data.get(i) for i in ['oid', 'name', 'no', 'product_id', 'bk', 'bill']]
    logger.info(data)
    if not device:
        resp['status'], resp['alert'] = 0, u'设备id不得为空'
        return json_response(resp)

    bkc = Device.objects.filter(id=ObjectId(device)).first()
    if not bkc:
        resp['status'], resp['alert'] = 0, u'未找到设备，请联系管理员'
        return json_response(resp)
    product = bkc.product
    query = {'product_name': product.name, 'brand': product.brand.id}

    if oid: query['oid'] = ObjectId(oid)
    if name:
        query['$or'] = [{'name': {'$regex': name}}, {'no': {'$regex': name}}]

    results = []
    spares = Spare.objects(__raw__=query)
    for sp in spares:
        item = {'id': str(sp.id), 'no': sp.no, 'name': sp.name, 'price': round(getattr(sp, 'price', 0), 2), 'over': 0}

        query2 = {'spare': sp.id, 'device': device}
        if bill:
            query2.update({'bill__ne': ObjectId(bill)})
        bsp = BSpare.objects(__raw__=query2).order_by('-create_time').first()
        if bsp:
            warranty3 = int(getattr(sp, 'warranty3', 0)) if sp.warranty3 else 0
            if now < bsp.create_time + relativedelta(months=+warranty3):
                item['over'] = 1
        if bkc.guarantee == 1:
            item['over'] = 1
        results.append(item)
    resp['info']['results'] = results
    return json_response(resp)


@login_required(0, 2)
def suppliers(request):
    """  供应商(适用标准版和连锁版)

    :uri: /api/v1/merchant/suppliers
    :post params:
        * id id 不传为返回所有 传则返回该id的
    :return:
        * id   id
        * name 名称
    """

    data = get_json_data(request) or request.GET
    oid = data.get('id')
    resp = {'status': 1, 'info': {}, 'alert': ''}
    if oid:
        item = Supplier.objects.filter(id=ObjectId(oid))
        if item:
            resp['info'] = {'id': oid, 'name': item.name}
    else:
        results = []
        suppliers = Supplier.objects.filter()
        for supplier in suppliers:
            results.append({'id': str(supplier.id), 'name': supplier.name})
        resp['info']['results'] = results
    return json_response(resp)


@login_required(0, 2)
def products(request):
    """  设备品牌列表(取消)

    :uri: /api/v1/merchant/products
    :get params:
        * id 为供应商的id，有则是该供应商下得设备，无则所有
        * name 为名称用户检索
    :return:
        * id   商品id
        * logo 有可能为空
        * name 商品品牌名称
        * initial 缩写
    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.GET
    oid, name = [data.get(i) for i in ['id', 'name']]
    results = []
    query = {}
    if oid:
        query.update({'supplier': ObjectId(oid)})
    if name:
        query.update({'name': {'$regex': name}})
    categorys = DB.product.find(query)
    for category in categorys:
        results.append({
            'id': str(category['_id']),
            'logo': category.get('logo', ''),
            'name': category['name'],
            'initial': get_pinyin_initials(category['name'])
        })
    resp['info']['results'] = results
    return json_response(resp)


@login_required('1')
def call(request):
    """  叫修 (适用标准版和连锁版)

    :uri: /api/v1/merchant/call

    :POST params:
        * type 1 为标准版:
            * cid       设备id 5621b9b00da60b02862e21e2
            * logo      故障图片 #https://www.baidu.com/img/bd_logo1.png
            * error     错误描述content
            * eid       错误描述id，从api/v1/merchant/fault获取，选择其他则为空
            * start_time   起始时间 20160414112300
            * end_time     结束时间 20160414112300

        * type > 1为连锁版:
            * cid       设备id 5621b9b00da60b02862e21e2
            * logo      故障图片 #https://www.baidu.com/img/bd_logo1.png
            * error     错误描述content    测试数据：content: error1, id: 55ee8d180da60b02aa8d7960, no: BK141114SH0001EQ
            * eid       错误描述id，从api/v1/merchant/fault获取，选择其他则为空
            * area      区域 #长宁区 暂时用这个（作废）
            * loc       坐标 x,y 中间‘,’隔开 （作废）
            * state     状态 1:紧急 2:一般 (当选择其他的时候允许人工选择紧急：1，和非紧急：2)，采购都未为非紧急
            * is_buy    1为采购 0为不是
    :return:
            * count 已经通知多少维修工
    """
    resp = {'status': 1, 'info': {}, 'alert': ''}
    now = dt.now()
    loggend_user = get_user(request)
    data = get_json_data(request) or request.POST.dict()
    head_type = int(data.get('type', 1))
    logo, error, cid, area, loc, state, eid, start_time, end_time = [data.get(i) for i in
                                                                     ['logo', 'error', 'cid', 'area', 'loc', 'state',
                                                                      'eid', 'start_time', 'end_time']]
    if eid:
        error_code = ErrorCode.objects.filter(id=ObjectId(eid)).first()
        if not error_code:
            resp['status'], resp['alert'] = 0, u'error code不得为空'
            return json_response(resp)
        error_content = error_code.get_result()
        state, must_time, fix_time = [error_content.get(i) for i in ['status', 'must_time', 'fix_time']]
    else:
        if state:
            state = int(state)
            if state not in [1, 2]:
                resp['status'], resp['alert'] = 0, u'叫修只有两个状态'
                return json_response(resp)

            must_time, fix_time = FIX_TIME[state]

    device = Device.objects.filter(id=ObjectId(cid), head_type=loggend_user.head_type).first()
    if not device:
        resp['status'], resp['alert'] = 0, u'没有找到该设备'
        return json_response(resp)

    store, product, supplier = device.store, device.product, device.supplier
    if not store:
        resp['status'], resp['alert'] = 0, u'该设备未找到餐厅，请联系管理员'
        return json_response(resp)
    if device.guarantee in [-2, -1]:
        resp['status'], resp['alert'] = 0, u'设备没有保固状态，请联系管理员'
        return json_response(resp)
    if not product:
        resp['status'], resp['alert'] = 0, u'该设备未找到设备大类，请联系管理员'
        return json_response(resp)
    if not supplier:
        resp['status'], resp['alert'] = 0, u'该设备未找到供应商，请联系管理员'
        return json_response(resp)

    # 是否采购
    is_buy = int(data.get('is_buy', 0))
    if is_buy == 1: state = 2

    if loggend_user.head_type > 1:
        if not logo:
            resp['status'], resp['alert'] = 0, u'故障图片不得为空'
            return json_response(resp)
        # 当前一个设备未完成的时候后面一个无法叫修
        if Maintenance.objects.filter(device=cid, user=loggend_user, is_buy=is_buy,
                                      status__in=[0, 1, 3]).count() > 0 and not is_buy:
            resp['status'], resp['alert'] = 0, u'该设备有未接的维修单，无法重新叫修，请去我的修单里处理'
            return json_response(resp)

        # 获取Push数据
        ca = Call.objects.filter(name=product.name, brand=product.brand, city=store.city, model=product.model,
                                 head_type=device.head_type).first()

        if not ca:
            ca = Call.objects.filter(name=product.name, brand=product.brand, city=store.city,
                                     head_type=device.head_type).first()
            if not ca:
                resp['status'], resp['alert'] = 0, u'没有找到维修该设备的服务商，请联系管理员'
                return json_response(resp)
        company = ca.warranty_in if device.guarantee else ca.warranty_out1

        push = DB.push.find_one({'city': store.city, 'company': company, 'head_type': loggend_user.head_type},
                                {'provider': 1, 'area_manager': 1, 'manager': 1, 'hq': 1})
        if not push:
            resp['status'], resp['alert'] = 0, u'没有找到更上层的推送，请联系管理员'
            return json_response(resp)
        call_provider = DB.user.find_one({'_id': ObjectId(push['provider'])}, {'username': 1, 'name': 1})
        if not call_provider:
            resp['status'], resp['alert'] = 0, u'未找到维修工主管，请联系管理员'
            return json_response(resp)
        provider_manager, manager, hq = ["|".join(push.get(i, [])) for i in ['area_manager', 'manager', 'hq']]

        users = list(User.objects(__raw__={'city': store.city, 'company': company, 'category': '0', 'is_active': 1}))
    else:
        if not loggend_user.loc:
            resp['alert'] = u'无法定位当前位置，请联系管理员'
            return json_response(resp)
        company = ''
        for step in range(1, 20):
            users = list(User.objects(
                    __raw__={"loc": SON([("$near", loggend_user.loc), ("$maxDistance", 10 * step / 111.12)]),
                             'category': '0', 'is_active': 1, 'device_token': {'$ne': None}}))
            if len(users) > 0:
                break
    if len(users) > 0:
        # 推送短信规则
        send_time = now.strftime('%H:%M')

        maintenance = {
            'user': loggend_user.id,
            'store_name': store.name,
            'store': str(store.id),
            'address': store.address,
            'company': company,
            'product': device.name,
            'product_id': product.id,
            'supplier': supplier.name,
            'supplier_id': supplier.id,
            'area': store.area,
            'city': store.city,
            'loc': store.loc,
            'status': 0,
            'brand': product.brand.name,
            'head_type': loggend_user.head_type,
            'device': str(device.id),
            'no': device.no,
            'store_no': store.no,
            'logo': logo.split(',') if logo else [],
            'content': error,
            'error_code': eid,
            'create_time': dt.now(),
            'update_time': dt.now(),
            'members': [str(i.id) for i in users]
        }
        if loggend_user.head_type > 1:

            states = u'紧急' if int(state) == 1 else u'非紧急'
            mt = lambda x: dt.now() + datetime.timedelta(hours=x)

            send_counts = _send_count(loggend_user.head_type)
            maintenance['code'] = send_counts
            maintenance['state'] = int(state)
            maintenance['is_buy'] = is_buy
            maintenance['guarantee'] = device.guarantee
            maintenance['must_time'] = mt(must_time)
            maintenance['work_range'] = fix_time
            maintenance['must_range'] = must_time
            mtceid = Maintenance(**maintenance).save()
            # mtceid = DB.maintenance.save(maintenance)
            REDIS.hset('call_pool', str(mtceid.id),
                       "{}|{}|0|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(time.time(), states, send_counts,
                                                                               send_time,
                                                                               SERVICE_COMPANY.get(store.head_type),
                                                                               store.name, store.no, device.name, error,
                                                                               send_time, call_provider['name'],
                                                                               call_provider['username'],
                                                                               provider_manager, manager, hq))

        else:

            maintenance['code'] = _send_count(loggend_user.head_type)
            maintenance['guarantee'] = device.guarantee
            maintenance['start_time'] = pf8(start_time)
            maintenance['end_time'] = pf8(end_time)
            # mtceid = DB.maintenance.save(maintenance)
            mtceid = Maintenance(**maintenance).save()

            # 新增报价单
            Bill(**{
                'opt_user': loggend_user, 'maintenance': mtceid.id,
                'supplier': device.supplier, 'product': device.product,
                'total': 0, 'analysis': '', 'measures': '', 'status': -2,
                'state': 1, 'device': device
            }).save()

        if MaintenanceHistory.objects(maintenances=mtceid).count():
            resp['status'], resp['alert'] = 0, u'订单已经存在维修历史, 请联系管理员'
            return json_response(resp)

        mhid = MaintenanceHistory(**{
            'user': loggend_user,
            'maintenances': [mtceid],
        }).save()

        mc_data = {
            'user': loggend_user,
            'histories': [mhid],
            'store_name': store.name,
            'store': str(store.id),
            'store_no': store.no,
            'address': store.address,
        }

        if loggend_user.head_type > 1:
            mc_data['state'] = maintenance.get('state')
            mc_data['must_time'] = maintenance.get('must_time')

        mcid = MaintenanceCollection(**mc_data).save()

        title = PUSH0.format(store.name, product.name)
        sdata = {'type': 0, 'oid': str(mtceid.id), 'cid': str(mcid.id)}

        resp['info']['id'] = str(mtceid.id)

        for user in users:
            PushHistory(**{'maintenance': str(mtceid.id), 'opt_user': loggend_user.id, 'user': user.id, 'data': sdata,
                           'title': title, 'head_type': 0, 'active': 0}).save()

        for member in mtceid.users():
            push_message(member.id, title, sdata)
        resp['alert'] = u'派单成功！请耐心等候维修工回复吧！'
    else:
        resp['status'], resp['alert'] = 0, u'该区域未找到相应的维修人员'
    resp['info']['count'] = len(users)
    return json_response(resp)


@login_required('1')
def update_restaurant(request, oid):
    """  修改预览餐厅，get预览，post修改   5625ef6c0da60b032da34605(连锁版)

    :uri: /api/v1/merchant/update_restaurant/<oid:唯一标识如:5624c4f10da60b062399b1f5>
    :get params:
        * cid:餐厅id,从选择中传入需要传入该id:5621b9b00da60b02862e21a4
        * return
    :post params:
        * cid:餐厅id,从选择中传入需要传入该id
        * return  
    :return:
        * rid 唯一标识<oid:不需要传入>
        * uid 流水号  <uid:不允许传入>
        * area 位置 "城市 区"
        * address 地址
        * name 名称
        * no 餐厅编号
        * delivery_time 交店时间
        * opening_time  开业时间
        * tel 固定电话
        * fax 传真
        * store_manager 门店经理
        * phone         手机号码
        * loc           坐标 x,y 中间‘,’隔开
    """
    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    if not user.head_type:
        resp['status'], resp['alert'] = 0, u'没有权限，请联系管理员'
        return json_response(resp)
    data = get_json_data(request) or request.POST.dict()
    logger.info(data)
    cid = data.get('cid') or request.GET.get('cid')
    # if not cid:
    #    resp['alert'], resp['status'] = u'请从餐厅中选择，请勿新增', 0 
    #    return json_response(resp)
    cstore = Store.objects.filter(id=ObjectId(cid)).first()
    rstore = Store.objects.filter(rid=oid).first()
    store = cstore or rstore
    if request.method == 'GET':
        resp['info'] = {
            'rid': oid,
            'uid': store.uid if store else '',
            'area': store.area if store else '',
            'address': store.address if store else '',
            'name': store.name if store else '',
            'no': store.no if store else '',
            'delivery_time': store.delivery_time if store else '',
            'opening_time': store.opening_time if store else '',
            'tel': store.tel if store else '',
            'fax': store.fax if store else '',
            'store_manager': store.store_manager if store else '',
            'phone': store.phone if store else '',
            'loc': store.loc if store else '',
            'city': store.city if store else '',
            'district': store.district if store else '',
            'id': store.id if store else ''
        }
        return json_response(resp)
    if not store: store = Store()

    keys = ['oid', 'area', 'address', 'name', 'no', 'delivery_time', 'opening_time', 'tel', 'fax', 'store_manager',
            'phone', 'loc']
    uid = "{}{}".format(data.get('opening_time') or store.opening_time, data.get('no') or store.no)

    if rstore:
        rstore.rid = ''
        rstore.save()

    setattr(store, 'uid', uid)
    if store.rid:
        setattr(store, 'old_rid', store.rid)
    setattr(store, 'rid', oid)
    for key in keys:
        if data.get(key):
            if key == 'area':
                city, district = [i.strip() for i in data['area'].split(' ')]
                setattr(store, 'city', city)
                setattr(store, 'district', district)
            elif key == 'loc':
                loc = [float(i) for i in data['loc'].split(',')]
                setattr(store, 'loc', loc)
            else:
                setattr(store, key, data.get(key))
    setattr(store, 'head_type', user.head_type)
    store.save()
    resp['info'] = {'id': str(store.id)}
    if DB.store.find({'rid': oid, '_id': {'$ne': store.id}}).count() > 0:
        DB.store.update({'rid': oid, '_id': {'$ne': store.id}}, {'$set': {'rid': ''}}, upsert=True, multi=True)
    return json_response(resp)


@login_required('1')
def update_assets(request, oid):
    """  修改预览资产，get预览，post修改（连锁版）

    :uri: /api/v1/merchant/update_assets/<oid:唯一标识如:5624c5010da60b062399b1f6> 
    :get params:
        * cid:设备大类id,从选择中传入需要传入该id 
        * return 
    :post params:
        * store 餐厅的id
        * cid:设备id,从选择中传入需要传入该id
        * return 
    :return:
        * category 设备类型(厨房设备，IT设备， 工程设备)
        * name 设备名称
        * brand 品牌
        * model 型号
        * specifications 规格
        * psnumber 生产序列号
        * manufacturer 制造厂商
        * provider 供应厂商
        * scrap_time 过保日期
        * logo 图片, ','隔开
    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    if not user.head_type:
        resp['status'], resp['alert'] = 0, u'没有权限，请联系管理员'
        return json_response(resp)
    data = get_json_data(request) or request.POST.dict()
    cid = data.get('cid') or request.GET.get('cid')
    logger.info(data)
    if data.get('name'):
        data['initial'] = get_pinyin_initials(data.get('name'))
    keyc = ['category', 'name', 'brand', 'model', 'specifications', 'initial']
    keys = ['store', 'uid', 'category', 'name', 'brand', 'model', 'specifications', 'psnumber', 'manufacturer',
            'provider', 'scrap_time', 'logo']

    rbk = Device.objects.filter(rid=oid).first()
    cbk = Product.objects.filter(id=ObjectId(cid)).first()
    if not cbk:
        resp['status'], resp['alert'] = 0, u'未找到该设备大类'
        return json_response(resp)
    device = rbk
    if request.method == 'GET':
        resp['info'] = {
            'rid': oid,
            'uid': device.uid if device else '',
            'category': device.category if device else '',
            'name': device.name if device else '',
            'brand': device.brand if device else '',
            'model': device.model if device else '',
            'specifications': device.specifications if device else '',
            'psnumber': device.psnumber if device else '',
            'manufacturer': device.manufacturer if device else '',
            'provider': device.provider if device else '',
            'scrap_time': device.scrap_time if device else '',
            'logo': device.logo if device else ''
        }
        return json_response(resp)

    data['uid'] = "{}{}".format(DEVICE_TYPE.get(data.get('category')), dt.now().strftime('%Y%m%d%H%M%S'))

    if not device: device = Device()

    setattr(device, 'rid', oid)
    setattr(device, 'uid', data['uid'])
    if cbk:
        setattr(device, 'efcategory', cbk.efcategory)
        setattr(device, 'ecategory', cbk.ecategory)
        setattr(device, 'product', cbk)

    # if data.get('name') and not Product.objects.filter(name=data.get('name')).first():
    #    Product(**dict([(i, data.get(i)) for i in keyc])).save()
    for key in keys:
        if key == 'logo' and data.get('logo'):
            data['logo'] = data['logo'].split(',')
        if data.get(key):
            if key == 'brand':
                brand = Brand.objects.filter(name=data.get('brand')).first()
                if not brand:
                    resp['status'], resp['alert'] = 0, u'未找到品牌类型'
                    return json_response(resp)

            # if key == 'psnumber':
            #    query = {'psnumber':data.get('psnumber')}
            #    if device: query['id__ne'] = device.id
            #    if Device.objects(__raw__=query).first():
            #        resp['status'], resp['alert'] = 0, u'生产序列号不得重复'
            #        return json_response(resp)

            if key == 'provider':
                provider_id = Supplier.objects.filter(name=data.get('provider')).first()
                if provider_id:
                    setattr(device, 'supplier', provider_id)
                else:
                    resp['status'], resp['alert'] = 0, u'未找到供应商'
                    return json_response(resp)
            elif key == 'store':
                store_id = Store.objects.filter(id=ObjectId(data[key])).first()
                if store_id:
                    setattr(device, 'store', store_id)
                    if store_id.rid == oid and store_id.old_rid:
                        setattr(store_id, 'rid', store_id.old_rid)
                        store_id.save()
                else:
                    resp['status'], resp['alert'] = 0, u'未找到门店'
                    return json_response(resp)
            elif key == 'scrap_time':
                setattr(device, 'expiration_date', data.get(key))
            else:
                setattr(device, key, data.get(key))

    setattr(device, 'head_type', user.head_type)
    device.save()
    resp['info']['id'] = str(device.id)
    return json_response(resp)


@login_required('1')
def update_qrcode(request, rid):
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    type = data['type']
    id = data['id']
    model = {'store': Store, 'device': Device}.get(type)

    if not model or not id:
        resp['alert'] = u'参数错误'
        return json_response(resp)

    if getattr(model, 'objects')(rid=rid).count():
        resp['alert'] = u'二维码已经存在, 请使用其他的二维码替换'
        return json_response(resp)

    instance = getattr(model, 'objects').get(id=ObjectId(id))

    if type == 'store':
        target_id = str(instance.id)
    elif type == 'device':
        target_id = str(instance.store.id)

    if str(user.store_id) != target_id:
        resp['alert'] = u'此二维码超出本店范围'
        return json_response(resp)

    instance.old_rid = instance.rid
    instance.rid = rid
    instance.update_time = dt.now()
    instance.save()

    resp['status'] = 1
    return json_response(resp)


@login_required('1')
def update_device(request, oid):
    """  修改预览资产，get预览，post修改（连锁版）

    :uri: /api/v1/merchant/update_assets/<oid:唯一标识如:5624c5010da60b062399b1f6>
    :get params:
        * cid:设备大类id,从选择中传入需要传入该id
        * return
    :post params:
        * store 餐厅的id
        * cid:设备id,从选择中传入需要传入该id
        * return
    :return:
        * category 设备类型(厨房设备，IT设备， 工程设备)
        * name 设备名称
        * brand 品牌
        * model 型号
        * specifications 规格
        * psnumber 生产序列号
        * manufacturer 制造厂商
        * provider 供应厂商
        * scrap_time 过保日期
        * logo 图片, ','隔开
    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    if not user.head_type:
        resp['status'], resp['alert'] = 0, u'没有权限，请联系管理员'
        return json_response(resp)
    data = get_json_data(request) or request.POST.dict()
    cid = data.get('cid') or request.GET.get('cid')
    logger.info(data)
    if data.get('name'):
        data['initial'] = get_pinyin_initials(data.get('name'))
    keyc = ['category', 'name', 'brand', 'model', 'specifications', 'initial']
    keys = ['store', 'uid', 'category', 'name', 'brand', 'model', 'specifications', 'psnumber', 'manufacturer',
            'provider', 'scrap_time', 'logo', 'supplier']

    rbk = Device.objects.filter(rid=oid).first()
    cbk = Product.objects.filter(id=ObjectId(cid)).first()
    if not cbk:
        resp['status'], resp['alert'] = 0, u'未找到该设备大类'
        return json_response(resp)
    device = rbk
    if request.method == 'GET':
        resp['info'] = {
            'rid': oid,
            'uid': device.uid if device else '',
            'category': device.category if device else '',
            'name': device.name if device else '',
            'brand': device.brand if device else '',
            'model': device.model if device else '',
            'specifications': device.specifications if device else '',
            'psnumber': device.psnumber if device else '',
            'manufacturer': device.manufacturer if device else '',
            'provider': device.provider if device else '',
            'scrap_time': device.scrap_time if device else '',
            'logo': device.logo if device else ''
        }
        return json_response(resp)

    data['uid'] = "{}{}".format(DEVICE_TYPE.get(data.get('category')), dt.now().strftime('%Y%m%d%H%M%S'))

    if not device: device = Device()

    setattr(device, 'rid', oid)
    setattr(device, 'uid', data['uid'])
    if cbk:
        setattr(device, 'efcategory', cbk.efcategory)
        setattr(device, 'ecategory', cbk.ecategory)
        setattr(device, 'product', cbk)

    # if data.get('name') and not Product.objects.filter(name=data.get('name')).first():
    #    Product(**dict([(i, data.get(i)) for i in keyc])).save()
    for key in keys:
        if key == 'logo' and data.get('logo'):
            data['logo'] = data['logo'].split(',')
        if data.get(key):
            if key == 'brand':
                brand = Brand.objects.filter(name=data.get('brand')).first()
                if not brand:
                    resp['status'], resp['alert'] = 0, u'未找到品牌类型'
                    return json_response(resp)

            # if key == 'psnumber':
            #    query = {'psnumber':data.get('psnumber')}
            #    if device: query['id__ne'] = device.id
            #    if Device.objects(__raw__=query).first():
            #        resp['status'], resp['alert'] = 0, u'生产序列号不得重复'
            #        return json_response(resp)

            if key == 'supplier':
                supplier_id = Supplier.objects.filter(name=data.get('supplier')).first()
                if supplier_id:
                    setattr(device, 'supplier', supplier_id)
                else:
                    resp['status'], resp['alert'] = 0, u'未找到供应商'
                    return json_response(resp)
            elif key == 'store':
                store_id = Store.objects.filter(id=ObjectId(data[key])).first()
                if store_id:
                    setattr(device, 'store', store_id)
                    if store_id.rid == oid and store_id.old_rid:
                        setattr(store_id, 'rid', store_id.old_rid)
                        store_id.save()
                else:
                    resp['status'], resp['alert'] = 0, u'未找到门店'
                    return json_response(resp)
            elif key == 'scrap_time':
                setattr(device, 'expiration_date', data.get(key))
            else:
                setattr(device, key, data.get(key))

    setattr(device, 'head_type', user.head_type)
    device.save()
    resp['info']['id'] = str(device.id)
    return json_response(resp)


@login_required('1')
def delete_device(request, rid):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    if not user.head_type:
        resp['status'], resp['alert'] = 0, u'没有权限，请联系管理员'
        return json_response(resp)
    data = get_json_data(request) or request.POST.dict()

    if request.method == 'DELETE':
        try:
            device = Device.objects.get(rid=rid)
        except:
            resp['status'], resp['alert'] = 0, u'设备不存在'
            return json_response(resp)

        if str(device.store.id) != user.store_id:
            resp['status'], resp['alert'] = 0, u'不是该店店员, 无法清空设备'
            return json_response(resp)

        print device.delete()
        return json_response(resp)


@login_required('1')
def confirm_bill(request, oid):
    """  确认报价单 (餐厅适用标准版和连锁版)

    :uri: /api/v1/merchant/confirm_bill/<oid:叫修id>
    :POST:
        * cid          报价单id（有则确认单个报价单，无则确认全部）
        * stauts       状态1为同意，-1为不同意
    """
    resp = {'status': 0, 'info': {}, 'alert': ''}
    user = get_user(request)
    data = get_json_data(request) or request.POST.dict()
    cid, status = [data.get(i) for i in ['cid', 'status']]
    mtce = Maintenance.objects.get(id=ObjectId(oid), user=user)
    query = {'maintenance': ObjectId(oid)}
    if cid: query['_id'] = ObjectId(cid)
    bills = Bill.objects(__raw__=query)
    msg = ''
    for bill in bills:
        status = int(status)
        setattr(bill, 'status', status)
        if status == -1:
            msg = u'餐厅拒绝了您的工单'
            bill.pay_status = 0
            bill.close_time = dt.now()
            bill.confirm_time = dt.now()
        else:
            msg = u'餐厅同意了您的工单'
            bill.pay_status = 1
            bill.confirm_time = dt.now()
        bill.save()
    REDIS.hdel('confirm_pool', oid)
    resp['status'] = 1
    sdata = {'type': 17, 'oid': oid, 'cid': cid, 'sub_type': status}
    push_message(mtce.grab_user.id, msg, sdata)
    return json_response(resp)


@login_required('1')
def delete_bill(request, oid):
    """  删除报价单 (餐厅适用标准版和连锁版)

    :uri: /api/v1/merchant/delete_bill/<oid:叫修id>
    :POST:
        * cid          报价单id必填
    """
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    cid = data.get('cid')
    user = get_user(request)
    mtce = Maintenance.objects.get(id=ObjectId(oid), user=user)
    if cid:
        Bill.objects.filter(maintenance=mtce, opt_user=user, id=ObjectId(cid)).delete()
    if not Bill.objects.filter(maintenance=mtce).count():
        mtce.status = -1
        mtce.save()
    resp['status'] = 1
    return json_response(resp)


@login_required('1')
def add_bill(request, oid):
    """  增加报价单 (餐厅适用标准版和连锁版)

    :uri: /api/v1/merchant/add_bill/<oid:叫修id>
    :POST:
        * cid          报价单id存在则是编辑
        * device       设备的id(必填，用于多工单报表, 从设备列表中增加)
    """
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    cid, device = [data.get(i) for i in ['cid', 'device']]
    user = get_user(request)
    mtce = Maintenance.objects.get(id=ObjectId(oid), user=user)
    if not device:
        resp['alert'] = u'设备不得为空'
        return json_response(resp)

    device = Device.objects.get(id=ObjectId(device))
    if cid:
        bill = Bill.objects.get(id=ObjectId(cid), opt_user=user)
    else:
        bill = Bill()
    item = {
        'opt_user': mtce.user, 'user': mtce.grab_user, 'maintenance': mtce,
        'supplier': device.supplier, 'product': device.product,
        'total': 0, 'analysis': '', 'measures': '', 'status': -2, 'state': 1, 'device': device
    }
    for k, v in item.iteritems():
        setattr(bill, k, v)
    bill.save()
    resp['status'], resp['alert'] = 1, u'增加工单成功'
    if mtce.grab_user:
        push_message(mtce.grab_user.id, PUSH15, {
            'type': 15,
            'oid': cid,
            'cid': str(bill.id),
            'name': user.name,
            'product': device.name
        })
    if mtce.status in [5, -1]:
        mtce.status = 3
        mtce.save()
    resp['info']['id'] = str(bill.id)
    return json_response(resp)


@login_required('1')
def call_history(request, oid):
    """  叫修历史 维修进程 (适用标准版和连锁版)

    :uri: /api/v1/merchant/call_history/<oid:叫修id>
    :return:
        * api/v1/merchant/maintenances 请参考
        * 连锁版
            * 在有人接单的情况下会显示，只在接受到接单推送之后刷新当前页面获取到下面数据并弹出接单弹窗：
            * grab_id 接单人id
            * grab_user_name 接单人名称
            * grab_user_logo 接单人头像
            * grab_come_time 接单人预计达到时间
            * grab_company 接单人公司
            * push_count 通知多少名维修工
            * push_count2 通知服务商区域主管 连锁版
            * push_count3 通知汉堡王区域主管 连锁版
            * push_count4 通知汉堡王总部    连锁版
            * reset_fixed 1为返修 
            * reset_fixed == 1:fix_name=返修人名
            * reset_fixed == 1:fix_prev 上一个返修
            * reset_fixed == 1:fix_next 下一个返修
        *标准版
            * no 设备序列号
            * pic 维修品图片
            * logo 头像 地图上的显示的头像
            * create_time 下单时间
            * area 维修区域 
            * address 维修地址
            * store 餐厅名称
            * store_no 餐厅编号
            * store_id 餐厅的id
            * store_logo logo 如汉堡王logo
            * company 公司
            * company_logo 商户公司Logo
            * loc 坐标[x,y]
            * bk(device) 设备id
            * count 完成了多数单
            * push_count 推送多少人
            * charge 人工费
            * home_fee 上门费
            * status (4,5,6,7为连锁版状态标准版无用，标准版其他状态请使用bills status and pay_status)
                维修单状态 
                -1：取消 0：新维修单 1：维修员确认(维修员抢单) 
                2：商家确认维修单相当于整个流程走完 
                3：到店 4：维修失败 5:已经完成未确认 6:为暂停 7:报价维修（标准版） 
            * mobile 发起人的手机
            * name 维修员名称  只有在状态为2的时候有
            * distance 距离 只有在状态为2的时候有

            * start_time    商家要求到店时间 起始
            * end_time      商家要求到店时间 结束
            * single_time   接单时间  抢单时间
            * come_time     预计到店时间
            * create_time   报修时间  

            * target_user_id     接单人的id
            * target_user_mobile 接单的手机
            * target_user_name   接单人的名称
            * target_user_logo   接单人的logo
            * target_company     接单人的公司
            * bills [{
                            *下面是修单明细（bill字段），标准版进程多工单请从这里循环生成,默认bill当无工单时候bill为设备信息
                                * id bill id
                                * pic 报修的故障图片 list
                                * repair_pic 维修员提交的 list 
                                * other_message 服务商其他建议
                                * description 故障描述
                                * quality 1为保修期内 0为保修期外
                                * odm odm号
                                * product  设备名称
                                * product_code  设备序列号
                                * error_code error_code
                                * supplier 供应商名称
                                * supplier_id 供应商id
                                * device 设备id
                                * guarantee 0为保固外 1为保固内 -1未知
                                * brand 品牌
                                * spare [{'name':配件名称, 'price':配件价格, 'count':配件数, 'total':配件总价, 'status':1 为保内 0为非保, 
                                        'category':1为自然 0为人为,'no':编号, 'base_price':原本价格}],
                                * spare_total 配件总价
                                * labor 人工费
                                * labor_hour 工时 float
                                * total 总价
                                * analysis 故障分析
                                * measures 故障措施
                                * reason 错误描述
                                * content 描述
                                * others 其他费用 list(dict('msg':u'描述', 'total':u'金额’))
                                * offer_time 报价时间
                                * pay_status 付款状态 1为已经付款0为未付款
                                * work_time 预计完成时间
                                * confirm_time 确认完成时间
                                * close_time 结束完成时间maintenace.status==2 -> 24 - (now-close_time).hours
                                * countdown_time 维修倒计时时间
                                * status 报价单状态 1为确认（完成） 0为未确认(未完成) -1为拒绝 -2餐厅提交报价单 维修工未报价(维修员未提交坐标，为报价)
                                * 状态转换描

                                    * OrderStatus (叫修状态)
                                    * BillStatus  (设备维修状态)
                                    * PayStatus   (支付状态)

                                    * 新维修单
                                    * OrderStatus = 0 (新维修单)
                                    * BillStatus = 0 (未确认)
                                    * PayStatus  =0  (未付款)

                                    * 维修单被接
                                    * OrderStatus = 1 (维修单被接)
                                    * BillStatus = 0 (未确认)
                                    * PayStatus  =0  (未付款)

                                    * 维修单被接(维修员要去提交这个工单,用于多工单，维修员在没有填写第一个工单情况下，
                                                去增加另外一个工单签到)
                                    * OrderStatus = 3 (因为提交的时候回提交坐标，自动签到了)
                                    * BillStatus  = -2 (新工单)
                                    * PayStatus   = 0 (未付款) 

                                    * 填写报价单
                                    * OrderStatus = 3 (因为提交的时候回提交坐标，自动签到了)
                                    * BillStatus  = 0 (未确认)
                                    * PayStatus   = 0 (未付款)

                                    * 继续维修(餐厅确认工单)
                                        OrderStatus = 3 
                                        BillStatus  = 1 (确认工单)  已status为标准
                                        BIllState   = 0 
                                        PayStatus   = 1 (已经付款,付款暂时不做默认为已经付款)
                                    * 不继续维修(餐厅拒绝工单)
                                        OrderStatus  = 3
                                        BillStatus   = -1 (拒绝) 
                                        BIllState    = -1 
                                        PayStatus    = 0 (未付款)
                                    * 维修工结束维修
                                        OrderStatus  = 5(全部结束)
                                        BillStatus   = 不变
                                        BIllState    = 1 工单结束状态
                                        PayStatus    = 不变
                                    * 餐厅确认完成
                                        OrderStatus  = 2(全部结束)
                                        BillStatus   = 不变
                                        BIllState    = 2 工单餐厅确认完成状态
                                        PayStatus    = 不变



    """

    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    mt = Maintenance.objects.filter(id=ObjectId(oid), user=user).first()

    if not mt:
        resp['alert'] = u'该叫修单不存在'
        return json_response(resp)

    if user.head_type > 1:
        detail = mt.get_result()
        detail['push_count2'] = PushHistory.objects.filter(maintenance=oid, category=2).count()
        detail['push_count3'] = PushHistory.objects.filter(maintenance=oid, category=3).count()
        detail['push_count4'] = PushHistory.objects.filter(maintenance=oid, category=4).count()
    else:
        detail = mt.get_result1()
    detail['push_count'] = len(mt.members)

    resp['status'], resp['info'] = 1, detail
    return json_response(resp)


@login_required('1')
def call_quit(request, oid):
    """  取消叫修(适用标准版和连锁版)

    :uri: /api/v1/merchant/call_quit/<oid>
    :post params:
        * content 取消理由（暂不需要该功能）
    """

    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    mtce = Maintenance.objects.filter(id=ObjectId(oid), status__in=[0, 1]).first()
    content = data.get('content')

    if mtce:
        REDIS.hdel('call_poll', oid)
        REDIS.hdel('control_pool', oid)
        item = {'update_time': dt.now(), 'status': -1, 'quit_content': content}
        for k, v in item.iteritems():
            setattr(mtce, k, v)
        mtce.save()

        resp['status'], resp['alert'] = 1, u'取消成功'
        title = PUSH6.format(mtce.title)
        sdata = {'type': 6, 'oid': str(oid)}

        for pt in mtce.users():
            push_message(pt.id, title, sdata)
    else:
        resp['alert'] = u'该叫修无法取消'
        return json_response(resp)
    return json_response(resp)


@login_required('1')
def call_repeat(request, oid):
    """  重新报修(适用标准版和连锁版)

    :uri: /api/v1/merchant/call_repeat/<oid> 维修单的id

    """
    user = get_user(request)
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    mtce = Maintenance.objects.filter(id=ObjectId(oid), user=user, status=0).first()
    if mtce:
        title = PUSH0.format(mtce.store_name, mtce.product)
        sdata = {'type': 0, 'id': oid}
        resp['status'], resp['alert'] = 1, u'重新发送维修单成功，请耐心等候！'
        mtce.update_time = dt.now()
        mtce.create_time = dt.now()
        mtce.save()
        if mtce.head_type > 1:
            content = REDIS.hget('call_pool', oid)
            if content:
                befor_time, states, head_type, send_counts, send_time, company, store_name, store_no, name, error, recive_time, provider, provider_mobile, provider_manager, provider_manager_mobile, manager, manager_mobile, hq, hq_mobile = content.split(
                        '|')
                REDIS.hset('call_pool', oid,
                           "{}|{}|0|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(time.time(), states,
                                                                                            send_counts, send_time,
                                                                                            company, store_name,
                                                                                            store_no, name, error,
                                                                                            send_time, provider,
                                                                                            provider_mobile,
                                                                                            provider_manager,
                                                                                            provider_manager_mobile,
                                                                                            manager, manager_mobile, hq,
                                                                                            hq_mobile))

        for pt in mtce.users():
            push_message(pt.id, title, sdata)
    else:
        resp['alert'] = u'没有该修单，或者该修单状态已经改变'
    return json_response(resp)


@login_required('1')
def maintenances(request):
    """  维修列表

    :uri: /api/v1/merchant/maintenances
    :POST params:
        * p 当前多少页，默认第一页，一页20条
    :return:
        * 标准版数据结构:
            请看:/api/v1/merchant/call_history/<oid:叫修id> 
        * 连锁版的数据结构
        * no 设备序列号
        * pic 维修品图片
        * logo 头像 地图上的显示的头像
        * product 维修品名称
        * product_id 维修品大类id
        * supplier 供应商
        * supplier_id 供应商id 
        * create_time 下单时间
        * area 维修区域 
        * address 维修地址
        * guarantee 0为保修外 1为保修内 -1未知
        * store_logo logo 如汉堡王logo
        * company 公司
        * company_logo 商户公司Logo
        * loc 坐标[x,y]
        * bk(device) 设备id
        * count 完成了多数单
        * push_count 推送多少人
        * status 
            维修单状态 -1：取消 0：新维修单 1：维修员确认 2：商家确认维修单相当于整个流程走完 3：到店 4：维修失败 5:已经完成未确认
            6:为暂停
        * mobile 发起人的手机
        * name 维修员名称  只有在状态为2的时候有
        * distance 距离 只有在状态为2的时候有

        * must_time    商家要求到店时间
        * single_time  接单时间  设计中1
        * arrival_time 到店扫码时间 设计中2如果没有则取target_come_time
        * target_come_time 接单人预计达到时间
        * work_time 完成时间
        * now_time 当前服务器时间
        * create_time 报修时间

        * target_user_id     接单人的id
        * target_user_mobile 接单的手机
        * target_user_name   接单人的名称
        * target_user_logo   接单人的logo
        * target_company     接单人的公司

        * stop         是否暂停 -1是申请暂停 0是确认暂停 -2是拒绝暂停
        * stop_content 暂停原因手工填写
        * stop_reason 暂停原因选择
        * stop_day 预计下次到店时间
        * stop_work_time 预计重新维修完成时间
        * is_buy 是否采购， 1为采购 0为不是采购
        * reset_fixed 1为返修 0为不返修
        * reset_fixed 1为返修 
        * reset_fixed == 1:fix_name=返修人名
        * reset_fixed == 1:fix_prev 上一个返修
        * reset_fixed == 1:fix_next 下一个返修
        * confirm_time 确认完成时间
        * close_time 结束完成时间maintenace.status==2 -> 24 - (now-close_time).hours
        * countdown_time 维修倒计时时间


    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    p = int(data.get('p', 1))
    # res = Maintenance.objects((Q(be_reset_fixed__ne=1) | Q(is_collect=1)) & Q(collected__ne=1) & Q(user=user)).order_by(
    #         '-create_time').skip((p - 1) * 20).limit(20)
    # result = []
    # for r in res:
    #     if r.head_type == 1:
    #         detail = r.get_result1()
    #     else:
    #         detail = r.get_result(0)
    #     detail['push_count'] = PushHistory.objects.filter(maintenance=str(r['id'])).count()
    #     result.append(detail)
    # resp['info']['results'] = result
    # return json_response(resp)

    mc = MaintenanceCollection.objects(user=user).order_by('-create_time').skip((p - 1) * 20).limit(20)
    collections = [collection.get_result() for collection in mc]
    resp['info']['results'] = collections
    return json_response(resp)


@login_required('1')
def maintenance(request, oid):
    """  维修详细

    :uri: /api/v1/merchant/maintenance/<oid>
    :result:
        * no 设备序列号
        * pic 维修品图片
        * logo 图像
        * product 维修品名称
        * product_id 维修费id
        * supplier 供应商
        * supplier_id 供应商id
        * create_time 下单时间
        * area 维修地址
        * company 公司
        * store_logo logo 如汉堡王logo
        * loc 坐标[x,y]
        * bk  (device) 设备id
        * count 完成了多数单
        * status 维修单状态 -1：取消 0：新维修单 1：确认接单 2：已经完成   3:到店  4:维修失败 5:已经完成未确认
        * mobile 发起人的手机号码
        * must_time 到店时间
        * name 维修员名称   只有在状态为2的时候有
        * distance 距离    只有在状态为2的时候有
        * target_user_id 接单人的id
        * target_user_mobile 接单的手机
        * target_user_name  接单人的名称
        * target_user_logo 接单人的logo
        * target_come_time 接单人预计达到时间
        * target_company 接单人的公司
        * 下面是修单明细（bill字段）
        * quality 1为保修期内 0为保修期外
        * odm odm号
        * product_name  设备名称
        * product_code  设备序列号
        * error_code error_code
        * supplier 供应商名称
        * spare [{'name':配件名称, 'price':配件价格, 'count':配件数, 'total':配件总价, 'status':1 为保内 0为非保, 'category':1为自然 0为人为}],
        * spare_total 配件总价
        * labor 人工费
        * travel 茶旅费
        * total 总价
        * analysis 故障分析
        * measures 故障措施
        * reason 错误描述
        * content 描述
        * confirm_message 餐厅确认备注
        * other_message 服务商其他备注
        * manager_content  服务商主管意见
        * express 快递单号
        * repair_pic 维修照片
        * express_logo 快递单图片
        * later 存在为迟到
        * delayed 存在为延时
        * status -1为拒绝 1为确认
    """
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    maintenance = Maintenance.objects.get(user=user, id=ObjectId(oid))

    if maintenance.head_type > 1:
        resp['info'] = maintenance.get_result()
    else:
        resp['info'] = maintenance.get_result1()

    resp['info']['reset_fix_maintenances'] = maintenance.get_reset_fixes(user)

    return json_response(resp)


@login_required('1')
def confirm(request, oid):
    """  确认修单 (适用标准版和连锁版为兼容老版本)

    :uri: /api/v1/merchant/confirm/<oid> oid 为维修单id 
    :post:
        * head_type -1 为拒绝(现不改变工单状态，只有消息推送) 1为同意(默认同意为兼容)
        * receipt_logo 收货图片(默认为空为兼容老版本),','号隔开
        * cid 报价单的id（使用标准版）确认单个报价单情况为空则全部
        * message  备注


    """

    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()

    user = get_user(request)
    mtce = Maintenance.objects.get(id=ObjectId(oid), user=user)

    cid, receipt_logo, confirm_message = [data.get(i) for i in ['cid', 'receipt_logo', 'message']]
    head_type = data.get('head_type', '1')

    if mtce.head_type == 1:
        query = {'maintenance': ObjectId(oid), 'opt_user': user.id}
        cid = data.get('cid')
        if cid: query['_id'] = ObjectId(cid)
        bills = Bill.objects(__raw__=query)
        for bill in bills:
            bill.state = 2
            bill.receipt_logo = receipt_logo.split(',') if receipt_logo else []
            bill.confirm_time = dt.now()
            bill.confirm_message = confirm_message
            bill.save()
        if not Bill.objects.filter(maintenance=mtce, state__in=[0, 1], opt_user=user).first():
            setattr(mtce, 'status', 2)
            mtce.save()
    else:
        if head_type == '1' and mtce.status == 5: mtce.status = 2
        mtce.update_time = dt.now()
        mtce.save()
        bill = Bill.objects(__raw__={'maintenance': ObjectId(oid), 'opt_user': user.id}).first()
        if bill:
            bill.status = int(head_type)
            bill.receipt_logo = receipt_logo.split(',') if receipt_logo else []
            bill.confirm_time = dt.now()
            bill.confirm_message = confirm_message
            bill.save()
        REDIS.hdel('confirm_pool', oid)
    if head_type == '-1':
        msg = u'餐厅拒绝了您的工单'
    else:
        msg = u'餐厅同意了您的工单'
    resp['status'], resp['alert'] = 1, u'确认成功！维修员会接受到您的消息。'
    sdata = {'type': 17, 'oid': oid, 'cid': cid, 'sub_type': head_type}
    push_message(mtce.grab_user.id, msg, sdata)
    return json_response(resp)


@login_required('1')
def review(request, oid):
    """  点评

    :uri: /api/v1/merchant/review/<oid> oid 为维修单id
    :POST:
        * ask1 维修结果
        * ask2 维修技能
        * ask3 维修及时
        * ask4 服务态度
        * content 描述
    :GET return:
        * user_id 被点评人id
        * user_name 被点评人名称
        * opt_user_id 点评人id
        * opt_user_name 点评人名称
        * ask1 点评1
        * ask2 点评2
        * content 点评描述
    """

    resp = {'status': 0, 'info': {}, 'alert': ''}
    user = get_user(request)
    if request.method == 'POST':
        data = get_json_data(request) or request.POST.dict()
        ask1, ask2, ask3, ask4, content = [data.get(i) for i in ['ask1', 'ask2', 'ask3', 'ask4', 'content']]
        maintenance = DB.maintenance_users.find_one({'maintenance': ObjectId(oid), 'opt_user': user.id})
        if maintenance and ask1 and ask2 and content:
            Review(**{
                'opt_user': maintenance['opt_user'],
                'user': maintenance['user'],
                'maintenance': ObjectId(oid),
                'ask1': ask1,
                'ask2': ask2,
                'ask3': ask3,
                'ask4': ask4,
                'content': content
            }).save()
            resp['status'] = 1
            return json_response(resp)
    if DB.review.find_one({'maintenance': ObjectId(oid), 'opt_user': user.id}):
        review = Review.objects.get(maintenance=ObjectId(oid), opt_user=user.id)
        resp['info'], resp['status'] = review.detail(), 1
    return json_response(resp)


@login_required('1')
def reset_fixed(request, oid):
    """  返修

    :uri: /api/v1/merchant/reset_fixed/<oid> oid 为维修单id
    :POST:
        *
    """
    resp = {'status': 0, 'info': {}, 'alert': ''}
    user = get_user(request)
    data = get_json_data(request) or request.POST.dict()
    mtce = Maintenance.objects.get(id=ObjectId(oid), user=user)
    mh = MaintenanceHistory.objects.get(maintenances=mtce)

    if mtce.be_reset_fixed:
        resp['alert'] = u'该订单已经存在返修单, 无法再返修'
        return json_response(resp)

    for key in ['id', 'code', 'members']: delattr(mtce, key)
    data = {
        'status': 0,
        'members': [str(mtce.grab_user.id)],
        'code': _send_count(user.head_type),
        'reset_fixed': 1,
        'reset_maintenance': mtce.reset_maintenance if mtce.reset_maintenance else oid,
        'create_time': dt.now(), 'update_time': dt.now()
    }
    delattr(mtce, 'grab_user')
    for k, v in data.iteritems():
        setattr(mtce, k, v)
    resp['status'] = 1

    fix_id = mtce.save().id
    mh.maintenances.append(mtce)
    mh.save()

    resp['info']['id'] = fix_id

    Maintenance.objects(id=ObjectId(oid)).update(set__be_reset_fixed=1, set__status=7)
    return json_response(resp)


@login_required('1')
def collection(request, id):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)

    try:
        mtce = MaintenanceCollection.objects.get(id=ObjectId(id), user=user)
    except:
        resp['alert'] = u'订单合集不存在'
        return json_response(resp)

    resp['info'] = mtce.get_result()
    return json_response(resp)


@login_required('0')
def collect(request, id):
    """  合集
    维修工添加合集

    :uri: /api/v1/merchant/collect/<oid> oid 为维修单id
    :POST params:
    * type 1 为标准版:
        * cid       设备id 5621b9b00da60b02862e21e2
        * logo      故障图片 #https://www.baidu.com/img/bd_logo1.png
        * error     错误描述content
        * eid       错误描述id，从api/v1/merchant/fault获取，选择其他则为空
        * start_time   起始时间 20160414112300
        * end_time     结束时间 20160414112300

    * type > 1为连锁版:
        * cid       设备id 5621b9b00da60b02862e21e2
        * logo      故障图片 #https://www.baidu.com/img/bd_logo1.png
        * error     错误描述content    测试数据：content: error1, id: 55ee8d180da60b02aa8d7960, no: BK141114SH0001EQ
        * eid       错误描述id，从api/v1/merchant/fault获取，选择其他则为空
        * state     状态 1:紧急 2:一般 (当选择其他的时候允许人工选择紧急：1，和非紧急：2)，采购都未为非紧急
        * is_buy    1为采购 0为不是
    """
    resp = {'status': 0, 'info': {}, 'alert': ''}
    user = get_user(request)
    data = get_json_data(request) or request.POST.dict()
    # mtce = Maintenance.objects.get(id=ObjectId(oid))

    try:
        collection = MaintenanceCollection.objects.get(id=ObjectId(id), grab_users=user)
    except:
        resp['alert'] = u'该用户无法合并订单'
        return json_response(resp)

    mtce = collection.histories[0].maintenances[-1]

    if mtce.collect_maintenance:
        resp['alert'] = u'叫修单已经被添加到{}中, 此新订单无法与其合并'.format(mtce.collect_maintenance)
        return json_response(resp)

    if mtce.be_reset_fixed:
        resp['alert'] = u'被返修的订单无法添加合并订单'
        return json_response(resp)

    logo, error, cid, state, eid, start_time, end_time = [data.get(i) for i in
                                                          ['logo', 'error', 'cid', 'state',
                                                           'eid', 'start_time', 'end_time']]
    if eid:
        error_code = ErrorCode.objects.filter(id=ObjectId(eid)).first()
        if not error_code:
            resp['status'], resp['alert'] = 0, u'error code不得为空'
            return json_response(resp)
        error_content = error_code.get_result()
        state, must_time, fix_time = [error_content.get(i) for i in ['status', 'must_time', 'fix_time']]
    else:
        if state:
            state = int(state)
            if state not in [1, 2]:
                resp['status'], resp['alert'] = 0, u'叫修只有两个状态'
                return json_response(resp)

            must_time, fix_time = FIX_TIME[state]

    device = Device.objects.filter(id=ObjectId(cid), head_type=user.head_type).first()
    if not device:
        resp['status'], resp['alert'] = 0, u'没有找到该设备'
        return json_response(resp)

    store, product, supplier = device.store, device.product, device.supplier
    if not store:
        resp['status'], resp['alert'] = 0, u'该设备未找到餐厅，请联系管理员'
        return json_response(resp)
    if str(store.id) != mtce.store:
        resp['status'], resp['alert'] = 0, u'要合并的订单设备不是该餐厅的，请联系管理员'
        return json_response(resp)
    if device.guarantee in [-2, -1]:
        resp['status'], resp['alert'] = 0, u'设备没有保固状态，请联系管理员'
        return json_response(resp)
    if not product:
        resp['status'], resp['alert'] = 0, u'该设备未找到设备大类，请联系管理员'
        return json_response(resp)
    if not supplier:
        resp['status'], resp['alert'] = 0, u'该设备未找到供应商，请联系管理员'
        return json_response(resp)

    # 是否采购
    is_buy = int(data.get('is_buy', 0))
    if is_buy == 1: state = 2

    if user.head_type > 1:
        # if not logo:
        #     resp['status'], resp['alert'] = 0, u'故障图片不得为空'
        #     return json_response(resp)
        # 当前一个设备未完成的时候后面一个无法叫修
        if Maintenance.objects.filter(device=cid, user=user, is_buy=is_buy,
                                      status__in=[0, 1, 3]).count() > 0 and not is_buy:
            resp['status'], resp['alert'] = 0, u'该设备有未接的维修单，无法合并，请去我的修单里处理'
            return json_response(resp)

    oid = mtce.id
    for key in ['id', 'code', 'members', 'reset_fixed', 'reset_maintenance', 'be_reset_fixed']: delattr(mtce, key)
    data = {
        'status': 3,
        'members': [str(mtce.grab_user.id)] if mtce.grab_user else mtce.members,
        'code': _send_count(user.head_type),
        'collected': 1,
        'collect_maintenance': str(oid),
        'create_time': dt.now(),
        'update_time': dt.now(),

        'user': mtce.user,
        'grab_user': user,
        'product': device.name,
        'product_id': product,
        'supplier': supplier.name,
        'supplier_id': supplier,
        'guarantee': device.guarantee,
        'brand': product.brand.name,
        'device': str(device.id),
        'no': device.no,
        'logo': logo.split(',') if logo else [],
        'content': error,
        'error_code': eid,
    }

    for k, v in data.iteritems():
        setattr(mtce, k, v)

    if user.head_type > 1:
        mt = lambda x: dt.now() + datetime.timedelta(hours=x)
        mtce['state'] = int(state)
        mtce['is_buy'] = int(is_buy or 0)
        mtce['must_time'] = mt(must_time)
        mtce['work_range'] = fix_time
        mtce['must_range'] = must_time
        new_id = mtce.save().id
    else:
        mtce['start_time'] = pf8(start_time)
        mtce['end_time'] = pf8(end_time)
        new_id = mtce.save().id

        # # 新增报价单
        # Bill(**{
        #     'opt_user': user, 'maintenance': mtceid.id,
        #     'supplier': device.supplier, 'product': device.product,
        #     'total': 0, 'analysis': '', 'measures': '', 'status': -2,
        #     'state': 1, 'device': device
        # }).save()


    mhid = MaintenanceHistory(**{
        'user': mtce.user,
        'grab_users': [mtce.grab_user],
        'maintenances': [mtce],
    }).save()
    collection.histories.append(mhid)
    collection.save()

    resp['status'] = 1
    resp['info'] = collection.get_result()

    return json_response(resp)
