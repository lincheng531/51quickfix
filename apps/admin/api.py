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
    print '==============>'
    print result
    print '==============>'
    resp['info'] = user.get_user_profile_dict()
    response = json_response(resp)
    return response

# @login_required(2)
def maintenanceList(request):
    # if request.method == 'OPTIONS':
    #     response = HttpResponse('', status=200)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     response['Access-Control-Allow-Methods'] = 'POST, GET, PUT, OPTIONS'
    #     response['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, XMLHttpRequest"
    #     return response

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


def test(request):
    import pdb;pdb.set_trace()
    return HttpResponse('test')