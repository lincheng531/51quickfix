#encoding:utf-8
from datetime import datetime as dt
from hashlib import md5
try:
    import json
except Exception as e:
    import simplejson as json
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import HttpResponsePermanentRedirect as Http301
from django.shortcuts import render_to_response as render
from django.template import RequestContext
from django.core.cache import cache  
from settings import USER_CATEGORY
from apps.base.common import admin_login_required as login_required
from apps.base.common import get_user, json_response
from apps.base.models import User, Store, Role, UserRole
from apps.base.forms import  StoreRoleEdit
from django.contrib import messages
from bson.objectid import ObjectId 
from apps.base.logger import getlogger
from django.core.paginator import Paginator,InvalidPage,EmptyPage

logger = getlogger(__name__)


@login_required(2) 
def list(request):
    current = 'role'
    user = get_user(request)
    nodes = []
    form = StoreRoleEdit()
    for index, category in enumerate(['5','3','4']):
        category_name = USER_CATEGORY.get(category)
        nodes.append({'id':int(category), 'pId':0, 'name':category_name, 'open':'true' if index==0 else 'false'})
        users = User.objects.filter(head_type=user.head_type,category=category)
        for u in users:
            step = int("{}00000".format(category))
            step += 1
            nodes.append({'id':step, 'pId':int(category),'v':str(u.id), 'name':'{}({})'.format(u.name, u.username)})
    
    nodes = json.dumps(nodes)
    return render('store/{}_list.html'.format(current),locals(),context_instance=RequestContext(request))

@login_required(2)
def detail(request):
    current = 'role'
    user = get_user(request)
    user_names = request.POST.get('q')
    res = []
    if user_names:
        user_names = user_names.split('|')
        curr_user = User.objects.filter(username=user_names[0]).first()
        if curr_user:
            roles = UserRole.objects.filter(user=curr_user)
            for role in roles:
                res.append(str(role.role.id))
    return json_response(res)


@login_required(2)
def edit(request):
    current = 'role'
    user = get_user(request)
    user_names, roles = [request.POST.get(i) for i in ['q', 'r']]
    if user_names and roles:
        roles = [ObjectId(i) for i in roles.split('|')]
        user_names = user_names.split('|')
        roles = Role.objects.filter(id__in=roles)
        users = User.objects.filter(username__in=user_names)
        UserRole.objects.filter(user__in=users).delete()
        for u in users:
            for r in roles:
                print r.name, r.code
                UserRole(role=r, user=u).save()
    return json_response({'status':1})









