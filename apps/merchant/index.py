# -*-encoding: utf-8-*-
from apps.base.common import admin_login_required as login_required
from apps.base.models import User
from apps.base.utils import login
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from settings import *

@login_required(2)
def index(request):
    current = 'overview'
    uname = request.GET.get('uname')
    if uname:
        user = User.objects.get(username=uname)
        login(request, user)

    res = []

    # total account
    res.append({'name': u'总注册账号数', 'value': DB.user.count()})
    res.append({'name': u'总叫修数', 'value': DB.maintenance.count()})
    res.append({'name': u'总维修单数', 'value': DB.bill.count()})

    return render('merchant/index.html', locals(), context_instance=RequestContext(request))
