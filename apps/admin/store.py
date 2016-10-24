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
from apps.base.common import get_user
from apps.base.common import admin_login_required as login_required
from apps.base.models import User, Supplier, Store, Device
from apps.base.sms import send_sms
from apps.base.forms import StoreEditAppendForm, SearchAccountForm
from django.contrib import messages
from settings import *
from apps.base.messages import *
from django.core.paginator import Paginator,InvalidPage,EmptyPage

logger = getlogger(__name__)


@login_required(1)
def list(request, category):
    current = 'store'
    page    = int(request.GET.get('page',1))
    page    = page if page >1 else 1
    limit   = 20

    query   = {}
    sort    = [('update_time',-1)]
    suf_fix = ''

    res  = []
    query = {'is_active':int(category), 'head_type':1}
    city, tag = [request.GET.get(i) for i in ['region', 'store']]
    if city:
        query['city'] = city 
    if tag:
        query['$or'] = [{'name':{'$regex':tag}},{'no':{'$regex':tag}}]
    _res = DB.store.find(query).sort(sort).skip((page-1)*limit).limit(limit)
    for _r in _res:
        _r['id'] = _r['_id']
        res.append(_r)

    paginator = Paginator(DB.store.find(query,fileds=['_id']),limit)

    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage):
        raise Http404
    print dir(paginator)
    form = SearchAccountForm()
    pre_fix = 'admin/{}/list'.format(current)
    n = 12
    l = page - (n/2) > 0 and page - (n/2) or 0
    r = l + n
    pages = range(1,paginator.num_pages + 1,)[l:r]
    
    return render('admin/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(1)
def active(request, oid, category):
    store = Store.objects.get(id=ObjectId(oid))
    setattr(store, 'is_active', int(category))
    store.save()
    return HttpResponseRedirect('/admin/store/detail/{}'.format(store.id))

@login_required(1)
def detail(request,oid):
    current = 'store'
    store   = Store.objects.get(id=ObjectId(oid))
    if request.method == 'POST':
        form = StoreEditAppendForm(request.POST)
        if not form.is_valid():
            return render('admin/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        for k, v in data.iteritems():
            setattr(store, k, v)
        if data.get('licence_type') == '-1' or data.get('certificate_type') == '-1':
            setattr(store, 'is_active', -1)
            logger.info('debug1')
        else:
            logger.info('debug2')
            setattr(store, 'is_active', 1)
        store.save()
        messages.success(request, u'更新成功')
        return HttpResponseRedirect('/admin/store/detail/{}'.format(oid))
    form    = StoreEditAppendForm(store.to_mongo())
    users   = User.objects.filter(store_id=str(store.id))
    return render('admin/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(1)
def delete(request,oid):
    current = 'account'
    resp = {'status':0,'info':{},'alert':''}
    DB.user.remove({'_id':ObjectId(oid)})
    url = '/admin/{}/list'.format(current)
    return HttpResponseRedirect(url)



