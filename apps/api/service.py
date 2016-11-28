# /user/bin/env python
# encoding:utf-8


import os
import time
import math
import traceback
import random
import json
from datetime import timedelta
from datetime import datetime as dt
from bson.objectid import ObjectId
from mongoengine import Q
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate
from apps.base.common import json_response, get_json_data, get_user
from apps.base.utils import distanceByLatLon
from apps.base.models import User, MaintenanceUsers, Bill, Maintenance, MaintenanceHistory, MaintenanceCollection, \
    Spare, Errors, Repair, Bconfig, Review, ErrorCode, BSpare, Member, Device, Charge, Store
from apps.base.messages import PUSH8, PUSH1, PUSH2, PUSH14, PUSH16, PUSH7
from apps.base.sms import send_sms
from apps.base.push import push_message
from apps.base.logger import getlogger
from apps.base.utils import login, distanceByLatLon, pf7, pf2, pf9, pf3
from apps.base.common import base_login_required as login_required
from settings import DB, DEBUG, HOST_NAME, ENV, REDIS, AREA_CONNECTOR, SERVICE_COMPANY, CHARGE

logger = getlogger(__name__)

'''
    test user:22222222222/000000
'''


@login_required('0')
def scan(request):
    """  签到->扫描店铺并传入商铺no(连锁版)

    :uri: /api/v1/service/scan

    :POST params:
        * no 设备的no  测试:5625ef6c0da60b032da34605    
        * type        1为标准 2为汉堡王 测试:2
    :return:
        * info -> status 1为正常 0为迟到
        * id 叫修单的id
 


 
    """

    resp = {'status': 0, 'info': {'status': 1}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    head_type, no = [data.get(i) for i in ['type', 'no']]
    user = get_user(request)
    if no and head_type:
        if head_type == '2':
            device = Device.objects.filter(rid=no).first()
            if not device:
                store = Store.objects.filter(rid=no).first()
                if not store:
                    resp['alert'] = u'该二维码不存在，请检查设备是否正确，或者去扫餐厅二维码!'
                    return json_response(resp)
            else:
                store = device.store
            mu = Maintenance.objects.filter(grab_user=user, store=str(store.id), status__in=[1, 6]).order_by(
                '-create_time').first()

            if mu:
                resp['status'] = 1
                resp['info']['id'] = str(mu.id)
                if mu.status == 1:
                    # 当晚上的单子的时候，迟到时间为必须到店时间
                    if mu.create_time.hour == 12 or mu.create_time.hour < 7:
                        if dt.now() > mu.must_time:
                            resp['info']['status'] = 0
                    else:
                        must_time = mu.must_time if mu.must_time > mu.come_time else mu.come_time
                        if dt.now() > must_time:
                            resp['info']['status'] = 0

                item = {'arrival_time': dt.now()}
                if mu.work_range > 0:
                    work_time = dt.now() + timedelta(hours=mu.work_range)
                    item['work_time'] = work_time
                if mu.status == 6:
                    REDIS.hdel('stop_poll', resp['info']['id'])
                    if dt.now() > mu.stop_day:
                        resp['info']['status'] = 0
                        item['stop_later'] = 1
                    item['stop_come_time'] = dt.now()
                item['status'] = 3
                for k, v in item.iteritems():
                    setattr(mu, k, v)
                mu.save()

                title = PUSH8.format(user.name)
                sdata = {'type': 8, 'oid': str(mu.id), 'cid': mu.collection_id}

                for member in mu.users():
                    push_message(member.id, title, sdata)
                # 取消迟到和扫码签到提醒
                content = REDIS.hget('control_pool', str(mu.id))
                if content:
                    befor_time3, code, grab_user_name, company_name, store_name, store_no, oid, opt_user_id, user_id, parent_user_id, come_time, come_time_status, work_time, work_time_status = content.split(
                        '|')
                    REDIS.hset('control_pool', oid,
                               '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(befor_time3, code, grab_user_name,
                                                                                  company_name, store_name, store_no,
                                                                                  oid, opt_user_id, user_id,
                                                                                  parent_user_id, come_time, 2,
                                                                                  work_time, work_time_status))
            else:
                resp['alert'] = u'无该叫修单'
    return json_response(resp)


