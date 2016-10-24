#!/user/bin/env python
#encoding:utf-8

import os
import xlwt
from datetime import datetime as dt
from hashlib import md5
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect 
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache  
from apps.base.utils import login, pf2
from apps.base.common import get_user, json_response, get_json_data
from apps.base.common import admin_login_required as login_required
from apps.base.models import User, Device, Store, Brand, Product, Region
from settings import DEVICE_CATEGORY, DEVICE_TYPE, DB, ROOT_PATH, STATIC_ROOT
from bson.objectid import ObjectId 
from apps.base.logger import getlogger
from apps.base.push import push_message
from apps.base.forms import AssetsEditForm, StoreEditForm, AssetsStoreForm, AssetsSearchForm
from django.contrib import messages
from django.core.paginator import Paginator,InvalidPage,EmptyPage

logger = getlogger(__name__)  

@login_required(2)
def list(request):
    current = 'assets'
    user = get_user(request)
    city, page, category, efcategory, store, brand, product, area, company  = [request.GET.get(i) for i in ['region', 'page', 'category', 'efcategory', 'store', 'brand', 'product', 'area', 'company']]
    page  = int(page) if page else 1
    limit = 30
    query = {'head_type':user.head_type}
    if city:
        query['city'] = city
    if store:
        query['$or'] = [{'name':{'$regex':store}},{'no':{'$regex':store}}]
    if area:
        query['area'] = area
    if company:
        query['company'] = company
    res   = Store.objects(__raw__=query).order_by('city')
    paginator = Paginator(res,limit)
    total  = res.count()
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage):
        p = paginator.page(1)
    query = res[(page-1)*limit:page*limit] if res.count() > (page-1)*limit else res[0:limit]
    res = []
    for index, r in enumerate(query):
        if index%2 == 1:
            setattr(r, 'row_class', 'active')
        res.append(r)
    form = AssetsStoreForm(request.GET,user=user) 
    return render('store/{}_store_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def detail(request, oid):
    current = 'assets'
    user = get_user(request)  
    device = Device.objects.filter(head_type=user.head_type).get(id=ObjectId(oid))
    timers = device.assets()
    return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(2)
def edit(request, oid):
    current = 'assets'
    user = get_user(request)
    device  = Device.objects.filter(head_type=user.head_type).get(id=ObjectId(oid))
    timers  = device.assets()
    if request.method == 'GET':
        form    = AssetsEditForm(device.to_mongo())
        return render('store/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))

    form = AssetsEditForm(request.POST, oid=ObjectId(oid))
    if not form.is_valid():
        return render('store/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))

    data = form.cleaned_data
    for k, v in  data.items():
        if k == 'product':
            setattr(device, 'name', v.name)
            setattr(device, 'brand', v.brand.name)
            setattr(device, 'supplier', v.supplier)
        setattr(device,k,v)
    device.save()
    messages.success(request,u'修改成功')
    url = '/store/{}/detail/{}'.format(current, oid)
    return HttpResponseRedirect(url)

@login_required(2)
def append(request, oid):
    current = 'assets'
    user = get_user(request)
    store = Store.objects.get(id=ObjectId(oid))
    if request.method == 'GET':
        form    = AssetsEditForm()
        form.fields['store'].initial = str(store.id)
        return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

    form = AssetsEditForm(request.POST)
    if not form.is_valid():
        return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
    
    device = Device()
    setattr(device, 'store', store)
    setattr(device, 'head_type', store.head_type)
    data = form.cleaned_data
    for k, v in  data.items():
        setattr(device,k,v)
    device.save()
    messages.success(request,u'保存成功')
    url = '/store/{}/detail/{}'.format(current, device.id)
    return HttpResponseRedirect(url)


@login_required(2)
def store(request, oid):
    current = 'assets'
    user = get_user(request)
    res  = Store.objects.filter(head_type=user.head_type).get(id=ObjectId(oid))
    timers = res.status_list()
    form   = AssetsSearchForm(request.GET)
    device, category, ecategory, brand, product, supplier = [request.GET.get(i) for i in ['device', 'category', 'ecategory', 'brand', 'product', 'supplier']]
    query  = {'store':res.id}
    if device:
        query['$or'] = [{'name':{'$regex':device}},{'no':{'$regex':device}}]
    if category:
        query['category'] = category
    if ecategory:
        query['ecategory'] = ecategory
    if brand:
        query['brand'] = Brand.objects.get(id=ObjectId(brand)).name
    if product:
        query['product'] = {'$in':[i.id for i in Product.objects.filter(name=product)]}
    if supplier:
        query['supplier'] = ObjectId(supplier)
    devices = Device.objects(__raw__=query).order_by('-name')
    return render('store/{}_store_detail.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def store_edit(request, oid):
    current = 'assets'
    user  = get_user(request) 
    res    = Store.objects.filter(head_type=user.head_type).get(id=ObjectId(oid))
    timers  = res.status_list()
    if request.method == 'GET':
        form = StoreEditForm(res.to_mongo(), user=user)
        return render('store/{}_store_edit.html'.format(current),locals(),context_instance=RequestContext(request))

    form = StoreEditForm(request.POST, user=user, oid=res.id)
    if not form.is_valid(): 
        return render('store/{}_store_edit.html'.format(current),locals(),context_instance=RequestContext(request))

    data  = request.POST.dict()
    for k, v in  data.items():
        if k == 'cprovince':setattr(res, 'area', v)
        elif k == 'ccity':setattr(res, 'city', v) 
        elif k == 'carea':setattr(res, 'district', v)
        else:setattr(res,k,v)
    res.save()
    messages.success(request,u'修改成功')
    url = '/store/{}/store/{}'.format(current, oid)
    return HttpResponseRedirect(url)

@login_required(2)
def store_append(request):
    current = 'assets'
    user  = get_user(request) 

    if request.method == 'GET':
        form = StoreEditForm(user=user)
        return render('store/{}_store_append.html'.format(current),locals(),context_instance=RequestContext(request))

    form = StoreEditForm(request.POST, user=user)
    if not form.is_valid(): 
        return render('store/{}_store_append.html'.format(current),locals(),context_instance=RequestContext(request))

    store = Store()
    data  = request.POST.dict()
    setattr(store, 'head_type', user.head_type)
    for k, v in  data.items():
        setattr(store,k,v)
    store.save()
    messages.success(request,u'修改成功')
    url = '/store/{}/store/{}'.format(current, store.id)
    return HttpResponseRedirect(url)

@login_required(2)
def store_close(request, oid):
    current = 'assets'
    user    = get_user(request)
    res     = Store.objects.filter(head_type=user.head_type).get(id=ObjectId(oid))
    if request.method == 'POST':
        close_time = request.POST.get('close_time')
        res.close_time = close_time
        res.save()
    return json_response({'status':1})

@login_required(2)
def region(request):
    current = 'assets'
    user = get_user(request)
    name = request.POST.get('name')
    resp  = {'status':1, 'alert':''}
    city = Region.objects(__raw__={'name':name, 'rid':{'$regex':'c'}}).filter().first()
    results = []
    if city:
        for r in Region.objects(__raw__={'parent_id':city.rid, 'rid':{'$regex':'d'}}).order_by('-name'):
            results.append(r.name)
    resp['results'] = results
    return json_response(resp)

@login_required(2)
def qrcode(request):
    current = 'assets'
    user  = get_user(request)
    resp  = {'status':0, 'alert':''}
    if request.method == 'POST':
        data = get_json_data(request) or request.POST.dict()
        oid  = data.get('oid')
        workbook = xlwt.Workbook()
        if oid:
            sheet = workbook.add_sheet(u'二维码')
            oids = [ObjectId(i) for i in oid.split(',')]
            for index, oid in enumerate(oids):
                sheet.write(index, 0, str(ObjectId()))
        response = HttpResponse(mimetype='application/vnd.ms-excel')  
        response['Content-Disposition'] = u'attachment; filename=二维码列表.xls'   
        workbook.save(response)
        return response 

@login_required(2)
def dump(request):
    current = 'assets'
    user    = get_user(request)

    workbook = xlwt.Workbook()
    data = get_json_data(request) or request.POST.dict()
    oid  = data.get('oid')
    #oids = oid.split(',')
    oids = [str(item.id) for item in Store.objects.filter(head_type=2, city='上海市')]
    store_codes = {}
    for index, oid in enumerate(oids):
        store   = Store.objects.get(id=ObjectId(oid))
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

        sheet.write_merge(0, 3, 1, 15, 'Equipment Order List',  xlwt.easyxf("font:height 600;align: vertical center, horizontal center;"))
        sheet.insert_bitmap(os.path.join(ROOT_PATH, 'static/img/store/{}.bmp'.format(user.head_type)),  0, 1, 20, 5, 0.5, 2.7)
        sheet.write(0, 16, 'Rest. Name:')
        sheet.write(0, 17, store.name)
        sheet.write(1, 16, 'Rest. No.:')
        sheet.write(1, 17, store.no)
        sheet.write(2, 16, 'Rest. Opening Date:')
        sheet.write(2, 17, pf2(store.opening_time))
        sheet.write(3, 16, 'Author:')
        sheet.write(3, 17, u'Stephanie殷姿')


        sheet.row(4).height_mismatch = True
        sheet.row(4).height  = 600
        tops = [u'ID(请勿修改)',u'二维码ID(请勿修改)', u"编号\nItem", u"供应商\nSupplier", u"设备类别\nCategory", u"PO No.", u"设备名称\nDevice Name", u'设备生产序列号', u"描述\nDescription", u"品牌\nBrand", u"型号\nModel", u"规格\nSpecification", u"单位\nUnit",u"数量\nQty", u"单价\nUnit Price", u"合计\nAmount", u"税率\nTax Rate", u"合计（不含税)\nAmount w/o vat", u"税额\ntax", u"Fixed Asset", u"备注\nRemark"]

        for index2, top in enumerate(tops):
            sheet.col(index2).width   = 6000
            sheet.write(4, index2, top, xlwt.easyxf("pattern: pattern solid, fore_color red;font: color white;align: wrap on,vertical center, horizontal center;"))

        devices = Device.objects.filter(store=store)
        results = []

        keys  = ['id', 'rid', 'None', 'supplier', 'efcategory', 'po_no', 'name', 'psnumber', 'description', 'brand', 'model', 'specifications', 'unit', 'qty', 'price', 'amount', 'tax_rate', 'total', 'tax', 'fixed', 'remarks']
        for index3, device in enumerate(devices):
            for index4, key in enumerate(keys):
                if key == 'supplier':
                    val = device.supplier.name
                elif key == 'id':
                    val = str(device.id)
                elif key == 'fixed':
                    val = 'E1'
                else:
                    val = getattr(device, key, '')
                sheet.write(index3+5, index4, val)
    response = HttpResponse(mimetype='application/vnd.ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=assets.xls'
    workbook.save(response)
    return response 










    

