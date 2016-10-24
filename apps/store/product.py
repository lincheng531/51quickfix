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
from apps.base.models import User, Product, Spare
from settings import *
from bson.objectid import ObjectId 
from apps.base.forms import ProductAppendForm, SpareEditForm
from apps.base.common import get_user, get_pinyin_initials



@login_required(2)
def list(request):
    current = 'product'
    user = get_user(request)
    page = request.GET.get('page', 0)
    tag = request.GET.get('tag')
    page  = int(page) if page else 1
    limit = 30
    query = {'head_type':user.head_type}
    if tag:
        query['$or'] = [{'name':{'$regex':tag}},{'category':{'$regex':tag}},{'brand_name':{'$regex':tag}}]
    query  = Product.objects(__raw__=query).order_by('-create_time')
    paginator = Paginator(query,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    res = query[(page-1)*limit:page*limit] if query.count() > (page-1)*limit else query[0:limit]
    return render('store/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def append(request):
    current = 'product'
    user = get_user(request)
    form = ProductAppendForm(request.GET) 
    if request.method == 'POST':
        form = ProductAppendForm(request.POST)
        if not form.is_valid():
            return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        product = Product()
        setattr(product, 'head_type', user.head_type)
        for k, v in data.iteritems():
            if k == 'brand':
                setattr(product, 'brand_name', v.name)
            if k == 'name':
                setattr(product, 'ecategory', v)
            setattr(product, k, v)
        messages.success(request,u'保存成功')
    return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(2)
def detail(request, oid):
    current = 'product'
    user = get_user(request)
    tag  = request.GET.get('tag')
    product = Product.objects.get(id=ObjectId(oid), head_type=user.head_type)
    query1 = {'product_name':product.name, 'brand':product.brand.id, 'model':product.model}
    query2 = {'product_name':product.name, 'brand':product.brand.id}
    if tag:
        tag = tag.strip()
        query1['$or'] = [{'no':{'$regex':tag}},{'name':{'$regex':tag}},{'brand':{'$regex':tag}}]
        query2['$or'] = [{'no':{'$regex':tag}},{'name':{'$regex':tag}},{'brand':{'$regex':tag}}]
    spares = Spare.objects(__raw__=query1)
    if spares.count() > 0:
        spares =  spares
    else:
        spares = Spare.objects(__raw__=query2)
    return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request)) 

@login_required(2)
def edit(request, oid):
    current = 'product'
    user  = get_user(request)
    product = Product.objects.get(id=ObjectId(oid),head_type=user.head_type)
    form  = ProductAppendForm(product.to_mongo())
    if request.method == 'POST':
        form = ProductAppendForm(request.POST)
        if not form.is_valid():
            return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        for k, v in data.iteritems():
            if k == 'brand':
                setattr(product, 'brand_name', v.name)
            setattr(product, k, v)
        product.save()
        messages.success(request,u'更新成功')
    return render('store/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(2)
def spare_detail(request, cid, oid):
    current = 'product'
    user = get_user(request)
    spare = Spare.objects.get(id=ObjectId(oid))
    form  = SpareEditForm(spare.to_mongo())
    if request.method == 'POST':
        form = SpareEditForm(request.POST)
        if not form.is_valid():
            return render('store/{}_spare_edit.html'.format(current),locals(),context_instance=RequestContext(request)) 
        data = form.cleaned_data
        for k,v in data.iteritems():
            setattr(spare, k, v)
        spare.save()
        messages.success(request,u'更新成功')
        return HttpResponseRedirect('/store/product/detail/{}'.format(cid))
    return render('store/{}_spare_edit.html'.format(current),locals(),context_instance=RequestContext(request)) 





    

