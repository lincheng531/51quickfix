#encoding:utf-8

from datetime import datetime as dt
from hashlib import md5
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache  
from apps.base.utils import login, pf6, pf7
from apps.base.common import get_user, json_response
from apps.base.common import admin_login_required as login_required
from apps.base.models import User, Maintenance, Device, Store, Product, Brand, Bill, Verify
from settings import *
from bson.objectid import ObjectId 
from apps.base.logger import getlogger
from apps.base.forms import AssetsEditForm
from django.core.paginator import Paginator,InvalidPage,EmptyPage

logger = getlogger(__name__)

@login_required(3) 
def list(request):
   
    current = 'verify'
    user = get_user(request)

    maintenances = Maintenance.objects(__raw__={'status':{'$in':[2,4]}, 'verify_status':-1})
    for maintenance in maintenances:
        device = Device.objects.get(id=ObjectId(maintenance.device))
        Verify(**{'head_type':maintenance.head_type, 'maintenance':maintenance.id, 'code':maintenance.code, 'company':maintenance.company, 'device':device.id}).save()
        maintenance.verify_status = 0
        maintenance.save()

    q, page, city, store, category, product, state, error_code, brand, tag, start_day, end_day   = [request.GET.get(i) for i in ['q', 'page', 'region', 'store', 'category', 'product', 'state', 'error_code', 'brand', 'tag', 'start_day', 'end_day']]
    
    page  = int(page) if page else 1
    limit = 30
    query = {'company':user.company,'city':user.city, 'status':{'$in':[2, 4]}}
    if not q:q = '0'
    if user.category == '3':
        query['area'] = user.area
    if user.category == '4':
        query['store'] = {'$in':user.store_id.split(',')}
    #if q or q == '0':
    #    query['status'] = {'$in':[int(i) for i in q.split(',')]}
    if city:
        query['city'] = city
    if store:
        query['store'] = store
    if category:
        products = Product.objects.filter(category=category)
        query['product_id'] = {'$in':products}
    if brand:
        brand = Brand.objects.get(id=ObjectId(brand))
        query['brand'] = brand.name
    if product:
        query['product'] = product
    if state:
        query['state'] = int(state)
    if error_code:
        query['error_code'] = error_code

    create_time_query = {}
    if start_day:
        create_time_query['$gte'] = dt.strptime(start_day, '%Y-%m-%d')
    if end_day:
        create_time_query['$lte'] = dt.strptime(end_day, '%Y-%m-%d')
    if start_day and end_day:
        query['create_time'] = create_time_query

    if tag:
        query['$or'] = [{'code':{'$regex':tag}}, {'company':{'$regex':tag}}, {'product':{'$regex':tag}}]
    maintenances = [i.id for i in Maintenance.objects(__raw__=query)]
    verifys = Verify.objects(__raw__={'maintenance':{'$in':maintenances}, 'status':int(q)})
    paginator = Paginator(verifys,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    res = verifys[(page-1)*limit:page*limit]

    new_call, step_call, hist_call, return_call = 0, 0, 0, 0
    new_call = Verify.objects(__raw__={'maintenance':{'$in':maintenances}, 'status':0}).count()
    step_call = Verify.objects(__raw__={'maintenance':{'$in':maintenances}, 'status':1}).count()
    hist_call = Verify.objects(__raw__={'maintenance':{'$in':maintenances}, 'status':2}).count()
    return_call = Verify.objects(__raw__={'maintenance':{'$in':maintenances}, 'status':3}).count()
    
    return render('provider/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(3)
def close(request):
    current = 'verify'
    ids     = request.POST.get('ids')
    verifys = Verify.objects.filter(id__in = [ObjectId(i) for i in ids.split(',')])
    for verify in verifys:
        verify.status = 2 
        verify.save()
    return json_response({'status':1})

@login_required(3)
def edit(request, oid):
    current = 'verify'
    user    = get_user(request)

    verify = Verify.objects.get(id = ObjectId(oid))
    
    return render('provider/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))


    


    

