#encoding:utf-8
from datetime import datetime as dt
from hashlib import md5
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache  
from apps.base.common import admin_login_required as login_required
from apps.base.common import get_user, json_response
from apps.base.models import User, Store, Role, UserRole
from apps.base.forms import StoreAccountAppendForm, StorePassword
from django.contrib import messages
from settings import *
from bson.objectid import ObjectId 
from apps.base.logger import getlogger
from django.core.paginator import Paginator,InvalidPage,EmptyPage

logger = getlogger(__name__)

@login_required(2) 
def list(request):
    current = 'account'
    user = get_user(request)
    q = request.GET.get('q')
    tag = request.GET.get('tag')
    page = int(request.GET.get('page', 1))
    limit = 30
    query = {'head_type':user.head_type}
    if q: query['category'] = q
    if tag:
        stores = Store.objects(__raw__={'$or':[{'name':{'$regex':tag}}, {'no':{'$regex':tag}}]})
        query['$or'] = [
                        {'store_id':{'$in':[str(i.id) for i in stores]}}, 
                        {'city':{'$regex':tag}}, 
                        {'name':{'$regex':tag}}, 
                        {'username':{'$regex':tag}}
                        ]
    query = User.objects(__raw__=query)
    if user.category == '4':
        ids = []
        for store_id in  user.store_id.split(','):
            ids.extend([i.id for i in User.objects.filter(store_id=store_id, head_type=user.head_type, category='1')])
        query = query.filter(id__in=ids)
    elif user.category == '3':
        ids = []
        stores = Store.objects.filter(area=user.area)
        for store in stores:
            ids.extend([i.id for i in User.objects(__raw__={'store_id':{'$regex':str(store.id)}, 'category':{'$in':['1', '4']}})])
        query = query.filter(id__in=ids)
    query = query.order_by('-create_time')
    paginator = Paginator(query,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    querys = query[(page-1)*limit:page*limit]
    res = []
    for query in querys:
        if query and query.store_id and query.category<>'4':
            store = Store.objects.filter(id=ObjectId(query.store_id)).first()
            if store:
                setattr(query, 'store', store)
        res.append(query)
    return render('store/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(2)
def detail(request, oid):
    current = 'account'
    user = get_user(request)
    res  = User.objects.get(id=ObjectId(oid), head_type=user.head_type)
    if res.category == '1':
        store = Store.objects.filter(id=ObjectId(res.store_id)).first()
        res['store'] = store
    elif res.category == '4' and res.store_id:
        store = Store.objects.filter(id__in=[ObjectId(i) for i in res.store_id.split(',')])
        res['store'] = store
    return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def edit(request, oid):
    current = 'account'
    user    = get_user(request)
    curr_user = User.objects.get(id=ObjectId(oid), head_type=user.head_type)
    category  = curr_user.category
    if request.method == 'POST':
        form = StoreAccountAppendForm(request.POST, category=category, head_type=user.head_type, store_id=curr_user.store_id, method='update')
        if not form.is_valid():
            return render('store/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        for name, val in data.iteritems():
            if name == 'password':
                if val: 
                    curr_user.set_password(val)
            elif name == 'mobile':
                if val <> curr_user.username:
                    setattr(curr_user, 'username', val)
                    setattr(curr_user, 'mobile', val)
            else:
                if name == 'store' and category == '4' and val:
                    setattr(curr_user, 'store_id', ','.join([str(i.id) for i in val]))
                    setattr(curr_user, 'store', ','.join([i.name for i in val]))
                elif name == 'store' and category == '1' and val:
                    setattr(curr_user, 'store_id', str(val.id))
                    setattr(curr_user, 'store', val.name)
                else:
                    setattr(curr_user, name, val)
        curr_user.save()
        messages.success(request, u'更新成功')
        return HttpResponseRedirect('/store/account/detail/{}'.format(curr_user.id))

    items  = curr_user.to_mongo()
    if category == '1':
        items['store'] = items['store_id']
    elif category == '4' and items.get('store_id'):
        items['store'] = [str(i.id) for i in Store.objects.filter(id__in=[ObjectId(i) for i in items['store_id'].split(',')])]
        print items['store']
    del items['password']
    form   = StoreAccountAppendForm(items, category=category, head_type=user.head_type, store_id=curr_user.store_id, method='view')
    return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(2)
def active(request, oid, category):
    current = 'account'
    user = get_user(request)
    if category in ['0', '1']:
        curr_user = User.objects.get(id=ObjectId(oid))
        curr_user.is_active = int(category)
        curr_user.save()
    return HttpResponseRedirect('/store/account/list')

@login_required(2)
def profile(request):
    current = 'account'
    res = get_user(request)
    if request.method == 'POST':
        form = StorePassword(request.POST)
        if not form.is_valid():
            return render('store/{}_profile.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        res.set_password(data.get('password'))
        res.save()
        messages.success(request, u'修改密码成功')
        return HttpResponseRedirect('/store/account/profile')

    form = StorePassword()
    if res.category == '1':
        store = Store.objects.get(id=ObjectId(res.store_id))
        res['store'] = store
    elif res.category == '4' and res.store_id:
        store = Store.objects.filter(id__in=[ObjectId(i) for i in res.store_id.split(',')])
        res['store'] = store
    
    return render('store/{}_profile.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(2)
def append(request, category):
    current = 'account'
    user    = get_user(request)
    if user.category == '4' and category <> '1':
        messages.success(request,u'无该权限')
        return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
    
    if user.category == '3' and category not in  ['1', '4']:
        messages.success(request,u'无该权限')
        return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

    form = StoreAccountAppendForm(category=category, head_type=user.head_type, store_id=user.store_id, method='view')
    if request.method == 'POST' and category in ['1', '3', '4', '5']:
        form = StoreAccountAppendForm(request.POST, category=category, head_type=user.head_type, store_id=user.store_id, method='save')
        if not form.is_valid():
            return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        append_user = User.objects.filter(username=data['mobile']).first()
        if append_user and append_user.head_type <> user.head_type:
            messages.success(request,u'该用户已经存在，你没有迁移该用户的权限，请联系管理员')
            return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))

        items = {
                    'is_staff': False, 
                    'user_permissions': [], 
                    'category': category, 
                    'avatar_img': user.avatar_img, 
                    'head_type': user.head_type, 
                    'username': data['mobile'], 
                    'company_logo': user.company_logo, 
                    'company':user.company, 
                    'is_active': 1,
                    'source': user.source,
                    'name': data['name'], 
                    'mobile': data['mobile'],
                    'is_superuser':0 if category == '1' else 2
                }
        if category == '1':
            if data['store']:
                items['store_id'] = str(data['store'].id)
                items['store'] = data['store'].name
                items['city'] = data['store'].city
                items['area'] = data['store'].area
                items['address'] = data['store'].address
        elif category == '3':
            items['area'] = data['area']
        elif category == '4':
            items['store_id'] = ','.join([str(i.id) for i in data['store']])
            items['store'] = ','.join([i.name for i in data['store']])
        if not append_user:
            append_user = User()
        for k,v in items.iteritems():
            setattr(append_user, k, v)
        append_user.set_password(data['password'])
        append_user.save()
        messages.success(request,u'保存成功')
        if category == '5':
            for role in Role.objects.filter():
                UserRole(user=append_user, role=role).save()
        return HttpResponseRedirect('/store/account/detail/{}'.format(append_user.id))
    else:
        messages.success(request,u'手机号码不得重复')
    return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))



