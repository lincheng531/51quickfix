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
from apps.base.models import Product, Errors
from apps.base.forms import ErrorsForm, SearchProductForm
from django.contrib import messages
from settings import *
from apps.base.messages import *
from django.core.paginator import Paginator,InvalidPage,EmptyPage

logger = getlogger(__name__)


@login_required
def list(request):
    current = 'errors'
    page    = int(request.GET.get('page',1))
    page    = page if page >1 else 1
    limit   = 20

    query   = {}
    sort    = [('_id',-1)]
    suf_fix = ''


    res  = []
    _res = DB.errors.find(query).sort(sort).skip((page-1)*limit).limit(limit)
    for _r in _res:
        _r['id'] = _r['_id']
        res.append(_r)

    paginator = Paginator(DB.errors.find(query,fileds=['_id']),limit)

    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage):
        raise Http404
    
    form = SearchProductForm()
    pre_fix = 'admin/{}/list'.format(current)
    n = 12
    l = page - (n/2) > 0 and page - (n/2) or 0
    r = l + n
    pages = range(1,paginator.num_pages + 1,)[l:r]
    
    return render('admin/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required
def detail(request,oid):
    current = 'errors'
    oid          = ObjectId(oid)
    item         = DB.errors.find_one({'_id':oid})
    item['id']   = item['_id']
    return render('admin/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required
def delete(request,oid):
    current = 'errors'
    resp = {'status':0,'info':{},'alert':''}
    DB.errors.remove({'_id':ObjectId(oid)})
    url = '/admin/{}/list'.format(current)
    return HttpResponseRedirect(url)


@login_required
def edit(request,oid):
    current = 'errors'
    oid = ObjectId(oid)
    
    if request.method == 'GET':
        building = DB.errors.find_one({'_id':oid})
        form = ErrorsForm(building)
        return render('admin/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))

    form = ErrorsForm(request.POST)
    if not form.is_valid():
        return render('admin/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))

    account = Errors.objects.get(id=oid)
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
    current = 'errors'
    
    if request.method == 'GET':
        form = ErrorsForm()
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

    form = ErrorsForm(request.POST)
    if not form.is_valid():
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

    data = form.cleaned_data
    new_record = Errors(**data)
    try:
        new_record.save()
    except Exception,e:
        messages.error(request,e.message)
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
    else:
        messages.success(request,u'保存成功')
    
    url = '/admin/{}/detail/{}'.format(current, new_record.id)
    return HttpResponseRedirect(url)



