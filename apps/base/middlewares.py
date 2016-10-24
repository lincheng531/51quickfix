#!/usr/bin/env python
#encoding:utf-8
import time
import base64
import random
from django.http import HttpResponse, HttpResponseRedirect
from settings import DEBUG,HOST_NAME, DB
import socket

"""
Coustom middlewares
"""


class BaseMiddleware(object):
    """ 权限控制
    """

    def process_request(self, request):

        if request.path.startswith('/store/'):
            if not request.user.is_authenticated():
                return HttpResponseRedirect('/admin/login')

        if request.path.startswith('/sec/') and not request.path.startswith('/sec/login'):
            if not request.session.get('team_id'):
                return HttpResponseRedirect('/sec/login')


    def process_view(self, request, view, args, kwargs):
        if view.__module__.startswith('apps.store'):
            func_name = '{}.{}'.format(view.__module__, view.__name__).replace('.', '_')
            if func_name in request.user.roles.keys() and not getattr(request.user.roles, func_name):
                return HttpResponseRedirect('/admin/login')

        

        





