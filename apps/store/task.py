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
from apps.base.models import User, Maintenance, Device, Store, Product, InventoryHeader, InventoryDetail
from settings import *
from bson.objectid import ObjectId 
from apps.base.forms import AssetsEditForm, AssetsStoreForm
from apps.base.common import get_user



@login_required(2)
def list(request):
    current = 'inventory'
    user = get_user(request)
    page = request.GET.get('page', 0)
    page  = int(page) if page else 1
    limit = 30
    query  = InventoryHeader.objects.filter(head_type=user.head_type).order_by('-create_time')
    paginator = Paginator(query,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    res = query[(page-1)*limit:page*limit] if query.count() > (page-1)*limit else query[0:limit]
    return render('store/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def append(request):
    current = 'inventory'
    user = get_user(request)
    form = AssetsStoreForm(request.GET,user=user) 

    area, company, region = [request.GET.get(i) for i in ['area', 'company', 'region']]
    query = {'head_type':user.head_type}
    if area:
        query['area'] = area
    if company:
        query['company'] = company
    if region:
        query['city'] = region
    stores = Store.objects(__raw__=query)
    if request.method == 'POST':
        oid, title, start_time, end_time = [request.POST.get(i) for i in ['oid', 'title', 'start_time', 'end_time']]
        oids   = oid.split(',')
        stores = Store.objects.filter(id__in=[ObjectId(i) for i in oids],head_type=user.head_type)
        header = InventoryHeader(title=title, start_time=start_time, end_time=end_time, total=stores.count(), store=oids,head_type=user.head_type).save()
        for store in stores:
            devices = Device.objects.filter(store=store)
            for device in devices:
                InventoryDetail(header=header, store=store, device=device).save()
        users = User.objects.filter(store_id__in = oids)
        for u in users:
            pass
        messages.success(request,u'保存成功')
    return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))



    

