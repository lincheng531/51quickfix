#!/user/bin/env python
#encoding:utf-8
import datetime
import json
from datetime import timedelta
from datetime import datetime as dt
from mongoengine import *
from bson.objectid import ObjectId
from django.utils.translation import ugettext_lazy as _
from mongoengine.django.auth import User as BaseUser
from settings import DB, SERVICE_COMPANY, CALL_STATUS
from apps.base.utils import distanceByLatLon, pf, pf2, pf3

class Dict2(dict):

    def __getattr__(self, key):
        return self.get(key, None)


def format_role(user):
    res = {}
    roles = DB.role.find()
    user_roles = [i['role'] for i in DB.user_role.find({'user':user.id})]
    for role in roles:
        if role['_id'] in user_roles:
            res[role['code']] = True 
        else:
            res[role['code']] = False
    return res
  
def repair_status2(maintenance):
    content = repair_status(maintenance)
    return content.replace('</p><p>', '\n').replace('<p class=\'f3\'>', '\n').replace('</p><p class="f3">', '\n').replace('<p>','').replace('</p>', '')

def repair_status(maintenance):  
    service_company = SERVICE_COMPANY.get(maintenance.head_type)
    send_time = maintenance.update_time.strftime('%H:%M')
    if maintenance.status == 0:
        for i in range(4 , 0, -1):
            if i in [4, 3, 2]:
                hp = DB.push_history.find_one({'maintenance':str(maintenance.id), 'category':i})
                if hp:
                    msg = '<p>{}</p><p>{}</p>'.format(hp.get('to_name'), hp.get('to_mobile'))
                    if i == 4:
                        msg = "{}<p class='f3'>{}通知{}总部</p>".format(msg, send_time, service_company)
                    elif i == 3:
                        msg = "{}<p class='f3'>{}通知{}总部</p>".format(msg, send_time, maintenance.company)
                    elif i == 2:
                        msg = "{}<p class='f3'>{}通知{}{}区域经理</p>".format(msg, send_time, maintenance.company, maintenance.city) 
                    return msg
            else:
                step1 = len(maintenance.members)
                return "<p>{}{}{}人</p><p class='f3'>{}通知</p>".format(maintenance.company, maintenance.city, step1, maintenance.update_time.strftime('%H:%M'))
    elif maintenance.status == 1:
        return '<p>未到店</p><p class="f3">预计到店 {}</p><p class="f3">合约到店 {}</p>'.format(pf(maintenance.come_time), pf(maintenance.must_time))
    elif maintenance.status == 3:
        if maintenance.stop == -1:
            return '<p>申请暂停</p><p class="f3">原因:{} {}</p> <p class="f3">重新到修:{}</p>'.format(maintenance.stop_content, maintenance.stop_reason, pf3(maintenance.stop_day) )
        elif maintenance.stop == 0:
            return '<p>确认暂停</p><p class="f3">原因:{} {}</p> <p class="f3">重新到修:{}</p>'.format(maintenance.stop_content, maintenance.stop_reason, pf3(maintenance.stop_day) )
        elif maintenance.stop == -2:
            return '<p>拒绝暂停</p><p class="f3">原因:{} {}</p> <p class="f3">重新到修:{}</p>'.format(maintenance.stop_content, maintenance.stop_reason, pf3(maintenance.stop_day) )
        else:
            return '<p>维修中</p><p class="f3">合约修复 {}</p>'.format(pf3(maintenance.work_time))
    elif maintenance.status == 2:
        return '<p>完成{}</p><p class="f3">合约修复 {}</p>'.format(pf3(maintenance.work_time), pf3(maintenance.must_time))
    elif maintenance.status == 4:
        bill = DB.bill.find_one({'maintenance':maintenance.id})
        if bill:
            return '<p>维修失败</p><p>原因 {}</p>'.format(bill.get('content'))
    elif maintenance.status == 5:
        return '<p>等待工单确认</p>'
    else:
        return CALL_STATUS.get(maintenance.status)


