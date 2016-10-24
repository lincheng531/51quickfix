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
from apps.base.models import User, Call
from settings import *
from bson.objectid import ObjectId 
from apps.base.forms import CallEditForm
from apps.base.common import get_user, get_pinyin_initials



@login_required(2)
def list(request):
    current = 'call'
    user = get_user(request)
    page = request.GET.get('page', 0)
    page  = int(page) if page else 1
    tag = request.GET.get('tag')
    query = {'head_type':user.head_type}
    if tag:
        query['$or'] = [
                        {'name':{'$regex':tag}}, 
                        {'brand_name':{'$regex':tag}}, 
                        {'city':{'$regex':tag}},
                        {'warranty_in':{'$regex':tag}},
                        {'warranty_out1':{'$regex':tag}},
                        {'warranty_out2':{'$regex':tag}},
                        {'warranty_out3':{'$regex':tag}},

                        ]
    limit = 30
    query  = Call.objects(__raw__=query).order_by('-create_time')
    paginator = Paginator(query,limit)
    try :
        p = paginator.page(page)
    except(InvalidPage,EmptyPage): 
        p = paginator.page(1)
    res = query[(page-1)*limit:page*limit] if query.count() > (page-1)*limit else query[0:limit]
    return render('store/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def append(request):
    current = 'call'
    user = get_user(request)
    form = CallEditForm(request.GET) 
    if request.method == 'POST':
        form = CallEditForm(request.POST, category='append')
        if not form.is_valid():
            return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        call = Call()
        setattr(call, 'head_type', user.head_type)
        for k, v in data.iteritems():
            setattr(call, k, v)
        call.save()
        messages.success(request,u'保存成功')
    return render('store/{}_append.html'.format(current),locals(),context_instance=RequestContext(request))


@login_required(2)
def detail(request, oid):
    current = 'call'
    user  = get_user(request)
    call  = Call.objects.get(id=ObjectId(oid),head_type=user.head_type)
    form  = CallEditForm(call.to_mongo())
    if request.method == 'POST':
        form = CallEditForm(request.POST)
        if not form.is_valid():
            return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))
        data = form.cleaned_data
        for k, v in data.iteritems():
            setattr(call, k, v)
        call.save()
        messages.success(request,u'更新成功')
    return render('store/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))





    

