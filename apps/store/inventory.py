#encoding:utf-8

from hashlib import md5
import xlrd, xlwt
from xlutils.copy import copy
from datetime import datetime as dt
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache  
from django.contrib import messages
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from apps.base.utils import login, pf4, pf2, pf5
from apps.base.common import admin_login_required as login_required
from apps.base.models import User, Maintenance, Device, Store, Product, InventoryHeader, InventoryDetail, Brand
from settings import *
from apps.base.messages import PUSH9
from bson.objectid import ObjectId 
from apps.base.logger import getlogger
from apps.base.forms import AssetsEditForm, AssetsStoreForm, AssetsSearchForm
from apps.base.common import get_user, json_response
from apps.base.push import push_message


logger = getlogger(__name__)  

@login_required(2)
def list(request):
    current = 'inventory'
    user = get_user(request)
    page = request.GET.get('page', 0)
    page  = int(page) if page else 1
    inventory_status = request.GET.get('inventory_status')
    limit = 30
    query = {'head_type':user.head_type}
    if inventory_status == u'未开始':
        query['status'] = 0
    elif inventory_status == u'进行中':
        query['status'] = 1
    elif inventory_status == u'已完成':
        query['status'] = 2
    query  = InventoryHeader.objects(__raw__=query).order_by('-create_time')
    paginator = Paginator(query,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    query = query[(page-1)*limit:page*limit] if query.count() > (page-1)*limit else query[0:limit]
    res = []
    for index, r in enumerate(query):
        if index%2 == 0:
            setattr(r, 'row_class', 'active')
        res.append(r)
    return render('store/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def append(request):
    current = 'inventory'
    user = get_user(request)
    form = AssetsStoreForm(request.GET,user=user) 

    title = PUSH9

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
        oid, title, start_time, end_time, scope = [request.POST.get(i) for i in ['oid', 'title', 'start_time', 'end_time', 'scope']]
        oids = oid.split(',')
        stores = Store.objects.filter(id__in=[ObjectId(i) for i in oids],head_type=user.head_type)
        header = InventoryHeader(title=title, start_time=start_time, end_time=end_time, total=stores.count(), store=oids,head_type=user.head_type, scope=scope).save()
        for store in stores:
            devices = Device.objects.filter(store=store)
            for device in devices:
                InventoryDetail(header=header, store=store, device=device, brand=device.brand, product=device.product, ecategory=device.ecategory, category=device.category).save()
        users = User.objects.filter(store_id__in=oids)
        for u in users:
            push_message(u.id, title, {'type':9, 'start_time':start_time, 'end_time':end_time, 'oid':str(header.id)})
        messages.success(request,u'保存成功') 
        return HttpResponseRedirect('/store/inventory/detail/{}'.format(header.id))
    return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def detail(request, oid):
    current = 'inventory'
    user   = get_user(request)
    header = InventoryHeader.objects.get(id=ObjectId(oid))
    return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(2)
def detail2(request, hid, oid):
    current = 'inventory'
    user = get_user(request)
    form   = AssetsSearchForm(request.GET)
    header = InventoryHeader.objects.get(id=ObjectId(hid),head_type=user.head_type)
    store  = Store.objects.get(id=ObjectId(oid))
    query  = {'header':header.id,'store':store.id}
    brand, product, status, ecategory, category = [request.GET.get(i) for i in ['brand', 'product', 'inventory_detail_status', 'ecategory', 'ecategory']]
    if brand:
        query['brand'] = Brand.objects.get(id=ObjectId(brand)).name
    if product:
        query['product'] = {'$in':[i.id for i in Product.objects.filter(name=product)]}
    if status:
        query['status'] = status
    if ecategory:
        query['ecategory'] = ecategory
    if category:
        query['category'] = category
    details = InventoryDetail.objects(__raw__=query)
    complete, miss, devices = 0, 0, []
    for index, d in enumerate(details):
        if index%2 == 0:
            setattr(d, 'row_class', 'active')
        if d.status in [1, 2]: complete += 1
        if d.status ==  2:miss += 1

        devices.append(d)
    return render('store/{}_detail2.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(2)
def notify(request, hid, oid):
    current = 'inventory'
    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    header = InventoryHeader.objects.get(id=ObjectId(hid))
    users = User.objects.filter(store_id=oid)
    for u in users:
        push_message(u.id, header.title, {'type':10, 'start_time':pf4(header.start_time), 'end_time':pf4(header.end_time)})
    return json_response(resp) 

@login_required(2)
def store(request):
    current = 'inventory'
    resp = {'status': 1, 'info': {}, 'alert': ''}
    user = get_user(request)
    query = {'head_type':user.head_type}
    areas, companys, citys = [request.POST.get(i) for i in ['area', 'company', 'city']]
    if citys: query['city'] = {'$in':citys.split(',')}
    elif companys: query['company'] = {'$in':companys.split(',')}
    elif areas: query['area'] = {'$in':areas.split(',')}
    else:query['area'] = 0
    stores = Store.objects(__raw__=query)
    results = []
    for store in stores:
        results.append({
                        'id':str(store.id),
                        'city':store.city,
                        'no':store.no,
                        'name':store.name,
                        'address':store.address,
                        'opening_time':pf5(store.opening_time),
                        'store_manager':store.store_manager,
                        'mobile':store.mobile,
                        'device_count':store.device_count
                    })
    resp['results'] = results
    return json_response(resp)


@login_required(2)
def dump(request):
    current = 'inventory'
    user = get_user(request)
    header, oid = [request.POST.get(i) for i in ['header', 'oid']]
    oids = oid.split(',')
    header = InventoryHeader.objects.get(id=ObjectId(header))
    stores = Store.objects.filter(id__in=[ObjectId(i) for i in oids])
    
    workbook = xlwt.Workbook()
    store_codes = {}
    for index, store in enumerate(stores):

        if store_codes.get(store.name):
            store_codes[store.name] += 1
            store_name = u'{}({})'.format(store.name, store_codes[store.name])
        else:
            store_codes.update({store.name:1})
            store_name = store.name
       
        try:
            sheet = workbook.get_sheet(index)
            sheet.set_name(store_name)
        except Exception as e:
            workbook.add_sheet(store_name, cell_overwrite_ok=True)
            sheet = workbook.get_sheet(index)
           
        
        tops = [u'编号',u'说明',u'原值','COST CENTER Code',u'账面值',u'历史维修费用',u'购置日期',u'折旧起始日期',u'折旧结束日期',u'说明 2',u'供应商编号',u'维修供应商编号',u'负责人',u'搜索说明',u'折旧账簿代码',u'FA 过账组',u'折旧方法',u'折旧年数',u'折旧月份数',u'清理']
        for index3, top in enumerate(tops):
            sheet.col(index3).width   = 6000
            sheet.write(0, index3, top, xlwt.easyxf("pattern: pattern solid, fore_color red;font: color white;align: vertical center, horizontal center;"))

        sheet.row(0).height_mismatch = True
        sheet.row(0).height  = 600
        
        style1 = xlwt.easyxf("align: vertical center, horizontal center;")
        devices = InventoryDetail.objects.filter(header=header, store=store)
        for index2, device in enumerate(devices):
            index2 += 1
            sheet.row(index2).height_mismatch = True
            sheet.row(index2).height  = 400
            sub_device = device.device
            sheet.write(index2, 0, '', style1)
            sheet.write(index2, 1, '', style1)
            sheet.write(index2, 2, sub_device.amount, style1)
            sheet.write(index2, 3, store.no, style1)
            sheet.write(index2, 4, '', style1)
            sheet.write(index2, 5, sub_device.price, style1)
            sheet.write(index2, 6, pf2(sub_device.purchase_date), style1)
            sheet.write(index2, 7, store.opening_time, style1)
            
            sheet.write(index2, 8, '', style1)
            sheet.write(index2, 9, sub_device.name, style1)
            sheet.write(index2, 10, '', style1)
            sheet.write(index2, 11, '', style1)
            sheet.write(index2, 12, '', style1)
            sheet.write(index2, 13, '', style1)
            sheet.write(index2, 14, '', style1)
            sheet.write(index2, 15, '', style1)
            sheet.write(index2, 16, '', style1)
            sheet.write(index2, 17, '', style1)
            sheet.write(index2, 18, '', style1)
            sheet.write(index2, 19, '', style1)

            sheet.write(index2, 18, xlwt.Formula('R{}*12'.format(index2+1)))
            sheet.write(index2, 8, xlwt.Formula('DATE(YEAR(H{})+R{},MONTH(H{}),DAY(H{}))'.format(index2+1, index2+1, index2+1, index2+1)))
        

    response = HttpResponse(mimetype='application/vnd.ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=inventory.xls'   
    workbook.save(response)
    return response 




    

