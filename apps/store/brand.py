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
from apps.base.models import User, Brand
from settings import *
from bson.objectid import ObjectId 
from apps.base.forms import BrandEditForm
from apps.base.common import get_user, get_pinyin_initials



@login_required(2)
def list(request):
    current = 'brand'
    user = get_user(request)
    page = request.GET.get('page', 0)
    tag  = request.GET.get('tag')
    page  = int(page) if page else 1
    limit = 30
    query = {}
    if tag:
        query['name'] = {'$regex':tag}
    query  = Brand.objects.filter(__raw__=query).order_by('-create_time')
    paginator = Paginator(query,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    for d in dir(p):
        print d, getattr(p, d)
    res = query[(page-1)*limit:page*limit] if query.count() > (page-1)*limit else query[0:limit]
    return render('store/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def append(request):
    current = 'brand'
    user = get_user(request)
    form = BrandEditForm(request.GET, category='view') 
    if request.method == 'POST':
        form = BrandEditForm(request.POST, category='append')
        if not form.is_valid():
            return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        name = data.get('name')
        Brand(**{'name':name, 'initial':get_pinyin_initials(name)}).save()
        messages.success(request,u'保存成功')
    return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def detail(request, oid):
    current = 'brand'
    user  = get_user(request)
    brand = Brand.objects.get(id=ObjectId(oid))
    form  = BrandEditForm(brand.to_mongo(), category='view')
    if request.method == 'POST':
        form = BrandEditForm(request.POST, category='edit')
        if not form.is_valid():
            return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        name = data.get('name')
        brand.name = name
        brand.initial = get_pinyin_initials(name)
        brand.save()
        messages.success(request,u'更新成功')
    return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))





    

