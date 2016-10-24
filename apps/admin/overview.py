#encoding:utf-8
from hashlib import md5
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache
from apps.base.utils import login
from apps.base.common import admin_login_required as login_required
from apps.base.models import User
from settings import *
from bson.objectid import ObjectId

@login_required(1)
def index(request):

    return render('admin/index.html', locals(),context_instance=RequestContext(request))

@login_required(1)
def overview(request):
    current = 'overview'
    uname = request.GET.get('uname')
    if uname:
        user = User.objects.get(username=uname)
        login(request,user)

    res = []

    # total account
    res.append({'name':u'总注册账号数','value':DB.user.count()})
    res.append({'name':u'总叫修数','value':DB.maintenance.count()})
    res.append({'name':u'总维修单数','value':DB.bill.count()})

    return render('admin/overview.html',locals(),context_instance=RequestContext(request))
    

