# -*- encoding:utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from apps.base.common import json_response, get_user, get_json_data
from apps.base.utils import login as _login
from django.contrib.auth import logout as _logout
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from apps.base.models import User
from apps.base.forms import StuffLoginForm as LoginForm
from apps.base.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from apps.base.logger import getlogger

logger = getlogger(__name__)

def logout(request):
    _logout(request)
    return HttpResponseRedirect('/admin/')


def login(request):
    resp = {'status':1, 'info':''}

    form = LoginForm(request.POST)
    if not form.is_valid():
        resp['status'] = 0
        resp['alert'] = u'用户名或密码不符合要求'
        return json_response(resp)

    form_data = form.cleaned_data

    user = authenticate(**form_data)
    if not user:
        resp['status'] = 0
        resp['alert'] = u'用户名或密码错误'
        return json_response(resp)

    if not user.is_superuser:
        resp['status'] = 0
        resp['alert'] = u'你不是管理员，禁止登录'
        return json_response(resp)

    if not user.is_active:
        resp['status'] = 0
        resp['alert'] = u'你已经被禁止登录'
        return json_response(resp)

    user.backend = 'mongoengine.django.auth.MongoEngineBackend'
    result = _login(request, user)
    resp['info'] = user.get_user_profile_dict()
    response = json_response(resp)
    return response

# @login_required(2)
def maintenanceList(request):
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

    query = {}
    status = request.GET.get('status')
    if status:
        query['status__in'] = status.split(',')

    mc = Maintenance.objects(**query).order_by('-create_time').skip((p - 1) * 20).limit(20)
    result = [item.get_result() for item in mc]
    resp['info']['results'] = result
    return json_response(resp)


def _process_result(_r):
    _r['id'] = _r['_id']
    _r['user'] = DB.user.find_one({'_id':_r['user']})
    _r['user_count'] = DB.maintenance_users.find({'maintenance':_r['_id'], 'opt_user':_r['user']['_id']}).count()
    _r['apply_count'] = DB.maintenance_users.find({'maintenance':_r['_id'], 'status':1, 'opt_user':_r['user']['_id']}).count()
    _r['confirm_count'] = DB.maintenance_users.find({'maintenance':_r['_id'], 'status':2, 'opt_user':_r['user']['_id']}).count()
    _r['head_type_'] = HEAD_BRAND.get(_r.get('head_type', ''), '')
    _r['state_'] = MaintenanceState.get(_r.get('state'), '')
    _r['status_'] = MaintenanceStatus.get(_r.get('status'), '')
    _r['device'] = DB.device.find_one({'_id': ObjectId(_r['device'])})
    return _r


def maintenanceDetail(request, id):
    id = ObjectId(id)
    item = DB.maintenance.find_one({'_id': id})
    item = _process_result(item)
    item['store'] = DB.store.find_one({'_id': ObjectId(item.get('store'))})
    grab_user = DB.user.find_one({'_id': ObjectId(item.get('grab_user'))})
    if grab_user:
        item['grab_user'] = grab_user
        item['grab_user']['title'] = USER_CATEGORY.get(grab_user['category'])
    # return render('admin/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))

    item['audit_repair_user'] = DB.user.find_one({'_id': ObjectId(item.get('audit_repair_user'))}) or {}
    item['audit_merchant_user'] = DB.user.find_one({'_id': ObjectId(item.get('audit_merchant_user'))}) or {}
    item['settle_repair_user'] = DB.user.find_one({'_id': ObjectId(item.get('settle_repair_user'))}) or {}
    item['settle_merchant_user'] = DB.user.find_one({'_id': ObjectId(item.get('settle_merchant_user'))}) or {}
    return json_response(item)


def audit_repair(request, id):
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(id))
    user = User.objects.get(id=ObjectId(data['user_id']))
    maintenance.settlement = 1
    maintenance.audit_repair_user = user
    maintenance.audit_repair_date = datetime.datetime.now()
    maintenance.audit_repair_result = bool(int(data['audit_repair_result']))
    maintenance.audit_repair_note = data.get('audit_repair_note')
    maintenance.save()
    return maintenanceDetail(request, id)


def audit_merchant(request, id):
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(id))
    user = User.objects.get(id=ObjectId(data['user_id']))
    maintenance.settlement = 2
    maintenance.audit_merchant_user = user
    maintenance.audit_merchant_date = datetime.datetime.now()
    maintenance.audit_merchant_result = bool(int(data['audit_merchant_result']))
    maintenance.audit_merchant_note = data.get('audit_merchant_note')
    maintenance.save()
    return maintenanceDetail(request, id)


def settlement_clear(request, id):
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(id))
    user = User.objects.get(id=ObjectId(data['user_id']))

    if user.category in ('1', '3', '4', '5', '7'):
        maintenance.settle_merchant_result = True
        maintenance.settle_merchant_user = user
        maintenance.settle_merchant_date = datetime.datetime.now()
        maintenance.settle_merchant_note = data.get('settle_note')

    if user.category in ('0', '2', '6', '7'):
        maintenance.settle_repair_result = True
        maintenance.settle_repair_user = user
        maintenance.settle_repair_date = datetime.datetime.now()
        maintenance.settle_repair_note = data.get('settle_note')

    if maintenance.settle_repair_result and maintenance.settle_merchant_result:
        maintenance.settlement = 3

    maintenance.save()
    return maintenanceDetail(request, id)



def test(request):
    import pdb;pdb.set_trace()
    return HttpResponse('test')