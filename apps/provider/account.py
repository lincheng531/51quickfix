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
from apps.base.models import User, Store, Role, UserRole, Member
from apps.base.forms import ProviderAccountAppendForm, StorePassword
from django.contrib import messages
from settings import *
from bson.objectid import ObjectId 
from apps.base.logger import getlogger
from django.core.paginator import Paginator,InvalidPage,EmptyPage

logger = getlogger(__name__)

@login_required(3) 
def list(request):
    current = 'account'
    user = get_user(request)
    q = request.GET.get('q', '1')
    page = int(request.GET.get('page', 1))
    limit = 30 
    query = {'company':user.company, 'category':q}
    query     = User.objects(__raw__=query).order_by('-create_time')
    paginator = Paginator(query,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    res = query[(page-1)*limit:page*limit]
    return render('provider/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(3)
def detail(request, oid):
    current = 'account'
    user = get_user(request)
    res  = User.objects.get(id=ObjectId(oid), company=user.company)
    print '>'*10, Member.objects.filter(opt_user=res)
    setattr(res, 'repair_user', Member.objects.filter(opt_user=res))
    return render('provider/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(3)
def edit(request, oid):
    current = 'account'
    user    = get_user(request)
    curr_user = User.objects.get(id=ObjectId(oid), company=user.company)
    category  = curr_user.category
    if request.method == 'POST':
        form = ProviderAccountAppendForm(request.POST, category=category, company=curr_user.company, method='update')
        if not form.is_valid():
            return render('provider/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        for name, val in data.iteritems():
            if name == 'password':
                if val: 
                    curr_user.set_password(val)
            elif name == 'mobile':
                if val <> curr_user.username:
                    setattr(curr_user, 'username', val)
                    setattr(curr_user, 'mobile', val)
            elif name == 'repair_user':
                Member.objects(opt_user=curr_user).delete()
                for v in val:
                    Member(**{
                            'opt_user':curr_user, 'user':User.objects.get(id=ObjectId(v)), 
                            'city':data['city'], 'company':curr_user.company
                        }).save()
            else:
                setattr(curr_user, name, val)
        curr_user.save()
        messages.success(request, u'更新成功')
        return HttpResponseRedirect('/provider/account/detail/{}'.format(curr_user.id))

    items  = curr_user.to_mongo()
    del items['password']
    if category == '2':
        items['repair_user'] = [str(i.user.id) for i in Member.objects.filter(opt_user=curr_user)]
    form   = ProviderAccountAppendForm(items, category=category, company=curr_user.company, method='view')
    return render('provider/{}_edit.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(3)
def active(request, oid, category):
    current = 'account'
    user = get_user(request)
    if category in ['0', '1']:
        curr_user = User.objects.get(id=ObjectId(oid))
        curr_user.is_active = int(category)
        curr_user.save()
    return HttpResponseRedirect('/provider/account/list?q=0')

@login_required(3)
def profile(request):
    current = 'account'
    res = get_user(request)
    if request.method == 'POST':
        form = StorePassword(request.POST)
        if not form.is_valid():
            return render('provider/{}_profile.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        res.set_password(data.get('password'))
        res.save()
        messages.success(request, u'修改密码成功')
        return HttpResponseRedirect('/provider/account/profile')

    form = StorePassword()
    if res.category == '1':
        store = Store.objects.get(id=ObjectId(res.store_id))
        res['store'] = store
    elif res.category == '4' and res.store_id:
        store = Store.objects.filter(id__in=[ObjectId(i) for i in res.store_id.split(',')])
        res['store'] = store
    
    return render('provider/{}_profile.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(3)
def append(request, category):
    current = 'account'
    user    = get_user(request)
    form    = ProviderAccountAppendForm(category=category, company=user.company, method='view')
    if request.method == 'POST' and category in ['2', '0']:
        form = ProviderAccountAppendForm(request.POST, category=category, company=user.company, method='save')
        if not form.is_valid():
            return render('provider/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        if not User.objects.filter(username=data['mobile']).first(): 
            items = {
                    'is_staff': False, 
                    'user_permissions': [], 
                    'category': category, 
                    'avatar_img': user.avatar_img, 
                    'head_type': user.head_type, 
                    'username': data['mobile'], 
                    'company_logo': user.company_logo, 
                    'company':user.company,
                    'area':user.area, 
                    'is_active': 1,
                    'city':data['city'],
                    'source': user.source,
                    'name': data['name'], 
                    'mobile': data['mobile'],
                    'is_superuser':None
                    }
            user = User()
            for k, v in items.iteritems():
                if k == 'repair_user':
                    for vv in v:
                        Member(**{
                                    'opt_user':user,
                                    'user':User.objects.get(id=ObjectId(vv)),
                                    'category':category,
                                    'city':data['city'],
                                    'company':user.company
                            }).save()
                else: 
                    setattr(user, k, v)
            user.set_password(data['password'])
            user.save()
            messages.success(request,u'保存成功')
            return HttpResponseRedirect('/provider/account/detail/{}'.format(user.id))
        else:
            messages.success(request,u'手机号码不得重复')
    return render('provider/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))