@login_required('0')
def delayed(request, oid):
    """  填写延时原因 /api/v1/service/delayed/<oid> 判断手机当前时间大于商户要求必须到店时间

    :uri: /api/v1/service/delayed/<oid>

    :POST params: 
        * content 延时原因

    """
    resp = {'status': 0, 'info': {'status': 1}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    content = data.get('content')
    user = get_user(request)
    if not content:
        resp['alert'] = u'延时原因不得为空'
        return json_response(resp)
    mt = Maintenance.objects.filter(id=ObjectId(oid)).first()
    if not mt:
        resp['alert'] = u'该叫修单不存在'
        return json_response(resp)
    mt.delayed = content
    mt.save()
    resp['status'] = 1
    # 推送消息给主管
    for parent_user in mt.users():
        push_message(parent_user.id, u'{}师傅申请延时到店'.format(user.name), {
            'type': 22,
            'oid': oid,
            'company': SERVICE_COMPANY.get(mt.head_type),
            'store_name': mt.store_name,
            'store_no': mt.store_no,
            'msg': content,
            'will_time': pf3(mt.come_time),
            'must_time': pf3(mt.must_time),
            'cid': mt.collection_id,
        })
    return json_response(resp)


@login_required('0')
def later(request, oid):
    """  填写迟到原因 /api/v1/service/later/<oid> info -> status为0 时候需要填写

    :uri: /api/v1/service/later/<oid>

    :POST params: 
        * content 迟到原因
    :return:
        * info -> status 1为正常 0为迟到

    """

    resp = {'status': 0, 'info': {'status': 1}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    content = data.get('content')
    user = get_user(request)
    if not content:
        resp['alert'] = u'迟到原因不得为空'
        return json_response(resp)

    mt = Maintenance.objects.filter(id=ObjectId(oid), grab_user=user).first()
    if not mt:
        resp['alert'] = u'该叫修单不存在'
        return json_response(resp)
    mt.later = content
    mt.save()
    resp['status'] = 1
    # 推送消息给主管
    for parent_user in mt.users():
        push_message(parent_user.id, u'{}师傅未在规定时间到达'.format(user.name), {
            'type': 23,
            'oid': oid,
            'company': SERVICE_COMPANY.get(mt.head_type),
            'store_name': mt.store_name,
            'store_no': mt.store_no,
            'msg': content,
            'will_time': pf3(mt.come_time),
            'must_time': pf3(mt.must_time),
            'cid': mt.collection_id,
        })
    return json_response(resp)


@login_required('0')
def grabs(request):
    """  接单列表(head_type)
    :POST:
        * head_type(user profile中取) 1为标准 大于1为连锁(默认) 0为混合(暂无)

    :uri: /api/v1/service/grabs

    """
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.GET.dict()
    user = get_user(request)
    p = int(data.get('p', 1))
    head_type = int(data.get('head_type', 2))
    if head_type > 1:
        maintenances = Maintenance.objects(
            __raw__={'status': 0, 'head_type': {'$gt': 1}, 'members': {'$all': [str(user.id)]}}).order_by(
            '-create_time')
        results = [i.get_result() for i in maintenances]
    elif head_type == 1:
        maintenances = Maintenance.objects(
            __raw__={'status': 0, 'head_type': 1, 'members': {'$all': [str(user.id)]}}).order_by('-create_time')
        results = [i.get_result1() for i in maintenances]
    resp['info']['results'] = results
    return json_response(resp)


@login_required(['0', '2'])
def grab(request, oid):
    """  接单或者抢单(适用标准版和连锁版)

    :uri: /api/v1/service/grab/<oid>
    :post:
        * come_time 到点时间 ‘201509101400’ 年月日时分

    :return:
        * oid 推送给商家，用于确认抢单 
        * cid 推送给商家，用户确认抢单
    """

    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    if user.category == '2':
        maintenance = Maintenance.objects.filter(id=ObjectId(oid), status=0).first()
    else:
        maintenance = Maintenance.objects.filter(
            __raw__={'_id': ObjectId(oid), 'status': 0, 'members': {'$all': [str(user.id)]}}).first()
    if maintenance:
        come_time = data.get('come_time')
        if not come_time:
            resp['alert'] = u'请填写预计到店时间'
            return json_response(resp)
        ct = dt.strptime(come_time, '%Y%m%d%H%M')
        if ct < dt.now():
            resp['alert'] = u'预计达到时间不得小于当前时间'
            return json_response(resp)
        if user.head_type > 1:
            pass
            '''
            #因为晚上无人接单的原因取消到预计到店时间限制(汉堡王),迟到时间为合约时间
            if maintenance.create_time.hour == 12 or maintenance.create_time.hour < 7:
                #ct = maintenance.must_time
                pass
            else:
                hy_time = maintenance.create_time + timedelta(hours=(maintenance.must_range+1))
                if ct > hy_time:
                    resp['alert'] = u'预计达到时间不得晚于合约时间一个小时:{}'.format(hy_time.strftime('%Y-%m-%d %H:%M'))
                    return json_response(resp)
                #ct = ct if  ct > maintenance.must_time else maintenance.must_time
            '''
        else:
            if maintenance.start_time > ct or ct > maintenance.end_time:
                resp['alert'] = u'预计时间必须在{}-{}'.format(pf9(maintenance.start_time), pf9(maintenance.end_time))
                return json_response(resp)
        loc = user.loc
        store = Store.objects.filter(id=ObjectId(maintenance.store)).first()
        logger.info('debug:{}:{}'.format(loc, store.loc))
        if not loc or not store or not store.loc:
            resp['status'], resp['alert'] = 0, u'用户,或者店铺坐标不存在，请联系管理员'
            return json_response(resp)

        opt_loc = store.loc
        distance = distanceByLatLon(opt_loc[0], opt_loc[1], loc[0], loc[1])
        item = {
            'status': 1,
            'come_time': ct,
            'update_time': dt.now(),
            'single_time': dt.now(),
            'work_distance': distance,
            'grab_user': user
        }
        for k, v in item.iteritems():
            setattr(maintenance, k, v)

        try:
            mh = MaintenanceHistory.objects.get(maintenances=maintenance)
        except:
            resp['status'], resp['alert'] = 0, u'维修历史不存在, 请联系管理员'
            return json_response(resp)

        mh.grab_users.append(maintenance.grab_user)

        try:
            mc = MaintenanceCollection.objects.get(histories=mh)
        except:
            resp['status'], resp['alert'] = 0, u'维修合集不存在, 请联系管理员'
            return json_response(resp)

        grab_users_set = set(mc.grab_users or [])
        grab_users_set.add(maintenance.grab_user)
        mc.grab_users = list(grab_users_set)

        maintenance.save()
        mh.save()
        mc.save()

        if maintenance.head_type > 1:
            # 如果为采购，接单即为签到
            if maintenance.is_buy:
                maintenance.status = 3
                maintenance.arrival_time = dt.now()
                maintenance.save()

            REDIS.hdel('call_pool', str(maintenance.id))
            parent_users = user.parent_users()
            parent_user_id = parent_users[0].id if len(parent_users) > 0 else ''
            # 计算到店时间和完成时间，用于消息推送
            come_time = ct if ct > maintenance.must_time else maintenance.must_time
            work_time = come_time + timedelta(hours=maintenance.work_range)
            REDIS.hset('control_pool', oid, '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|0|{}|0'.format(time.time(),
                                                                                             maintenance.code,
                                                                                             maintenance.grab_user.name,
                                                                                             SERVICE_COMPANY.get(
                                                                                                 maintenance.head_type),
                                                                                             maintenance.store_name,
                                                                                             store.no,
                                                                                             maintenance.id,
                                                                                             maintenance.user.id,
                                                                                             user.id,
                                                                                             parent_user_id,
                                                                                             time.mktime(
                                                                                                 come_time.timetuple()),
                                                                                             time.mktime(
                                                                                                 work_time.timetuple())))

        title = PUSH1.format(maintenance.title, user.name)
        push_message(maintenance.user.id, title, {
            'type': 1,
            'oid': str(maintenance.id),
            'come_time': pf3(ct),
            'cid': str(mc.id),
        })
        resp['status'] = 1
        resp['info'] = {'oid': str(maintenance.id), 'cid': str(mc.id)}
    else:
        resp['alert'] = u'该单已经被抢'
    return json_response(resp)


@login_required('0')
def repairs(request):
    """  修单列表（适用标准版和连锁版）

    :uri: /api/v1/service/repairs
    :POST params:
        * p 当前页面，默认1
    :return:
        * 请参考 uri: /api/v1/merchant/maintenance/<oid>
    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    data = get_json_data(request) or request.POST.dict()
    p = int(data.get('p', 1))
    # mtce = Maintenance.objects((Q(be_reset_fixed__ne=1) | Q(is_collect=1)) & Q(collected__ne=1) & Q(grab_user=user) & Q(status__gt=0)).order_by('-create_time').skip((p-1)*20).limit(20)
    # results = []
    # for m in mtce:
    #     if m.head_type ==1:
    #         results.append(m.get_result1())
    #     else:
    #         results.append(m.get_result())
    # resp['info']['results'] = results
    # return json_response(resp)

    mc = MaintenanceCollection.objects(grab_users=user).order_by('-create_time').skip((p - 1) * 20).limit(20)
    collections = [collection.get_result(grab_user=user) for collection in mc]

    resp['info']['results'] = collections
    return json_response(resp)


@login_required('0')
def repair(request, oid):
    """  修单详细（适用标准和连锁版）标准版多进程

    :uri: /api/v1/service/repair/<oid>
    :return:
        * 请参考 uri: /api/v1/merchant/maintenance/<oid>

    """
    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    logger.info(oid)
    mh = MaintenanceHistory.objects.filter(grab_users=user, maintenances=ObjectId(oid))
    if mh.count():
        mtce = Maintenance.objects.get(id=ObjectId(oid))
    else:
        resp['status'], resp['alert'] = 0, u'该维修工无法查看此工单'
        return json_response(resp)

    if mtce.head_type == 1:
        resp['info'] = mtce.get_result1()
    else:
        resp['info'] = mtce.get_result(1)

    resp['info']['reset_fix_maintenances'] = mtce.get_reset_fixes(user)

    return json_response(resp)


@login_required('0')
def collection(request, id):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)

    try:
        mtce = MaintenanceCollection.objects.get(id=ObjectId(id), grab_users=user)
    except:
        resp['alert'] = u'订单合集不存在'
        return json_response(resp)

    resp['info'] = mtce.get_result(grab_user=user)
    return json_response(resp)


@login_required('0')
def bill1(request, oid):
    """  填写(修改)工单 (使用标准版)

    :uri: /api/v1/service/bill1/<oid> 叫修单id
    :POST:
        * cid          报价单id存在则是编辑
        * device       设备的id(必填，用于多工单报表,第一次填写工单选择维修单device)
        * loc          坐标提交用于签到
        * analysis     故障分析
        * measures     故障描述
        * spare        配件id “,”号隔开
        * spare_status 配件损坏类型 1为自然 0为人为 “,”号隔开
        * spare_count  配件个数 “,”号隔开
        * spare_over   保固非保固 1为保内 0为非保多个用“,”隔开
        * labor_hour   人工维修时间
        * other_msg    其他费用原因','隔开
        * other_total  其他费用金额','隔开          
        * message      备注
        * other_message 其他建议
        * repair_pic   维修图片多个','号隔开

    """
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    logger.info('debug1:{}'.format(data))
    user = get_user(request)
    mtce = Maintenance.objects.filter(id=ObjectId(oid), status__in=[1, 5, 3, 4], grab_user=user).first()
    if not mtce:
        resp['alert'], resp['status'] = u'该维修单不存在', 0
        return json_response(resp)
    query = {'maintenance': mtce}
    cid = data.get('cid')
    if cid:
        query['id'] = ObjectId(cid)
    else:
        query['id'] = ObjectId()
    bill = Bill.objects.filter(**query).first()
    if request.method == 'POST':
        if bill:
            if bill.status == 1:
                resp['alert'] = u'该修单已经确认无法修改'
                return json_response(resp)
            if mtce.grab_user <> user:
                resp['alert'] = u'无该订单权限'
                return json_response(resp)
        analysis, measures, spare, spare_status, spare_count, spare_over, labor_hour, other_msg, other_total, message, device, repair_pic, other_message, loc = \
            [data.get(i) for i in
             ['analysis', 'measures', 'spare', 'spare_status', 'spare_count', 'spare_over', 'labor_hour', 'other_msg',
              'other_total', 'message', 'device', 'repair_pic', 'other_message', 'loc']]
        if not analysis:
            resp['alert'] = u'请填写故障分析'
            return json_response(resp)
        if not measures:
            resp['alert'] = u'请填写故障描述'
            return json_response(resp)
        if not labor_hour:
            resp['alert'] = u'维修工时不得为空'
            return json_response(resp)
        if not device:
            resp['alert'] = u'该设备不存在'
            return json_response(resp)

        store = Store.objects.get(id=ObjectId(mtce.store))
        # 对比坐标距离
        if store.loc and loc:
            loc = [float(i) for i in loc.split(',')]
            if distanceByLatLon(store.loc[0], store.loc[1], loc[0], loc[1]) > 1:
                resp['alert'] = u'请在餐厅里提交工单,未获取当前坐标'
                return json_response(resp)

        sp_status, sp_over, total, sparess = 1, 1, 0, []
        if spare and spare_status and spare_count and spare_over:
            spares = spare.split(',')
            spare_statuss = spare_status.split(',')
            spare_counts = spare_count.split(',')
            spare_overs = spare_over.split(',')
            for idx, sp in enumerate(spares):
                spa = Spare.objects.get(id=ObjectId(sp))
                over = int(spare_overs[idx])
                spc = int(spare_counts[idx])
                sps = int(spare_statuss[idx])
                if sps == 0: sp_status = 0
                if over == 0: sp_over = 0
                price = 0 if over == 1 and sps == 1 else spa.price
                total += spc * price
                sparess.append({'device': mtce.device, 'spare': ObjectId(sp), 'guarantee': spa.guarantee, 'count': spc,
                                'name': spa.name, 'price': round(price, 2), 'status': over, 'category': sps,
                                'total': round(spc * price, 2)})
        labor = CHARGE * float(labor_hour)
        total += labor
        others = []
        if other_msg:
            other_msgs = other_msg.split(',')
            other_totals = other_total.split(',')
            for index, other_m in enumerate(other_msgs):
                other_t = float(other_totals[index])
                total += other_t
                others.append({'msg': other_m, 'total': other_t})
        device = Device.objects.get(id=ObjectId(device))
        work_time = dt.now() + timedelta(hours=float(labor_hour))
        item = {
            'opt_user': mtce.user,
            'user': user,
            'maintenance': mtce,
            'total': round(total, 2),
            'analysis': analysis,
            'measures': measures,
            'status': 0,
            'state': 0,
            'labor_hour': float(labor_hour),
            'device': device,
            'labor': round(labor, 2),
            'others': others,
            'message': message,
            'other_message': other_message,
            'repair_pic': repair_pic.split(',') if repair_pic else [],
            'will_work_time': work_time
        }
        if bill:
            for k, v in item.iteritems():
                setattr(bill, k, v)
            bill.save()
            BSpare.objects(bill=bill).delete()
            resp['alert'] = u'修改成功'
        else:
            bill = Bill()
            for k, v in item.iteritems():
                print k, v
                setattr(bill, k, v)
            bill.save()
            resp['alert'] = u'保存成功'
        for s in sparess:
            s.update({'bill': bill})
            BSpare(**s).save()
        resp['status'] = 1
        # 更新签到状态
        mtce.status = 3
        mtce.arrival_time = dt.now()
        mtce.save()
        push_message(mtce.user.id, PUSH14, {
            'type': 14,
            'oid': oid,
            'bid': str(bill.id),
            'name': user.name,
            'product': device.name,
            'cid': mtce.collection_id,
        })
    resp['status'] = 1
    resp['info'] = mtce.get_result1()
    return json_response(resp)


@login_required('0')
def bill(request, oid):
    """  填写(修改)维修单-维修成功工单 (适用连锁版)

    :uri: /api/v1/service/bill/<oid> 叫修单ID
   
    :POST:
        * analysis     故障分析
        * measures     故障描述
        * spare        配件id “,”号隔开
        * spare_status 配件损坏类型 1为自然 0为人为 “,”号隔开
        * spare_count  配件个数 “,”号隔开
        * spare_over   保固非保固 1为保内 0为非保多个用“,”隔开
        * stay         住宿天数
        * message      备注

        * express       快递单号
        * other_msg     其他费用原因','隔开 （其他费用包含快递费）
        * other_total   其他费用金额','隔开 （其他费用包含快递费）  
        * other_message 其他建议

        * repair_pic   维修图片多个','号隔开(包含快递单号)
        * express_logo  快递单图片

    :get return:
        * api/v1/merchant/maintenances 请参考
    """

    def charge(mtce, stay):
        now = dt.now()
        if mtce.state == 1:
            post_time = mtce.single_time.hour
            post_type = 1 if 8 <= post_time <= 20 else 2
            charge = Charge.objects.filter(status=1, head_type=mtce.user.head_type, fix_time=mtce.work_range,
                                           fix_time_type=post_type).first()
        else:
            charge = Charge.objects.filter(status=2, head_type=mtce.user.head_type, fix_time_type=3,
                                           fix_time=mtce.work_range).first()
        labor, traff, stay = 0, 0, 0
        if charge and mtce.is_buy == 0:
            # 维修时效
            fix_range = float(getattr(charge, 'fix_time', 0))
            # 判断是否迟到，判断是否准时完修
            # 晚上的单子，合约到店时间是到店时间 0为按时 1为迟到 2为xxx
            # 合约完成时间
            is_later, is_worked = 0, 0
            if mtce.create_time.hour == 12 or mtce.create_time.hour < 7:
                must_time = mtce.must_time
            else:
                must_time = mtce.must_time if mtce.must_time > mtce.come_time else mtce.come_time
                # 判断是否到修时间内
            if mtce.arrival_time > must_time: is_later = 1
            # 必须完成时间
            work_time = mtce.arrival_time + timedelta(hours=fix_range)
            # 合约规定完成时间
            must_work_time = must_time + timedelta(hours=fix_range)
            # 判断是否在维修时效内
            if now > work_time: is_worked = 0
            # 迟到算一半费用
            traff = charge.traffic1 if is_later else charge.traffic1 * 0.5
            # 暂停另外计算合约修复时间，不计算迟到
            if mtce.stop == 0:
                work_time = mtce.stop_come_time + timedelta(hours=fix_range)
                must_work_time = mtce.stop_day + timedelta(hours=fix_range)
                work_range = round(time.mktime(now.timetuple()) - time.mktime(mtce.stop_come_time.timetuple()) / 3600,
                                   1)
            else:
                work_range = round(time.mktime(now.timetuple()) - time.mktime(mtce.arrival_time.timetuple()) / 3600, 1)
            # 获取到个数和分数
            p, t = [int(i) for i in str(work_range).split('.')]
            if p >= charge.fix_time:
                labor = charge.fix_time * charge.quickfix1
                labor += (p - charge.fix_time) * charge.quickfix2
                if t <= 5:
                    labor += charge.quickfix2 * 0.5
                else:
                    labor += charge.quickfix2
            else:
                labor = p * charge.quickfix1
                if t <= 5:
                    labor += charge.quickfix2 * 0.5
                else:
                    labor += charge.quickfix2
            if labor > charge.quickfix3: labor = charge.quickfix3
            stay = int(stay) * charge.quickfix4
        return round(labor, 2), round(traff, 2), round(stay, 2)

    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    mtce = Maintenance.objects.filter(id=ObjectId(oid), status__in=[1, 5, 3, 4], grab_user=user).first()
    if not mtce:
        resp['alert'], resp['status'] = u'该维修单不存在', 0
        return json_response(resp)

    bill = Bill.objects.filter(maintenance=mtce).first()
    if request.method == 'POST':
        if bill:
            if bill.status == 1:
                resp['alert'] = u'该修单已经确认无法修改'
                return json_response(resp)

            if bill.user <> user:
                resp['alert'] = u'无该订单权限'
                return json_response(resp)
        analysis, measures, spare, spare_status, spare_count, spare_over, stay, message, repair_pic, other_message, express, other_msg, other_total, express_logo \
            = [data.get(i) for i in
               ['analysis', 'measures', 'spare', 'spare_status', 'spare_count', 'spare_over', 'stay', 'message',
                'repair_pic', 'other_message', 'express', 'other_msg', 'other_total', 'express_logo']]
        if not analysis and mtce.is_buy == 0:
            resp['alert'] = u'请填写故障分析'
            return json_response(resp)
        if not measures and mtce.is_buy == 0:
            resp['alert'] = u'请填写故障描述'
            return json_response(resp)
        if mtce.is_buy == 1 and not express:
            resp['alert'] = u'请填写快递单号'
            return json_response(resp)
        sp_status, sp_over, total, sparess = 1, 1, 0, []
        if spare and spare_status and spare_count and spare_over:
            spares = spare.split(',')
            spare_statuss = spare_status.split(',')
            spare_counts = spare_count.split(',')
            spare_overs = spare_over.split(',')
            for idx, sp in enumerate(spares):
                spa = Spare.objects.get(id=ObjectId(sp))
                over = int(spare_overs[idx])
                spc = int(spare_counts[idx])
                sps = int(spare_statuss[idx])
                if sps == 0: sp_status = 0
                if over == 0: sp_over = 0
                price = 0 if over == 1 and sps == 1 else spa.price
                total += spc * price
                sparess.append({'device': mtce.device, 'spare': ObjectId(sp), 'guarantee': spa.guarantee, 'count': spc,
                                'name': spa.name, 'price': round(price, 2), 'status': over, 'category': sps,
                                'total': round(spc * price, 2)})
        stay = int(data.get('stay', 0)) if data.get('stay') else 0
        if sp_status == 0 or sp_over == 0 or (mtce.guarantee == 0 and not spare):
            labor, travel, stay_total = charge(mtce, stay)
        else:
            labor, travel, stay_total = 0, 0, 0
        total += labor
        total += travel
        total += stay_total

        others = []
        if other_msg:
            other_msgs = other_msg.split(',')
            other_totals = other_total.split(',')
            for index, other_m in enumerate(other_msgs):
                other_t = float(other_totals[index])
                total += other_t
                others.append({'msg': other_m, 'total': other_t})

        item = {
            'opt_user': mtce.user,
            'user': user,
            'maintenance': mtce,
            'total': round(total, 2),
            'analysis': analysis,
            'measures': measures,
            'status': 0,
            'state': 1,
            'labor': round(labor, 2),
            'travel': round(travel, 2),
            'stay': stay,
            'stay_total': stay_total,
            'express': express,
            'message': message,
            'others': others,
            'other_message': other_message,
            'repair_pic': repair_pic.split(',') if repair_pic else [],
            'express_logo': express_logo
        }
        if bill:
            for k, v in item.iteritems():
                setattr(bill, k, v)
            bill.save()
            BSpare.objects(bill=bill).delete()
            resp['alert'] = u'修改成功'
        else:
            bill = Bill(**item).save()
            resp['alert'] = u'保存成功'

        for s in sparess:
            s.update({'bill': bill})
            BSpare(**s).save()
        resp['status'] = 1

        members = [mtce.user]
        members.extend(user.parent_users())
        for member in members:
            push_message(member.id, PUSH2.format(user.name), {
                'type': 2,
                'oid': oid,
                'cid': mtce.collection_id,
            })

        item = {'status': 5, 'work_time': dt.now()}
        for k, v in item.iteritems():
            setattr(mtce, k, v)
        mtce.save()
        # 删除提醒
        REDIS.hdel('control_pool', oid)
        REDIS.hset('confirm_pool', oid, '{}|{}|{}|{}'.format(time.time(), mtce.user.id, 0, mtce.title))
        return json_response(resp)
    resp['status'] = 1
    resp['info'] = mtce.get_result()
    return json_response(resp)


@login_required('0')
def bill2(request, oid):
    """  填写(修改)维修单--失败 填写失败原因 (适用连锁版)

    :uri: /api/v1/service/bill2/<oid> 修单ID
    :post:
        * analysis     故障分析
        * measures     故障描述
        * reason       选择失败原因
        * content      填写失败原因 
        * stay         住宿费,天数
        * message       备注
        * other_message 其他备注
        * repair_pic   维修图片多个','号隔开(包含快递单号)

    """
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    mtce = Maintenance.objects.filter(id=ObjectId(oid), status__in=[1, 5, 3, 4], grab_user=user).first()
    if not mtce:
        resp['alert'], resp['status'] = u'该维修单不存在', 0
        return json_response(resp)

    def charge(mtce, stay):
        if mtce.state == 1:
            post_time = mtce.single_time.hour
            post_type = 1 if 8 <= post_time <= 20 else 2
            charge = Charge.objects.filter(status=1, head_type=mtce.user.head_type, fix_time=mtce.work_range,
                                           fix_time_type=post_type).first()
        else:
            charge = Charge.objects.filter(status=2, head_type=mtce.user.head_type, fix_time_type=3,
                                           fix_time=mtce.work_range).first()
        labor, traff = 0, 0
        if charge:
            work_time = float(pf7(dt.now()) - pf7(mtce.arrival_time)) / float(3600)
            work_range = work_time - charge.quickfix
            labor = charge.fix_time * charge.quickfix1
            if work_range > 0:
                if work_range < 0.5:
                    labor += charge.quickfix2 * 0.5
                else:
                    labor += charge.quickfix2
            # 交通费只算市内
            traff = charge.traffic1
        '''
            if mtce.work_distance <= 100:
                traff = charge.traffic1
            elif 100 < mtce.work_distance and mtce.work_distance <= 150:
                traff = charge.traffic2
            elif 150 < mtce.work_distance:
                traff = charge.traffic3 
        stay = int(stay) * charge.quickfix4 if stay else 0
        '''
        stay = int(stay) * charge.quickfix4
        return round(labor, 2), round(traff, 2), round(stay, 2)

    bill = Bill.objects.filter(maintenance=mtce).first()
    if request.method == 'POST':
        if bill:
            if bill.status == 1:
                resp['alert'] = u'该修单已经确认无法修改'
                return json_response(resp)
            if bill.user <> user:
                resp['alert'] = u'无该订单权限'
                return json_response(resp)
        analysis, measures, content, reason, stay, repair_pic, other_message, message = [data.get(i) for i in
                                                                                         ['analysis', 'measures',
                                                                                          'content', 'reason', 'stay',
                                                                                          'repair_pic', 'other_message',
                                                                                          'message']]
        stay = int(data.get('stay', 0)) if data.get('stay') else 0
        total = 0
        if mtce.guarantee == 0:
            labor, travel, stay_total = charge(mtce, stay)
        else:
            labor, travel, stay_total = 0, 0, 0
        total += labor
        total += travel
        total += stay_total
        item = {
            'opt_user': mtce.user,
            'user': user,
            'maintenance': mtce,
            'analysis': analysis,
            'measures': measures,
            'content': content,
            'reason': reason,
            'total': total,
            'status': 0,
            'state': 0,
            'labor': round(labor, 2),
            'travel': round(travel, 2),
            'stay': stay,
            'stay_total': stay_total,
            'message': message,
            'repair_pic': repair_pic.split(',') if repair_pic else [],
            'other_message': other_message
        }
        if bill:
            for k, v in item.iteritems():
                setattr(bill, k, v)
            bill.save()
            resp['alert'] = u'修改成功'
        else:
            bill = Bill(**item).save()
            resp['alert'] = u'保存成功'

        item = {'status': 4, 'work_time': dt.now()}
        for k, v in item.iteritems():
            setattr(mtce, k, v)
        mtce.save()

        title = PUSH7.format(user.name, mtce.title)
        sdata = {'type': 7, 'content': content, 'oid': oid, 'name': user.name, 'cid': mtce.collection_id}

        for member in mtce.users():
            push_message(member.id, title, sdata)
        # 删除提醒
        REDIS.hdel('control_pool', oid)
        REDIS.hset('confirm_pool', oid, '{}|{}|{}|{}'.format(time.time(), mtce.user.id, 0, mtce.title))
        return json_response(resp)
    resp['info'] = mtce.get_result()
    return json_response(resp)


@login_required('0')
def bill3(request, oid):
    """  填写(修改)维修单--完整 #作废

    :uri: /api/v1/service/bill3/<oid> 修单ID

    :GET return:
        * product: 维修设备名称
        * supplier: 供应商名称
        * repairs: [{'product_code':维修品序列号, 'production_date':生产日期, 'installation_date':安装日期,'expiration_date':过期日期}]
        
        * quality 保质期 1为保质期内 0为保质期外
        * odm odm号
        * product 商品id
        * error_code 错误代码
        * product_code 设备序列号
        * spare':配件信息，请查看 repairs
        * spare_price':配件总价
        * labor':人工费
        * travel':茶旅费
        * total':总价
        * status: 0是新创建的， 1为商家确认
        * production_date':生产日期
        * expiration_date':安装日期
        * installation_date':过期日期

    :POST params(修改): 
        * cid 该修单的id(修改)
        * quality 保质期 1为保质期内 0为保质期外
        * odm odm号
        * error_code error_code_id
        * product_code 设备序列号
        * spare 备件id多个用|隔开
        * spare_count 配件数与spare对应请用|隔开
        * travel 差旅费
        * labor 人工费
        * production_date 生产日期
        * installation_date 安装日期
        * expiration_date 过期日期

        * analysis     故障分析
        * measures     故障描述
        * content      失败原因

    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    cid = data.get('cid')
    user = get_user(request)
    mtce = Maintenance.objects.get(id=ObjectId(oid), status__in=[1, 2, 3], grab_user=user)
    if not mtce:
        resp['alert'], resp['status'] = u'该维修单不存在', 0
        return json_response(resp)
    bill = Bill.objects.filter(maintenance=mtce.maintenance).first()
    if request.method == 'POST':
        if bill:
            if bill.status == 1:
                resp['alert'] = u'该修单已经确认无法修改'
                return json_response(resp)
            if bill.user <> user:
                resp['alert'] = u'无该订单权限'
                return json_response(resp)
        quality, odm, error_code, product_code, spare, spare_count, travel, labor, production_date, expiration_date, installation_date = [
            data.get(i) for i in
            ['quality', 'odm', 'error_code', 'product_code', 'spare', 'spare_count', 'travel', 'labor',
             'production_date', 'expiration_date', 'installation_date']]
        if DB.bill.find_one({'maintenance': ObjectId(oid)}) and not cid:
            resp['alert'], resp['status'] = u'该维修单已经生成请勿重复生成', 0
        elif not quality and quality <> 0:
            resp['alert'], resp['status'] = u'是否在保质期必须选择', 0
        elif not odm and 'odm' not in mtce.skips:
            resp['alert'], resp['status'] = u'ODM号码必须填写', 0
        elif not error_code:
            resp['alert'], resp['status'] = u'error code不得为空', 0
        elif not product_code:
            resp['alert'], resp['status'] = u'设备序列号不得为空', 0
        else:
            total = 0
            errors = Errors.objects.get(id=ObjectId(error_code))
            if errors:
                total = 0
            else:
                resp['alert'], resp['status'] = u'无该error code', 0
                return json_response(resp)
            spare_total, spas = 0, []
            if spare:
                spare_counts = spare_count.split('|')
                sparess = spare.split('|')
                for idx, s in enumerate(sparess):
                    spa = Spare.objects.filter(id=ObjectId(s)).first()
                    spc = int(spare_counts[idx])
                    if spa and spc:
                        spas.append({
                            'id': str(spa.id),
                            'name': spa.name,
                            'price': spa.price,
                            'count': spc,
                            'total': spa.price * spc
                        })
                        total += spa.price * spc
                        spare_total += spa.price * spc
                    else:
                        resp['alert'], resp['status'] = u'无该备件', 0
                        return json_response(resp)
            if labor:
                total += float(labor)
            if travel:
                total += float(travel)
            item = {
                'opt_user': mtce.opt_user,
                'user': user,
                'maintenance': mtce.maintenance,
                'quality': quality,
                'odm': odm,
                'supplier': mtce['supplier_id'],
                'product': mtce['product_id'],
                'error_code': errors,
                'product_code': product_code,
                'spare': spas,
                'spare_price': spare_total,
                'labor': float(labor),
                'travel': float(travel),
                'total': total,
                'status': 0,
                'state': 2,
                'production_date': production_date,
                'expiration_date': expiration_date,
                'installation_date': installation_date
            }
            if bill:
                for k, v in item.iteritems():
                    setattr(bill, k, v)
                bill.save()
            else:
                Bill(**item).save()
            BSpare.objects(bill=bill).delete()
            for s in sparess:
                s.update({'bill': bill})
                BSpare(**s).save()
            push_message(mtce.opt_user.id, u"{}填写了维修单，价格为:{}，赶快去确认吧！".format(user.name, total), {
                'type': 2,
                'oid': oid,
                'cid': mtce.collection_id,
            })
            resp['alert'], resp['status'] = u'提交成功，请等待商家确认！', 1
            mtce.updates('status', 4)
        return json_response(resp)

    item = {
        'product': mtce.product_id.name,
        'supplier': mtce.supplier_id.name,
        'repairs': rps,
        'skip': mtce.skips
    }
    if mtce.head_type == 2:
        item.update(mtce.get_result())
    else:
        repairs = DB.repair.find(
            {'user': mtce.opt_user.id, 'product': mtce.product_id.id, 'supplier': mtce.supplier_id.id})
        rps = []
        pf = lambda x: dt.strftime(x, '%Y-%m-%d') if x else ''
        for rep in repairs:
            rps.append({
                'product_code': rep.get('product_code'),
                'production_date': pf(rep.get('production_date')),
                'installation_date': pf(rep.get('installation_date')),
                'expiration_date': rep.get('expiration_date')
            })
    if bill:
        item['bill'] = bill.detail()
    resp['info'] = item
    return json_response(resp)


@login_required('0')
def review(request, oid):
    """  获取点评

    :uri: /api/v1/service/review/<oid> oid 为维修单id

    :GET return:
        * user_id 被点评人id
        * user_name 被点评人名称
        * opt_user_id 点评人id
        * opt_user_name 点评人名称
        * ask1 点评1
        * ask2 点评2
        * content 点评描述
    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    review = Review.objects.get(maintenance=ObjectId(oid), user=user.id)
    resp['info'] = review.detail()
    return json_response(resp)


@login_required('0')
def stop(request, oid):
    """  暂停服务 

    :uri: /api/v1/service/stop/<oid> oid 为修单id(接单id:/api/v1/service/grab/<oid>)
    :GET params:
        * title 与xxx xxx区设备经理沟通情况
        * name 区域经理名
        * mobile 区域经理电话

    :POST params:
        * day 从新到店维修时间 ‘201509101400’ 年月日时分
        * type 是否沟通 1 为沟通 0为未沟通 必须沟通
        * reason 提交暂停内容
        * content 请输入原因 
    """

    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(oid), status__gt=0, grab_user=user)

    if not maintenance:
        resp['status'], resp['alert'] = 0, u'无该修单或者无该权限'
        return json_response(resp)
    company_name = SERVICE_COMPANY[maintenance.head_type]
    if request.method == 'GET':
        connector = AREA_CONNECTOR[maintenance.head_type][maintenance.area]
        resp['info']['title'] = u'与{} {}设备经理沟通情况'.format(company_name, maintenance.area)
        resp['info']['name'] = connector[0]
        resp['info']['mobile'] = connector[1]
        return json_response(resp)
    day, head_type, reason, content = [data.get(i) for i in ['day', 'type', 'reason', 'content']]
    if not head_type or int(head_type) == 0:
        resp['status'], resp['alert'] = 0, u'必须沟通'
        return json_response(resp)
    if not day:
        resp['status'], resp['alert'] = 0, u'必须选择重新到店时间'
        return json_response(resp)
    if not reason:
        resp['status'], resp['alert'] = 0, u'必须填写暂停原因'
        return json_response(resp)

    item = {'stop': -1, 'stop_day': day, 'stop_reason': reason, 'stop_content': content}
    for k, v in item.iteritems():
        setattr(maintenance, k, v)
    maintenance.save()
    stop_day = dt.strptime(day, '%Y%m%d%H%M%S')

    mobile = AREA_CONNECTOR[maintenance.head_type][maintenance.area][1]
    send_sms(mobile, u'【51快修】餐厅:{},设备:{},编号:{},需要暂停至:{},申请暂停,原因:{},申请人:{}({}),确认请回:编号 Y,拒绝请回:编号 N,请尽快处理！'.format(
        maintenance.store_name, maintenance.product, maintenance.code, stop_day.strftime(u'%Y年%m月%d日 %H:%M'),
        reason,
        user.name, user.username), maintenance.code)
    return json_response(resp)


@login_required('0')
def close(request, oid):
    """  结束维修(连锁版，维修工)

    :uri: /api/v1/service/close/<oid:维修单id>  
    :POST params:
        * cid 报价单id(为空则全部结束)
    """
    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    data = get_json_data(request) or request.POST.dict()
    mtce = Maintenance.objects.get(id=ObjectId(oid))
    device = Device.objects.get(id=ObjectId(mtce.device))
    if mtce.head_type == 1:
        query = {'maintenance': mtce.id}
        cid = data.get('cid')
        if cid: query['_id'] = ObjectId(cid)

        bills = Bill.objects(__raw__=query)
        for bill in bills:
            setattr(bill, 'close_time', dt.now())
            setattr(bill, 'state', 1)
            bill.save()
    if not Bill.objects.filter(maintenance=mtce, state__in=[0, 1]).first():
        setattr(mtce, 'status', 5)
        mtce.save()

    push_message(mtce.user.id, PUSH16, {
        'type': 16,
        'oid': oid,
        'name': user.name,
        'product': device.name,
        'cid': mtce.collection_id,
    })
    return json_response(resp)


@login_required('0')
def delete_bill(request, oid):
    """  删除报价单 (餐厅适用标准版和连锁版)

    :uri: /api/v1/service/delete_bill/<oid:叫修id>
    :POST:
        * cid          报价单id必填
    """
    resp = {'status': 0, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    cid = data.get('cid')
    if not cid:
        resp['alert'] = u'报价单id必须填写'
        return json_response(resp)
    user = get_user(request)
    mtce = Maintenance.objects.get(id=ObjectId(oid), grab_user=user)
    Bill.objects.filter(maintenance=mtce, user=user, id=ObjectId(cid)).delete()
    resp['status'] = 1
    return json_response(resp)
