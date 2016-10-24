#encoding:utf-8
from datetime import datetime as dt
from bson.objectid import ObjectId
from hashlib import md5
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache
from apps.base.utils import login
from apps.base.logger import getlogger
from apps.base.common import *
from apps.base.models import Maintenance, MaintenanceStatus, MaintenanceState
from apps.base.models.base import HEAD_BRAND, USER_CATEGORY
from apps.base.forms import ProductForm, SearchMaintenanceForm
from django.contrib import messages
from settings import *
from apps.base.messages import *
from django.core.paginator import Paginator,InvalidPage,EmptyPage

logger = getlogger(__name__)


def _process_result(_r):
    _r['id'] = _r['_id']
    _r['user'] = DB.user.find_one({'_id':_r['user']})
    _r['user_count'] = DB.maintenance_users.find({'maintenance':_r['_id'], 'opt_user':_r['user']['_id']}).count()
    _r['apply_count'] = DB.maintenance_users.find({'maintenance':_r['_id'], 'status':1, 'opt_user':_r['user']['_id']}).count()
    _r['confirm_count'] = DB.maintenance_users.find({'maintenance':_r['_id'], 'status':2, 'opt_user':_r['user']['_id']}).count()
    _r['head_type_'] = HEAD_BRAND.get(_r.get('head_type', ''), '')
    _r['state_'] = MaintenanceState.get(_r.get('state'), '')
    _r['status_'] = MaintenanceStatus.get(_r.get('status'), '')

    return _r

@login_required
def list(request):
    current = 'maintenance'
    store   = request.GET.get('store')
    status = request.GET.get('status')
    search_q = request.GET.get('search_q')
    limit   = int(request.GET.get('length') or '0')
    start = int(request.GET.get('start') or '0')

    query   = {}
    sort    = [('create_time', -1)]
    suf_fix = ''
    if store:
        query['store'] = store

    if status:
        if status == 'pending':
            query['status'] = {'$in': [0]}
        elif status == 'working':
            query['status'] = {'$in': [1, 3, 5, 6]}
        elif status == 'done':
            query['status'] = {'$in': [-1, 2, 4]}

    if search_q:
        query['$or'] = [{item: {'$regex': search_q}} for item in ['code', 'store_name', 'product']]

    res  = []
    _q = DB.maintenance.find(query)
    _res = _q.sort(sort).skip(start).limit(limit)
    for _r in _res:
        _r = _process_result(_r)
        res.append(_r)

    count = _q.count()

    return json_response({
        'draw': request.GET.get('draw'),
        'recordsFiltered': count,
        'data': res
    })


@login_required
def detail(request, oid):
    current = 'maintenance'
    oid = ObjectId(oid)
    item = DB.maintenance.find_one({'_id': oid})
    item = _process_result(item)
    item['store'] = DB.store.find_one({'_id': ObjectId(item.get('store'))})
    grab_user = DB.user.find_one({'_id': ObjectId(item.get('grab_user'))})
    if grab_user:
        item['grab_user'] = grab_user
        item['grab_user']['title'] = USER_CATEGORY.get(grab_user['category'])
    #return render('admin/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))
    return json_response(item)


@login_required
def delete(request,oid):
    current = 'maintenance'
    resp = {'status':0,'info':{},'alert':''}
    DB.maintenance.remove({'_id':ObjectId(oid)})
    url = '/admin/{}/list'.format(current)
    return HttpResponseRedirect(url)


@login_required
def edit(request,oid):
    current = 'maintenance'
    oid = ObjectId(oid)
    
    if request.method == 'GET':
        building = DB.maintenance.find_one({'_id':oid})
        form = ProductForm(building)
        return render('admin/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))

    form = ProductForm(request.POST)
    if not form.is_valid():
        return render('admin/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))

    account = Maintenance.objects.get(id=oid)
    data = form.cleaned_data
    for k,v in  data.items():
        setattr(account,k,v)

    setattr(account, 'update_time', dt.now())
    account.save()
    
    messages.success(request,u'修改成功')
    url = '/admin/{}/detail/{}'.format(current, account.id)
    return HttpResponseRedirect(url)


@login_required
def append(request):
    current = 'maintenance'
    
    if request.method == 'GET':
        form = ProductForm()
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

    form = ProductForm(request.POST)
    if not form.is_valid():
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

    data = form.cleaned_data
    new_record = Maintenance(**data)
    try:
        new_record.save()
    except Exception,e:
        messages.error(request,e.message)
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
    else:
        messages.success(request,u'保存成功')
    
    url = '/admin/{}/detail/{}'.format(current, new_record.id)
    return HttpResponseRedirect(url)