def repair_list(maintenance):
    results = []
    service_company = SERVICE_COMPANY.get(maintenance.head_type)
    create_time = pf2(maintenance.create_time)
    results.append({
                    'head_type':-1,
                    'create_time':create_time
                    })
    results.append({
                    'head_type':1,
                    'create_time':pf(maintenance.create_time),
                    'name':maintenance.user.name,
                    'mobile':maintenance.user.username,
                    'must_time':pf(maintenance.must_time)
                })
    hps = DB.push_history.find({'maintenance':str(maintenance.id), 'category':1})
    if hps.count() > 0:
        create_time2 = pf2(hps[0].get('create_time'))
        if create_time <> create_time2:
            results.append({
                            'head_type':-1,
                            'create_time':create_time2
                            })
            create_time = create_time2 
        item = {
                'head_type':2,
                'count':hps.count(),
                'company':maintenance.company,
                'city':maintenance.city,
                'create_time':pf(hps[0].get('create_time'))
                }
        member_user = DB.user.find_one({'_id':hps[0]['user']})
        if member_user:
            member = DB.user.find_one({'company':member_user['company'], 'city':member_user['city'], 'category':'2'})
            if member:
                item['name'] = member['name']
                item['mobile'] = member['username']
        results.append(item)
    for i in range(2, 5):
        hp = DB.push_history.find_one({'maintenance':str(maintenance.id), 'category':i})
        if hp:
            if i == 2:
                create_time3 = pf2(hp.get('create_time'))
                if create_time <> create_time3:
                    create_time = create_time3
                    results.append({
                        'head_type':-1,
                        'create_time':create_time
                    })
                results.append({
                            'head_type':3,
                            'to_name':hp.get('to_name'),
                            'to_mobile':hp.get('to_mobile'), 
                            'city':maintenance.city,
                            'company':maintenance.company,
                            'create_time':pf(hp.get('create_time'))
                    })
            elif i == 3:
                create_time4 = pf2(hp.get('create_time'))
                if create_time <> create_time4:
                    create_time = create_time4
                    results.append({
                        'head_type':-1,
                        'create_time':create_time
                    })
                results.append({
                            'city':maintenance.city,
                            'company':service_company,
                            'head_type':4,
                            'to_name':hp.get('to_name'),
                            'to_mobile':hp.get('to_mobile'),
                            'create_time':pf(hp.get('create_time'))
                    })
            elif i == 4:
                create_time5 = pf2(hp.get('create_time'))
                if create_time <> create_time5:
                    create_time = create_time5
                    results.append({
                        'head_type':-1,
                        'create_time':create_time
                    })
                results.append({
                            'city':maintenance.city,
                            'company':service_company,
                            'head_type':5,
                            'to_name':hp.get('to_name'),
                            'to_mobile':hp.get('to_mobile'),
                            'create_time':pf(hp.get('create_time'))
                    })
    tmu = maintenance.grab_user
    if tmu:
        create_time6 = pf2(maintenance.single_time) 
        if create_time <> create_time6:
            create_time = create_time6
            results.append({
                'head_type':-1,
                'create_time':create_time
            })
        results.append({
                        'head_type':6,
                        'create_time':pf(maintenance.single_time),
                        'must_time':pf(maintenance.come_time),
                        'to_name':tmu.name,
                        'to_mobile':tmu.username,
                        'company':maintenance.company,
                        'city':maintenance.city
                        })
        if maintenance.status in [2, 3, 4, 5, 6]:
            create_time7 = pf2(maintenance.arrival_time)
            if create_time <> create_time7:
                create_time = create_time7
                results.append({
                    'head_type':-1,
                    'create_time':create_time
                })
            results.append({
                    'head_type':7,
                    'arrival_time':pf(maintenance.arrival_time),
                    'later':maintenance.later
                })
            if maintenance.stop in [-1, 0, -2]:
                titles = {-1:u'申请暂停', 0:u'确认暂停', -2:u'拒绝暂停'}
                results.append({
                    'head_type':12,
                    'title':titles.get(maintenance.stop),
                    'stop_time':pf3(maintenance.stop_day),
                    'content':'{}{}'.format(maintenance.stop_content, maintenance.stop_reason)
                })
        if maintenance.status:
            if maintenance.bill:
                create_time8 = pf2(maintenance.bill.update_time)
                if create_time <> create_time8:
                    create_time = create_time8
                    results.append({
                        'head_type':-1,
                        'create_time':create_time
                    })
                h, t = str(float(86400 - (dt.now() - maintenance.bill.create_time).seconds)/float(3600)).split('.')
                t  = int(float("0.{}".format(t))*60)
                results.append({
                    'head_type':11,
                    'msg':u'未返修,维修成功' if maintenance.bill.state == 1 else u"请在<span class='f1'>{}小时{}分钟</span>内确认故障是否解决".format(h, t), 
                    'create_time':pf(maintenance.bill.update_time) if maintenance.bill else ''
                    })
        elif maintenance.status == 4:
            create_time9 = pf2(maintenance.bill.create_time)
            if create_time <> create_time9:
                create_time = create_time9
                results.append({
                    'head_type':-1,
                    'create_time':create_time
                })
            results.append({
                    'head_type':9,
                    'msg':u'维修失败',
                    'create_time':pf(maintenance.bill.create_time) if maintenance.bill else ''
                })
        else:
            create_time10 = pf2(maintenance.work_time)
            if create_time <> create_time10:
                create_time = create_time10
                results.append({
                    'head_type':-1,
                    'create_time':create_time
                })
            results.append({
                    'head_type':8,
                    'create_time':pf(maintenance.work_time) if maintenance.work_time else ''
                })

    return results