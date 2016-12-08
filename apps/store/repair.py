#encoding:utf-8
import xlwt
from xlutils.copy import copy 
from xlrd import open_workbook
from datetime import datetime as dt
from hashlib import md5
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache  
from apps.base.utils import login, pf6, pf7
from apps.base.common import get_user
from apps.base.common import admin_login_required as login_required
from apps.base.models import User, Maintenance, Device, Store, Product, Brand, Bill
from settings import *
from bson.objectid import ObjectId 
from apps.base.logger import getlogger
from apps.base.forms import AssetsEditForm, RepairSearchForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage

logger = getlogger(__name__)

@login_required(2) 
def list(request):
    current = 'repair'
    user = get_user(request)
    q, page, city, store, category, product, state, error_code, status, brand   = [request.GET.get(i) for i in ['q', 'page', 'region', 'store', 'category', 'product', 'state', 'error_code', 'status', 'brand']]
    page  = int(page) if page else 1
    limit = 30
    query = {'head_type':user.head_type}
    if user.category == '3':
        query['area'] = user.area
    if user.category == '4': 
        query['store'] = {'$in':user.store_id.split(',')}
    if q or q == '0':
        query['status'] = {'$in':[int(i) for i in q.split(',')]}
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
    if status:
        query['status'] = int(status)
    maintenance   = Maintenance.objects(__raw__=query).order_by('-create_time')
    paginator = Paginator(maintenance,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    maintenance = maintenance[(page-1)*limit:page*limit]
    res = []
    for index, qq in enumerate(maintenance):
        device = Device.objects.filter(id=ObjectId(qq.device)).first()
        if device:
            setattr(qq, 'device', device)
        index += 1
        if index%2 == 1:
            setattr(qq, 'row_class', 'active')
        res.append(qq)
    if query.get('status'):del query['status']
    new_call   = Maintenance.objects(__raw__=query).filter(status=0).count()
    step_call  = Maintenance.objects(__raw__=query).filter(status__in=[1,3,6,5]).count()
    hist_call  = Maintenance.objects(__raw__=query).filter(status__in=[-1,2,4]).count()
    form = RepairSearchForm()
    return render('store/{}_list.html'.format(current), locals(), context_instance=RequestContext(request))

@login_required(2)
def detail(request, oid):
    current = 'repair'
    user = get_user(request)
    res = Maintenance.objects.get(id=ObjectId(oid),head_type=user.head_type)
    store = Store.objects.get(id=ObjectId(res['store']))
    device    = Device.objects.get(id=ObjectId(res['device']))
    setattr(res, 'store', store)
    detail = res.get_result()
    bill   = res.bill.detail() if res.bill else {}
    return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))



