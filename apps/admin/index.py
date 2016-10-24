#encoding:utf-8

from hashlib import md5
from bson.objectid import ObjectId
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache
from apps.base.utils import login as _login
from django.contrib.auth import logout as _logout
from apps.base.models import User
from apps.base.forms import StuffLoginForm as LoginForm
from django.contrib.auth import authenticate
from django.contrib import messages
from apps.base.logger import getlogger
from settings import *
logger = getlogger(__name__)
    
def logout(request):
    _logout(request)
    return HttpResponseRedirect('/admin/')


def login(request):
    title = u'请用管理员账号登录'
    

    if request.method == 'GET':
        form = LoginForm()
        return render('login.html',locals(),context_instance=RequestContext(request))
    
    form = LoginForm(request.POST)
    if not form.is_valid():
        return render('login.html',locals(),context_instance=RequestContext(request))

    form_data = form.cleaned_data
    
    user =  authenticate(**form_data)
    if not user:
        messages.error(request,u'密码错误')
        return render('login.html',locals(),context_instance=RequestContext(request))
        
    if not user.is_superuser:
        messages.error(request,u'你不是管理员，禁止登录')
        return render('admin/login.html', locals(), context_instance=RequestContext(request))
        
    if not user.is_active:
        messages.error(request,u'你已经被禁止登录')
        return render('admin/login.html', locals(), context_instance=RequestContext(request))

    user.backend = 'mongoengine.django.auth.MongoEngineBackend'
    _login(request,user)
    messages.success(request,u'欢迎你，管理员 {}，请保护好你的账号密码切勿泄露'.format(user.name or user.username))
    urls = {1:'/admin/', 2:'/store/', 3:'/provider/repair/list?q=0'}
    return HttpResponseRedirect(urls.get(user.is_superuser))
