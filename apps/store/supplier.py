#encoding:utf-8
from hashlib import md5
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache  
from django.contrib import messages
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from apps.base.utils import login
from apps.base.common import admin_login_required as login_required
from apps.base.models import User, Supplier
from settings import *
from bson.objectid import ObjectId 
from apps.base.forms import SupplierEditForm
from apps.base.common import get_user, get_pinyin_initials



@login_required(2)
def list(request):
    current = 'supplier'
    user = get_user(request)
    tag = request.GET.get('tag')
    page = request.GET.get('page', 0)
    page  = int(page) if page else 1
    limit = 30
    query = {}
    if tag: query['name'] = {'$regex':tag}
    query  = Supplier.objects(__raw__=query).order_by('-create_time')
    paginator = Paginator(query,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    res = query[(page-1)*limit:page*limit] if query.count() > (page-1)*limit else query[0:limit]
    return render('store/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def append(request):
    current = 'supplier'
    user = get_user(request)
    form = SupplierEditForm(request.GET, category='view') 
    if request.method == 'POST':
        form = SupplierEditForm(request.POST, category='append')
        if not form.is_valid():
            return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        name = data.get('name')
        Supplier(**{'name':name, 'initial':get_pinyin_initials(name)}).save()
        messages.success(request,u'保存成功')
    return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def detail(request, oid):
    current = 'supplier'
    user  = get_user(request)
    supplier = Supplier.objects.get(id=ObjectId(oid))
    form  = SupplierEditForm(supplier.to_mongo(), category='view')
    if request.method == 'POST':
        form = SupplierEditForm(request.POST, category='edit')
        if not form.is_valid():
            return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        name = data.get('name')
        supplier.name = name
        supplier.initial = get_pinyin_initials(name)
        supplier.save()
        messages.success(request,u'更新成功')
    return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))





    

