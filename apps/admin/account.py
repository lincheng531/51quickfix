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
from apps.base.models import User, Supplier, Store
from apps.base.sms import send_sms
from apps.base.forms import VerifyForm, SearchProductForm, SearchAccountForm, AccountAppendForm, AccountAppend1Form, AccountPassword, AccountEditForm
from django.contrib import messages
from settings import *
from apps.base.messages import *
from django.core.paginator import Paginator,InvalidPage,EmptyPage

logger = getlogger(__name__)


@login_required(1)
def list(request, category, status):
    current = 'account'
    page    = int(request.GET.get('page',1))
    city, tag = [request.GET.get(i) for i in ['region','tag']]
    page    = page if page >1 else 1
    limit   = 20
    status  = int(status)
    query   = {'category':category}
    sort    = [('update_time',-1)]
    suf_fix = ''
    if city:
        query['city'] = city
    query_or = []
    if tag:
        stores = Store.objects.filter(__raw__={'$or':[{'name':{'$regex':tag}},{'no':{'$regex':tag}}]})
        query_or.extend([
                            {'city':{'$regex':tag}}, 
                            {'store_id':{'$in':[str(i.id) for i in stores]}},
                            {'name':{'$regex':tag}},
                            {'mobile':{'$regex':tag}},
                            {'username':{'$regex':tag}}
                        ])

    if status  == 2:
        query['is_active'] = -1 
        query['is_update'] = True
    else:
        query['is_active'] = status
    if query_or: query['$or'] = query_or
    users = User.objects(__raw__=query).order_by('-create_time').skip((page-1)*limit).limit(limit)
    paginator = Paginator(DB.user.find(query,fileds=['_id']),limit)

    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage):
        raise Http404

    res = []
    for user in users:
        if user.store_id:
            store = Store.objects.filter(id=ObjectId(user.store_id)).first()
            if store and not store.is_active:
                user.is_active = 2
        res.append(user)
    
    form = SearchAccountForm()
    pre_fix = 'admin/{}/list'.format(current)
    n = 12
    l = page - (n/2) > 0 and page - (n/2) or 0
    r = l + n
    pages = range(1,paginator.num_pages + 1,)[l:r]
    
    return render('admin/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(1)
def active(request, oid, category):
    current = 'account'
    user = User.objects.get(id=ObjectId(oid), head_type=1)
    category = int(category)
    if user.store_id and category:
        store = Store.objects.get(id=ObjectId(user.store_id))
        if not store.is_active:
            messages.success(request,u'请先去审核通过该餐厅')
            return render('admin/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))
    setattr(user, 'is_active', category if category <> 2 else -1)
    user.save()
    send_sms(user.username, u'【51快修】{} 您的账号:{}审核通过!'.format(user.name, user.username))
    return HttpResponseRedirect('/admin/account/detail/{}'.format(user.id))


@login_required(1)
def detail(request, oid):
    current = 'account'
    user         = User.objects.get(id=ObjectId(oid))
    if user.store_id:
        store = Store.objects.filter(id=ObjectId(user.store_id)).first()
        if store and not store.is_active:
            user.is_active = -1
    if request.method == 'POST':
        is_active  = 1
        data = request.POST.dict()
        train_type, train_name, train_day1, train_day2, train_msg, train_brand, train_category = [], [], [], [], [], [], []
        for index, train in enumerate(user.train):
            train_type.append(data.get('train_type_{}'.format(index),''))
            train_name.append(data.get('train_name_{}'.format(index),''))
            train_day1.append(data.get('train_day1_{}'.format(index),''))
            train_day2.append(data.get('train_day2_{}'.format(index),''))
            train_msg.append(data.get('train_msg_{}'.format(index),''))
            train_brand.append(data.get('train_brand_{}'.format(index),''))
            train_category.append(data.get('train_category_{}'.format(index),''))

        setattr(user, 'train_name', train_name)
        setattr(user, 'train_day1', train_day1)
        setattr(user, 'train_day2', train_day2)
        setattr(user, 'train_msg', train_msg)
        setattr(user, 'train_type', train_type)
        setattr(user, 'train_brand', train_brand)
        setattr(user, 'train_category', train_category)
        if -1 in train_type or '-1' in train_type: is_active = -1

        for k,v in data.iteritems():
            if not k.startswith('train'):
                if k.find('type') > -1 and v == '-1':
                    is_active = -1
                setattr(user, k, v)
        setattr(user, 'is_active', is_active)
        if is_active == 1 and ENV <> 'TEST':
            send_sms(user.username, u'【51快修】{} 您的账号:{}审核通过!'.format(user.name, user.username))

        user.save()
        messages.success(request, u'修改成功')
    items =  user.to_mongo()
    p = lambda x, y: x[y] if len(x) >y else ''
    for index, train in enumerate(user.train):
        items['train_name_{}'.format(index)] = p(user.train_name,index)
        items['train_day1_{}'.format(index)] = p(user.train_day1,index)
        items['train_day2_{}'.format(index)] = p(user.train_day2,index)
        items['train_msg_{}'.format(index)] =  p(user.train_msg,index)
        items['train_type_{}'.format(index)] =  p(user.train_type,index)
        items['train_brand_{}'.format(index)] = p(user.train_brand,index)
        items['train_category_{}'.format(index)] = p(user.train_category,index)
    if user.category <> '1':
        form = AccountEditForm(items, user=user)
    return render('admin/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(1)
def delete(request,oid):
    current = 'account'
    resp = {'status':0,'info':{},'alert':''}
    DB.user.remove({'_id':ObjectId(oid)})
    url = '/admin/{}/list'.format(current)
    return HttpResponseRedirect(url)


@login_required(1)
def profile(request):
    current = 'account'
    res = get_user(request)
    if request.method == 'POST':
        form = AccountPassword(request.POST)
        if not form.is_valid():
            return render('admin/{}_profile.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        res.set_password(data.get('password'))
        res.save()
        messages.success(request, u'修改密码成功')
        return HttpResponseRedirect('/admin/account/profile')
    form = AccountPassword()
    return render('admin/{}_profile.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(1)
def append(request):
    current = 'account'
    
    if request.method == 'GET':
        form = AccountAppendForm()
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

    form = AccountAppendForm(request.POST)
    if not form.is_valid():
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

    data = form.cleaned_data
    store = DB.store.find_one({'no':data['no']})
    if not store:
        messages.error(request,u'找不到该编号的餐厅')
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
    try:
        items = {
                u'store_id': str(store['_id']),
                u'is_staff': False, 
                u'user_permissions': [], 
                u'category': u'1', 
                u'city': store['city'], 
                u'area': u'华东区', 
                u'avatar_img': u'/static/img/store/2.png', 
                u'head_type': 2, 
                u'store': store['address'], 
                u'username': data['mobile'], 
                u'company_logo': u'/static/img/store/2.png', 
                u'company': u'汉堡王', 
                u'is_active': 1,
                u'password': u'pbkdf2_sha256$12000$tRaMa5pqFWm6$2o4ZCrDiikNRsQ9YUs4ZD0P/aYjZjjf6Zm8v3Rb9mWs=', 
                u'source': u'汉堡王',
                u'name': data['name'], 
                u'mobile': data['mobile'], 
                u'create_time': dt.now(),
                u'update_time': dt.now(),
                u'_cls': u'User.User'
                }
        user = DB.user.find_one({'username':data['mobile']})
        if not user:
            DB.user.save(items)
        else:
            DB.user.update({'username':data['mobile']},{'$set':items})
    except Exception,e:
        messages.error(request,e.message)
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
    else:
        messages.success(request,u'保存成功')
    
    url = '/admin/{}/detail/{}'.format(current, user['_id'])
    return HttpResponseRedirect(url)



@login_required
def append1(request):
    current = 'account'

    def _create_user(DB, name, mobile, category, works, area, city, electrician, refrigeration, service_provider):

        user   = DB.user.find_one({'username':mobile})
        if not user:
            item   = {
                        '_cls':'User.User',
                        'user_permissions':[],
                        'username':mobile,
                        'name':name,
                        'works':works,
                        'source':service_provider,
                        'area':area,
                        'city':city,
                        'mobile':mobile,
                        'company':service_provider,
                        'company_log':'/static/img/store/2.png',
                        'avatar_img':'/static/images/avatar_l.png',
                        'category':category,
                        'electrician_no':electrician,
                        'refrigeration_no':refrigeration,
                        'is_active':1,
                        'is_staff':False,
                        'is_superuser':False,
                        'is_update':False,
                        'head_type':2,
                        'create_time':dt.now(),
                        'update_time':dt.now(),
                        'password':u'pbkdf2_sha256$12000$Gld2R6H1WLz1$ftuGiMCxggl5D7utqdzCn/KXPLsaFEm//Xdyw6DlHBE='
                    }
            uid = DB.user.save(item)
        else:
            uid = user['_id']
            DB.user.update({'username':mobile},{'$set':{'update_time':dt.now()}})
        return uid
    
    if request.method == 'GET':
        form = AccountAppend1Form()
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

    form = AccountAppend1Form(request.POST)
    if not form.is_valid():
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
    
    data = form.cleaned_data
    try:
        area, city, company, provider_manager_name, provider_manager_mobile, service_name, service_mobile, electrician , refrigeration  ,area_manager_name, area_manager_mobile = \
        [data.get(i) for i in ['area', 'city', 'company', 'provider_manager_name', 'provider_manager_mobile', 'service_name', 'service_mobile', 'electrician', 'refrigeration', 'area_manager_name', 'area_manager_mobile']]
        works = []
        if electrician:
            works.append(u'电工证')
        if refrigeration:
            works.append(u'制冷正')

        opt_user = _create_user(DB, provider_manager_name, provider_manager_mobile, '2', works, area, city, electrician, refrigeration, company)
        user = _create_user(DB, service_name, service_mobile, '0', works, area, city, electrician, refrigeration, company)

        if not DB.member.find_one({'opt_user':opt_user, 'user':user}):
            DB.member.save({
                    'category':2,
                    'update_time':dt.now(),
                    'area':area,
                    'city':city,
                    'company':company,
                    'opt_user':opt_user,
                    'create_time':dt.now(),
                    'user':user,
                    'active':1,
                    'head_type':2,
                    'store':u'汉堡王'
                })
        acrea_manager = {u'华北区':[u'周文辉','13585753381'],u'华东区':[u'邱渊','18221168715'],u'华南区':[u'周文辉','13585753381'],u'加盟区':[u'周文辉','13585753381']}
        DB.push.save({
                    'area':area,
                    'city':city,  
                    'company':company,
                    'head_type':2,          
                    'provider': str(opt_user),           
                    'service': str(user),   
                    'area_manager':[area_manager_name, area_manager_mobile],  
                    'manager': acrea_manager.get(area),          
                    'hq':[u'周文辉', '13585753381']               
            })
    except Exception,e:
        messages.error(request,e.message)
        return render('admin/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
    else:
        messages.success(request,u'保存成功')
    
    url = '/admin/{}/detail/{}'.format(current, user)
    return HttpResponseRedirect(url)





