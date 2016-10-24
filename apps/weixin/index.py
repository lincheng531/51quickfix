#encoding:utf-8

from hashlib import md5, sha1
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
from apps.base.common import sec_login_required as login_required
from apps.base.forms import StuffLoginForm as LoginForm
from django.contrib.auth import authenticate
from django.contrib import messages
from apps.base.logger import getlogger
from settings import *
from apps.base.common import json_response
from django.http import HttpResponse
import traceback

logger = getlogger(__name__)


def get_profile(request):
    code = request.GET.get('code')
    logger.info("code:{}".format(code))
    if code:
        s = urlopen("https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx281067754af07cd6&secret=38b92f0765eb226eb4da69c5646aa668&code={}&grant_type=authorization_code".format(code)).read()
        try:
            s = loads(s)
            logger.info(str(s))
            if s and len(s) > 0:
                access_token, openid = s.get('access_token'), s.get('openid')
                if access_token and openid:
                    try:
                        b = urlopen("https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}".format(access_token, openid)).read()
                        return str(b)
                    except Exception as e:
                        logger.error(str(e))
        except Exception as e:
            logger.info(str(e))
          
              
         
def index(request):
    if request.method == 'GET':
        token = 'abc123'
        signature, timestamp, nonce = [request.GET.get(i) for i in ['signature', 'timestamp', 'nonce']]
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        if sha1(s).hexdigest() == signature:
            return HttpResponse(request.GET.get('echostr'))    
            
                        
def entry(request):
    if request.method == 'GET':
        return render('weixin/entry.html',locals(),context_instance=RequestContext(request))
    resp = {}
    name, mobile, address, code, industry, brand, area = [request.POST.get(i) for i in ['name', 'mobile', 'address', 'code',  'industry', 'brand', 'area']]
    #verify = REDIS.get(mobile)
    #if not verify:
    #    return json_response({'status':0, 'msg':u'验证码超时'})
    #if not verify == code:
    #    return json_response({'status':0, 'msg':u'验证码不正确'})
    if name and mobile:
        if DB.user.find({'mobile':mobile}).count() > 0:
            resp = {'status':0, 'msg':u'手机号码不得重复'}
        else:
            try:
                DB.user.save({
                            'username':mobile,
                            'mobile':mobile,
                            'name':name,
                            'gender':u'男',
                            'weixin':'weixin',
                            'address':address,
                            'category':u'客户',
                            'industry':industry,
                            'brand':brand,
                            'area':area,
                            'action':u'有意',
                            'public':1
                })
                resp = {'status':1, 'msg':u'加入成功'}
            except Exception as e:
                logger.info(traceback.print_exc())
                resp = {'status':0, 'msg':u'加入失败'}

    else:
        resp = {'status':0, 'msg':u'不得有空字段'}
    
    return json_response(resp)
            
  
def shop(request, category):
    count = 10
    page = int(request.GET.get('page', 0))
    category1 = int(category)
    if page:
        sales = DB.sale.find({'category':str(category1)}).sort('_id', -1).skip((page-1)*count).limit(count*page)
        result = []
        for sale in sales:
            result.append({
                'no':sale.get('no'),
                'm2':sale.get('m2'),
                'price':sale.get('price'),
                'content':sale.get('content'),
                'cover_image':sale.get('cover_image')
            })
        return json_response({'result':result})
    else:
        sales = DB.sale.find({'category':str(category1)}).sort('_id', -1).skip(0).limit(10)
        count = sales.count()
        return render('weixin/shop.html',locals(),context_instance=RequestContext(request))
    
    
def about(request):
    return render('weixin/about.html',locals(),context_instance=RequestContext(request))
    
def brand(request):
    return render('weixin/brand.html',locals(),context_instance=RequestContext(request))
    
def link(request):
    return render('weixin/link.html',locals(),context_instance=RequestContext(request))
    
def project(request):
    return render('weixin/project.html',locals(),context_instance=RequestContext(request))