@login_required(2)
def dump(request):
    current = 'repair'
    user = get_user(request)
    if request.method == 'POST': 
        rb = open_workbook(os.path.join(STATIC_ROOT, 'template/repair_template.xls'),formatting_info=True) 
        workbook = copy(rb) 
        sheet = workbook.get_sheet(0) 
        sheet.row(0).height_mismatch = True
        sheet.row(0).height  = 600
        style1 = xlwt.easyxf("pattern: pattern solid, fore_color red;font: color white;align: wrap on,vertical center, horizontal center;")
   
        q, start_day, end_day, sb, provider = [request.POST.get(i) for i in ['q', 'start_day', 'end_day', 'sb', 'provider']]
        query   = Maintenance.objects.order_by('-create_time')
        query   = query.filter(head_type=user.head_type)
        if user.category == '3':
            query = query.filter(area=user.area)
        if user.category == '4':
            query = query.filter(store__in=user.area.store_id.split(','))
        if provider:
            query = query.filter(company=provider)
        if sb:
            for kv in sb.split('|'):
                key, val = kv.split(':')
                if key == 'city':query = query.filter(city=val)
                if key == 'store':query = query.filter(store=val)
                if key == 'category':
                    products = Product.objects.filter(category=val)
                    query = query.filter(product_id__in=products)
                if key == 'brand':
                    brand = Brand.objects.get(id=ObjectId(val))
                    query = query.filter(brand=brand.name)
                if key == 'product':query = query.filter(product=val)
                if key == 'state':query = query.filter(state=int(val))
                if key == 'error_code':query = query.filter(error_code=val)
                if key == 'status':query = query.filter(status=int(val))
        if start_day:
            start_day = dt.strptime(start_day + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
            query = query.filter(create_time__gte=start_day)
        if end_day:
            end_day = dt.strptime(end_day + ' 23:56:56', '%Y-%m-%d %H:%M:%S')
            query = query.filter(create_time__lte=end_day)

        style = xlwt.easyxf("align: wrap on,vertical center, horizontal center;")
        for col_index in range(60):
            sheet.col(col_index).width   = 6000

        sheet.row(1).height_mismatch = True 
        sheet.row(1).height  = 600  

        index = 0
        for q in query:
            bill = Bill.objects.filter(maintenance=q).first()
            spares = [-1]
            if bill:
                detail = bill.detail()
                spares = detail.get('spare', [])
                if not spares:
                    spares = [-1]

            for spare_index, spare in enumerate(spares):

                sheet.row(index+2).height_mismatch = True
                sheet.row(index+2).height  = 600
                device = Device.objects.filter(id=ObjectId(q.device)).first()
                if not device:
                    continue
                sheet.write(index+2, 0, q.code, style)
                sheet.write(index+2, 1, q.statuss, style)
                sheet.write(index+2, 2, q.city, style)
                sheet.write(index+2, 3, device.store.no, style)
                sheet.write(index+2, 4, q.store_name, style)
                
                sheet.write(index+2, 5, device.store.opening_time.strftime('%Y-%m-%d'), style)
                sheet.write(index+2, 6, device.category, style)
                sheet.write(index+2, 7, device.brand, style)
                sheet.write(index+2, 8, device.name, style)

                sheet.write(index+2, 9, device.model, style)
                sheet.write(index+2, 10, device.psnumber, style)
                if not isinstance(device.guarantee_time, int):
                    sheet.write(index+2, 11, device.guarantee_time.strftime('%Y-%m-%d'), style)
                sheet.write(index+2, 12, '', style)

                sheet.write(index+2, 13, q.states, style)
                sheet.write(index+2, 14, q.content, style)

                sheet.write(index+2, 15, q.create_time.strftime('%Y-%m-%d'), style)
                sheet.write(index+2, 16, q.create_time.strftime('%H:%M'), style)
                target_user = q.grab_user 

                if target_user:
                    sheet.write(index+2, 17, target_user.name, style)
                    sheet.write(index+2, 18, target_user.username, style)
                    sheet.write(index+2, 19, u"{} {}".format(target_user.company, target_user.city), style)

                sheet.write(index+2, 20, q.must_time.strftime('%Y-%m-%d %H:%M') if q.must_time else '', style)
                sheet.write(index+2, 21, q.come_time.strftime('%Y-%m-%d %H:%M') if q.come_time else '', style)
                sheet.write(index+2, 22, q.arrival_time.strftime('%Y-%m-%d %H:%M') if q.arrival_time else '' ,style)

                stop_status = ''
                if q.stop == -1:
                    stop_status = u'申请暂停'
                elif q.stop == 0:
                    stop_status = u'确认暂停'
                elif q.stop == -2:
                    stop_status = u'否决暂停'

                sheet.write(index+2, 23, stop_status, style)
                sheet.write(index+2, 24, u"{} {}".format(q.stop_content if q.stop_content else '',q.stop_reason if q.stop_reason else ''), style)
                if q.stop_day:
                    sheet.write(index+2, 25, q.stop_day.strftime('%Y-%m-%d'), style)
                    sheet.write(index+2, 26, q.stop_day.strftime('%H:%M'), style)
                    if q.arrival_time:
                        sheet.write(index+2, 27, q.arrival_time.strftime('%Y-%m-%d %H:%M'), style)
                if q.stop_day and q.stop == 0:
                    if q.stop_come_time and q.stop_come_time > q.stop_day:
                        sheet.write(index+2, 28, u'否', style)
                        sheet.write(index+2, 29, pf6((pf7(q.stop_come_time) - pf7(q.stop_day))), style)
                    if q.stop_come_time and q.stop_come_time <= q.stop_day:
                        sheet.write(index+2, 28, u'是', style)
                        sheet.write(index+2, 29, pf6((pf7(q.stop_come_time) - pf7(q.stop_day))), style)
                else:
                    if q.come_time and q.must_time:
                        #come_time = q.must_time if q.must_time > q.come_time else q.come_time
                        come_time = q.must_time
                        if q.arrival_time and q.arrival_time > come_time:
                            sheet.write(index+2, 28, u'否', style)
                            sheet.write(index+2, 29, pf6((pf7(q.arrival_time) - pf7(come_time))), style)
                        if q.arrival_time and q.arrival_time <= come_time:
                            sheet.write(index+2, 28, u'是', style)
                            sheet.write(index+2, 29, pf6((pf7(q.arrival_time) - pf7(come_time))), style)
                if q.later:sheet.write(index+2, 30, q.later, style)
                sheet.write(index+2, 31, q.work_range, style)
               
                if q.arrival_time and q.work_time and bill:
                    sheet.write(index+2, 32, bill.create_time.strftime('%Y-%m-%d %H:%M'), style)
                    sheet.write(index+2, 33, pf6((pf7(bill.create_time)-pf7(q.arrival_time))), style)
                    if q.stop == 0:
                        base_work_time = q.stop_day + timedelta(hours=q.work_range)
                    else:
                        base_work_time = q.must_time + timedelta(hours=q.work_range)

                    sheet.write(index+2, 34, u'否' if (pf7(bill.create_time)-pf7(base_work_time)) > 0 else u'是', style)
                    sheet.write(index+2, 35, pf6((pf7(bill.create_time)-pf7(base_work_time))), style)

                
                if bill:
                    detail = bill.detail() 
                    sheet.write(index+2, 36, bill.analysis, style)
                    sheet.write(index+2, 37, bill.measures, style)
                    sheet.write(index+2, 38, u'维修成功' if bill.state == 1 else u'维修失败', style)

                    sheet.write(index+2, 39, bill.reason, style)
                    sheet.write(index+2, 40, q.manager_content, style)
                    
                    if spare <> -1:
                        sheet.write(index+2, 41, spare.get('name'), style)
                        sheet.write(index+2, 42, u'保固期内' if spare.get('status') == 1 else u'保固期外', style)
                        sheet.write(index+2, 43, spare.get('price'), style)
                        sheet.write(index+2, 44, spare.get('count'), style)
                        sheet.write(index+2, 45, spare.get('total',0), style)

                    if spare_index == 0:

                        sheet.write(index+2, 46, bill.stay_total, style)
                        sheet.write(index+2, 47, bill.labor, style)
                        sheet.write(index+2, 48, bill.travel, style)
                        sheet.write(index+2, 49, '', style)
                        sheet.write(index+2, 50, detail.get('spare_total',0)+bill.stay_total+bill.labor+bill.travel, style)
                        sheet.write(index+2, 51, bill.opt_user.name, style)
                        sheet.write(index+2, 52,  bill.opt_user.username, style)
                        sheet.write(index+2, 53, bill.confirm_time.strftime('%Y-%m-%d %H:%M') if bill.confirm_time else '', style) 

                        sheet.write(index+2, 54, '', style)
                        sheet.write(index+2, 55, '', style)
                        sheet.write(index+2, 56, '', style)
                        sheet.write(index+2, 57, '', style)
                        sheet.write(index+2, 58, '', style)
                        sheet.write(index+2, 59, '', style)
                        sheet.write(index+2, 60, q.message, style)
                        
                index += 1


    
        response = HttpResponse(mimetype='application/vnd.ms-excel') 
        response['Content-Disposition'] = 'attachment; filename=repair.xls' 
        workbook.save(response)
        return response 
    


    

