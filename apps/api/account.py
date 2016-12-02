#encoding:utf-8


import os
import time
import traceback
import random
import json
import StringIO
from datetime import datetime as dt
from bson.objectid import ObjectId
from settings import DB, REDIS, ENV
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate
from apps.base.common import json_response, get_json_data, get_user, login_required, gen_token, get_pinyin_initials
from apps.base.models import User, Store, Feedback
from apps.base.messages import *
from apps.base.logger import getlogger
from apps.base.utils import login 
from settings import DEBUG, HOST_NAME, ENV
from apps.base.sms import send_sms
from apps.base.validate import create_validate_code
from apps.base.uploader import base_upload as _upload

#if ENV == 'PRO':
#    from tasks.ansync import send_sms

from PIL import Image

logger = getlogger(__name__)

def download(request):
    '''
    更新版本
    :uri: /api/v1/account/download
    :POST:
        category 1为商户版 2为维修工版本

    :return:
        * versionCode
        * versionName
        * desc 
        * downloadUrl
    '''
    category = int(request.POST.get('category', 1))
    if ENV == 'PRO':
        href1 = 'http://www.51quickfix.com/static/app/release_business_7_v1.2.3.apk'
        href2 = 'http://www.51quickfix.com/static/app/release_quickfix_7_v1.2.3.apk'
    elif ENV == 'TEST2':
        href1 = 'http://bk.gaofriend.com/static/app/bk_51quickfix_business_v1.2.1.apk'
        href2 = 'http://bk.gaofriend.com/static/app/bk_51quickfix_quickfix_v1.2.1.apk'
    else:
        href1 = 'http://51quickfix.gaofriend.com/static/app/release_business_7_v1.2.3.apk'
        href2 = 'http://51quickfix.gaofriend.com/static/app/release_quickfix_7_v1.2.3.apk'
    if category == 1:
        resp = {'status':1, 'info':{'versionCode':7,'versionName':'51快修商户版V1.2.3','desc':u'', 'downloadUrl':href1}}
    else: 
        resp = {'status':1, 'info':{'versionCode':7,'versionName':'51快修V1.2.3','desc':u'', 'downloadUrl':href2}}
    return json_response(resp)

@login_required
def feedback(request):
    """
    # 反馈

    :uri: /api/v1/account/feedback

    :POST params:
        * content 反馈内容

    """
    user = get_user(request)
    data =  get_json_data(request) or request.GET
    content = data.get('content')
    resp = {'status':0}
    if not content:
        resp['alert'] = u'反馈内容不得为空'
        return json_response(resp)
    resp['status'] = 1
    Feedback(**{'user':user, 'content':content}).save()
    return json_response(resp)


@login_required
def loc(request):
    """
    # 更新or获取用户坐标:get为获取,post为更新

    :uri: /api/v1/account/loc

    :GET params:
        * uid 需要获取的用坐标的id
    :GET return:
        * loc 坐标

    :POST params:
        * loc x,y 经纬度坐标

    :return:
        * loc

    """
    resp = {'status':0, 'info':{}}
    if request.method == 'GET':
        logger.info("loc get")
        uid  = request.GET.get('uid')
        user = DB.user.find_one({'_id':ObjectId(uid)})
        resp['status'], resp['info']['loc'] = 1, user.get('loc',[])
        logger.info("get loc:{}".format(resp))
    else:
        data = get_json_data(request) or request.POST.dict()
        user = get_user(request)
        loc  = data.get('loc')
        if loc:
            user.loc = [float(i) for i in loc.split(',')]
            user.save()
            resp['status'] = 1
        logger.info("post loc:{}".format(loc))
    
    return json_response(resp)


@login_required
def remove(request):
    uname = request.GET.get('username')
    User.objects.filter(username=uname).delete()
    REDIS.hdel('verify', uname)
    logger.info('u:{}'.format(uname))
    return HttpResponse('ok')


@login_required
def rember(request): 
    """
    # 登录成功后记录iphone的device token等信息

    :uri: /api/v1/account/rember

    :POST params:
        * device_token
        * platform
        * version
        * model 机型 
        * edition 系统版本

    """
    
    data =  get_json_data(request) or request.GET
    resp = {'status':0, 'info':''}
    token, platform, loc, app_version, model, edition = [data.get(i, '') for i in  ['device_token', 'platform', 'loc',  'version', 'model', 'edition']]

    user = get_user(request)
    user = User.objects.get(username=user.mobile)

    if not token or not platform:
        resp['info'] = u'invalid device token'
        return json_response(resp)

    # 保存device token 推送通知时备用
    user.device_token = token
    user.platform     = platform
    user.app_version  = app_version
    user.app_model    = model 
    user.app_edition  = edition
    if loc:
        user.loc      = [float(i) for i in loc.split(',')]
    user.save()
    resp['status'] = 1
    return json_response(resp)


@login_required
def upload_img(request):
    """

    :uri: /api/v1/account/upload_img

    :POST params:
        * file 图片文件
        * type 文件类型，取值为：avatar,cover,status 3选1

    :return:
        * succeed {
            'status':1,
            'info':{'avatar_img':'avatar/foo/bar/xx.jpg'}} or {'status':1,'info':{'cover_img':'cover/foo/bar/xx.jpg'}} 图片的路径为相对路径，显示时需要在前面加上域名信息比如：http://www.domain.com/avatar/foo/bar/xxx.jpg 即为完整地url
            'grade':积分

    """

    #if ENV == 'PRO':
    #    assert HOST_NAME == 's1'

    data =  get_json_data(request) or request.GET

    resp = {'status':0, 'info':''}
    type    = data.get('type', 'test')

    try:
        assert type in ['avatar', 'cover', 'status']
    except:
        resp['status'] = 3
        resp['alert'] = u'参数type错误'
        return json_response(resp)

    error, url_path  = _upload(request)
    resp['status'] = 1 if error == 0 else 0

    k = '{}_img'.format(type)
    user_data = {k:url_path}
    resp['info'] = user_data
    
    # save in db
    DB.user.update({'_id':request.user.id}, {'$set':user_data})
    
    return json_response(resp)


@login_required
def update_profile(request):
    """  更新用户信息，用户修改用户信息（不得用户审核信息更新）

    :uri: /api/v1/account/update_profile

    :POST params: 
        * 需要修改什么字段就提交该字段的名称
    
    :return :
        * status:int
        * alert:string
        * info:{profile:profile}
    """
    if request.method == 'GET':
        raise Http404
    
    resp = {'status':0, 'info':{}, 'alert':''}
    user = get_user(request)
    data =  get_json_data(request) or request.POST.dict()
    for k, v in data.iteritems():
        if k == 'card' and v:
            v = v.split(',')
        if hasattr(user, k):
            setattr(user, k, v)
    user.is_update = True
    user.save()
    resp['status'], resp['alert'] = 1, u'修改成功'
    resp['info']   = user.get_user_profile_dict()
    resp['status'] = 1
    return json_response(resp)



def signin(request):
    """  用户登录，根据用户的分类来获取商户和维修员的数据

    :uri: /api/v1/account/signin

    :POST params:
        * username 必填,用户名(手机号)
        * password 必填,帐号密码

    :return:
        * status
        * info:
                如果category为1 商户
                    username    
                    name       
                    address         地址
                    mobile          手机号码
                    company         公司名称
                    store           门店名称
                    store_id        门店id
                    category        1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员
                    avatar_img      头像
                    company_logo    公司logo
                    device_count    餐厅资产数
                    task_count      任务数
                    repair_count    维修数
                    is_active       1为审核成功 0为待审核  -1未审核失败
                    
                如果category为0 维修工
                    * username    登陆账号
                    * name        昵称
                    * city        城市 
                    * area        大区域
                    * address     地址
                    * district    比如浦东区，请充地图获取
                    * mobile      手机号码
                    * category    1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员
                    * avatar_img  头像 
                    
                    * card        身份证多个列表 [正面,反面] string用,隔开
                    * card_type   1:审核通过 0:暂停 -1:拒绝
                    * card_no     身份证号码
                    * screen_name 身份证名称
                    * card_msg    身份证审核不通过原因

                    * electrician        电工证
                    * electrician_type   1:电工证审核通过 0:暂停 -1:拒绝
                    * electrician_day1   起始时间 
                    * electrician_day2   结束时间
                    * electrician_msg    不通过原因

                    * gas        煤气证照片
                    * gas_type   1:电工证审核通过 0:暂停 -1:拒绝
                    * gas_day1   起始时间 
                    * gas_day2   结束时间
                    * gas_msg    不通过原因

                    * refrigeration        制冷正号码
                    * refrigeration_type   1:审核通过 0:暂停 -1:拒绝
                    * refrigeration_day1   起始时间 
                    * refrigeration_day2   结束时间
                    * refrigeration_msg    不通过原因

                    * trains培训证 {'img':图片, 'name':名称, 'type':1:审核通过 0:暂停 -1拒绝, 'day1':起始时间, 'day2':结束时间, 'msg':不通过原因}
                    * is_active 1为审核成功 0为待审核  -1未审核失败
                
        * alert 如果某个字段值为空，则不返回该字段

    """

    if request.method == 'GET':
        raise Http404

    data =  get_json_data(request) or request.POST.dict()
    resp = {'status':0, 'info':{}, 'alert':''}

    username = str(data.get('username', '')).strip().lower()
    password = str(data.get('password', ''))
   

    mobile_user = User.objects.filter(username=username).first()
    email_user = User.objects.filter(email=username).first()

    logger.debug('mobile user:{}'.format(mobile_user))
    logger.debug('email user:{}'.format(email_user))
    logger.debug('username:{}'.format(username))

    if not mobile_user and not email_user:
        resp['status'], resp['alert'] = USER_DOES_NOT_EXISTS
        return json_response(resp)
    
    _user = mobile_user or email_user
    user =  authenticate(username=_user.username, password=password)
    if user:
        if user.is_active:
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            login(request, user)
            user.save()
            user = User.objects.get(username=username)
            resp['status'] = 1
            resp['info'] = user.get_user_profile_dict()
        else:
            resp['status'], resp['alert'] = 0, u'当前的账户禁止登陆，请稍等或者联系我们'
        logger.info(resp)
        return json_response(resp)
    
    resp['status'], resp['alert'] =  PWD_ERROR
    logger.info(resp)
    return json_response(resp)

def send_code(request, code):
    """  发送验证码(忘记密码的)

    :uri: /api/v1/account/send_code/<code:图片验证码>

    :POST params:
        * username 必填,用户名(手机号)

    """
    resp        = {'status':0, 'info':{}, 'alert':''}
    try:
        data        =  get_json_data(request) or request.POST
        username    = str(data['username'])
        user        = User.objects.filter(username=username).first()
        if user == None:
            resp['status'], resp['alert'] = USER_DOES_NOT_EXISTS
        else:
            if REDIS.get('validate_{}'.format(username)) <> code:
                resp['status'], resp['alert'] = 0, u'请输入正确的图片验证码'
                return json_response(resp)
            code = gen_token()
            REDIS.set("send_{}".format(username), code)
            REDIS.expire("send_{}".format(username), 600)
            resp['status'], resp['alert'] = 1, u'发送成功'
            if ENV <> 'PRO':
                resp['code'] = code
            else:
                send_sms(username, u'【51快修】您当前的验证码是:{}'.format(code))
    except Exception as e:
        resp['status'], resp['alert'] = 0, u'发送失败'
    finally:
        return json_response(resp)
        

def forget(request):
    """  忘记密码

    :uri: /api/v1/account/forget

    :POST params:
        * username 必填,用户名(手机号)
        * password 必填,用户名密码
        * code 验证码 必填

    """
    resp        = {'status':0, 'info':{}, 'alert':u'重置失败'}
    data        =  get_json_data(request) or request.POST
    username    = str(data['username'])
    password    = str(data['password'])
    code        = str(data['code'])
    
    user        = User.objects.filter(username=username).first()
    if user == None:
        resp['status'], resp['alert'] = 0, u'该用户不存在'
        return json_response(resp)
    else:   
        verify_code = REDIS.get("send_{}".format(username))
        logger.info('debug1:{}:{}:{}'.format(username, verify_code, code))
        if verify_code and verify_code == code:
            resp['status'] = 1
            user.set_password(data.get('password'))
            user.save()
    return json_response(resp)


@login_required
def reset_pwd(request):
    """  重设密码

    :uri: /api/v1/account/reset_pwd

    :POST params:
        * old_password 当前密码，必填
        * password 必填,用户名密码

    """

    resp        = {'status':0, 'info':{}, 'alert':''}
    data        =  get_json_data(request) or request.POST
    password, old_password    = [data.get(i) for i in ['password', 'old_password']]
    user = get_user(request)
    if user and password and old_password:
        if user.check_password(old_password):
            resp['status'], resp['alert'] = 1, u'重设密码成功'
            user.set_password(data.get('password'))
            user.save()
        else:
            resp['alert'] = u'当前密码不对'
    return json_response(resp)


def signout(request):
    """ 退出登录帐号

    :uri: /api/v1/account/signout

    :GET params: 空

    """

    resp = {'status':1, 'info':{}, 'alert':''}
    keys = ['user_id', 'username', 'screen_name']
    for key in keys:
        if key in request.session.keys():del request.session[key]
        assert(key not in request.session.keys())
    return  json_response(resp)

@login_required
def profile(request, uid):
    """ 根据用户ID获取用户信息,该接口必须是自己查询自己的资料，不得查询他人的

    :uri: /api/v1/account/profile/<uid>

    """
    resp  = {'status':0, 'info':{}}
    user  = get_user(request)
    resp['status']  = 1
    resp['info']    = user.get_user_profile_dict()
    return json_response(resp)


@login_required
def verify_profile(request):
    """  更新审核资料多个界面一起上传，该接口必须登录，重新上传数据

    :uri: /api/v1/account/verify_profile
    :POST parmar:
        * category 商户：1
                        * name 用户名
                        * store 门店名称
                        * address 地址 
                        * loc x,y坐标 请从地图获取
                        * city 城市，请从地图获取
                        * district 比如浦东区，请充地图获取
                        * tel 固定电话
                        * area 区 华东,华北,华南有则提交无则不填写
                        * avatar_img 头像 请用uploader接口上传
                        * logo 餐厅头像 请用uploader接口上传
                        * card 证件如:“营业执照,税务登记证” 请用uploader接口上传
                   维修员：0
                        * card 身份证照片 多个请用,分割
                        * electrician 电工证照片
                        * gas 煤气证照片
                        * refrigeration 制冷证照片
                        * train 培训证 多个请用,分割
                        * loc x,y 
                        * city 城市，请从地图获取
                        * district 比如浦东区，请充地图获取
        * 商户的时候注册没用”电话“，在更新的时候多个电话请用“,”号隔开
        * 更新数据请参考mregister， sregister, 都无需提交手机，密码，验证码

    """
    user = get_user(request)
    resp    = {'status':0, 'info':{}}
    data =  get_json_data(request) or request.POST
    if user.category == '1':
        if not data.get('name'):
            resp['alert'] = u'名称不得为空'
        elif not data.get('store'):
            resp['alert'] = u'门店名称不得为空'
        elif not data.get('avatar_img'):
            resp['alert'] = u'头像不得为空'
        elif not data.get('card'):
            resp['alert'] = u'营业执照,税务登记证不得为空'
        else:
            if len(data.get('card',[])) <> 2:
                resp['alert'] = u'营业执照,税务登记证不得为空'
                return json_response(resp)
            licence, certificate = data.get('card', [])
            store = Store.objects.get(id=ObjectId(user.store_id))
            setattr(store, 'name', data.get('store'))
            setattr(store, 'licence', licence)
            setattr(store, 'certificate', certificate)
            setattr(store, 'logo', [data.get('logo','')])
            for key, v in data.iteritems():
                if key == 'tel' and v:
                    v = v.split(',')
                if key == 'loc' and v:
                    v = v.split(',')
                if key not in ['store', 'card', 'logo']:
                    setattr(user, key, v)
            resp['status'], resp['alert'] = 1, u'修改成功'
    elif user.category in ('0', '2'):
        if not data.get('card'):
            resp['alert'] = u'身份证图片不得为空'
        else:
            if len(data.get('card').split(',')) <> 2:
                resp['alert'] = u'身份证必须正反两面'
                return json_response(resp)
            __p = lambda t:True if t else False
            if True in [__p(data.get('electrician')) , __p(data.get('gas')), __p(data.get('refrigeration'))]:
                for key, v in data.iteritems():
                    if key == 'loc' and v:
                        v = [float(i) for i in v.split(',')]
                    if key == 'train':
                        v = v.split(',')
                    if key == 'card' and v:
                        v = v.split(',')
                    setattr(user, key, v)
                resp['status'], resp['alert'] = 1, u'修改成功'
            else:
                resp['alert'] = u'电工证，制冷证，煤气证必选其一'
                return json_response(resp)
    setattr(user, 'is_update', True)
    user.save()
    resp['status'] = 1
    resp['info'] = user.get_user_profile_dict()
    return json_response(resp)



def send_mobile(request, mobile, code):
    """  获取验证手机唯一性，将验证码传入进来一起核对

    :uri: /api/v1/account/send_mobile/<mobile:手机号码>/<code:图片验证码>
    :return:
        * status -1 为已经注册

    """

    resp    = {'status':0, 'info':{}}
    if len(mobile) <> 11 or not mobile.isdigit():
        resp['alert'] = u'请填写正确的手机号码'
        return json_response(resp)
    validate = REDIS.get('validate_{}'.format(mobile))
    REDIS.delete('validate_{}'.format(mobile))
    if not code or not validate or code <> validate:
        resp['alert'] = u'请填写正确的图片验证码'
        return json_response(resp)
    user = DB.user.find_one({'mobile':mobile})
    if user:
        resp['alert'] = u'该手机号码已存在'
        resp['status'] = -1
        return json_response(resp)

    code = gen_token()
    REDIS.set("rvg_{}".format(mobile), code)
    REDIS.expire("rvg_{}".format(mobile), 1800)
    logger.info("mobile:{},code:{}".format(mobile, code))
    if ENV <> 'PRO':
        resp['code'] = code
    else:
        send_sms(mobile, u'【51快修】您的验证码是:{},30分钟内有效'.format(code))
    resp['status'],resp['alert'] = 1,u'发送成功'
    return json_response(resp)


def verify_mobile(request, mobile, code):
    """  验证手机，请保存手机和该手机验证码，一次性提交注册

    :uri: /api/v1/account/verify_mobile/<mobile>/<code>手机验证码
    :return 
        * status -1已经注册
 
    """
    resp    = {'status':0, 'info':{}, 'alert':u'手机短信码错误'}
    user = DB.user.find_one({'mobile':mobile})
    if user:
        resp['status'] = -1
        resp['alert']  = u'该手机号码已存在，不得注册'
        return json_response(resp)
    verify_code = REDIS.get("rvg_{}".format(mobile))
    if verify_code and verify_code == code:
        resp['status'], resp['alert'] = 1, u'验证成功'
    return json_response(resp)


def validate(request,mobile):
    """  获取图片验证码,没获取一次短信验证码之后要刷新该url并显示

    :uri: /api/v1/account/validate/<mobile:手机号码>


    """
    code_img, validate_code = create_validate_code()
    buf = StringIO.StringIO() 
    code_img.save(buf, 'JPEG',quality=70)
    REDIS.set('validate_{}'.format(mobile),validate_code)
    REDIS.expire("validate_{}".format(mobile), 1800)
    return HttpResponse(buf.getvalue(), 'image/gif')


def mregister(request):
    """  商户版注册-多次步骤一次性提交

    :uri: /api/v1/account/mregister

    :POST params: 
        * mobile 手机
        * code 短信验证码防止跳过注册第一步
        * password 密码
        * name 用户名
        * store 门店名称
        * address 地址 
        * loc x,y坐标 请从地图获取
        * city 城市，请从地图获取
        * district 比如浦东区，请充地图获取
        * tel 固定电话
        * area 区 华东,华北,华南有则提交无则不填写
        * avatar_img 头像 请用uploader接口上传
        * logo 餐厅头像 请用uploader接口上传
        * card 证件如:“营业执照,税务登记证” 请用uploader接口上传
        * 
    :return:
        info->status:1 为已经注册

    """
    resp = {'status':0, 'info':{'status':0}}
    data =  get_json_data(request) or request.POST
    mobile, code, password, name, store, avatar_img, address, area, loc, card, district, city, tel, logo = [data.get(i) for i in ['mobile', 'code', 'password', 'name', 'store', 'avatar_img', 'address', 'area', 'loc', 'card', 'district', 'city', 'tel', 'logo']]
    if not mobile:
        resp['alert'] = u'手机不得为空'
        return json_response(resp)
    if not loc:
        resp['alert'] = u'请查看是否允许定位功能'
        return json_response(resp)
    if not code:
        resp['alert'] = u'验证码不得为空'
        return json_response(resp)
    if not password:
        resp['alert'] = u'密码不得为空'
        return json_response(resp)
    if not name:
        resp['alert'] = u'名称不得为空'
        return json_response(resp)
    if not store:
        resp['alert'] = u'门店名称不得为空'
        return json_response(resp)
    if not address:
        resp['alert'] = u'地址不得为空'
        return json_response(resp)
    if not city:
        resp['alert'] = u'城市不得为空'
        return json_response(resp)
    if not district:
        resp['alert'] = u'区域不得为空'
        return json_response(resp)
    if not card:
        resp['alert'] = u'营业执照,税务登记证不得为空'
        return json_response(resp)
    else:
        if len(card.split(',')) <> 2:
            resp['alert'] = u'营业执照,税务登记证缺一不可'
            return json_response(resp)

    verify_code = REDIS.get("rvg_{}".format(mobile))
    if verify_code and verify_code == code:
        if DB.user.find_one({'username':mobile}):
            resp['alert'], resp['info']['status'] = u'该手机号码已存在，不得注册', 1
            return json_response(resp)
        cards = card.split(',')
        store_no = Store.objects.filter(head_type=1).count() + 1
        store_data = {
                        'head_type':1, 'name':store, 'rid':str(ObjectId()), 'area':area, 
                        'city':city, 'district':district, 'address':address, 'no':str(store_no),
                        'tel':tel, 'loc':[float(i) for i in loc.split(',')], 
                        'mobile':mobile, 'phone':mobile, 'logo':[logo], 'is_active':1,
                        'initial':get_pinyin_initials(store), 'licence':cards[0], 'licence_type':1, 
                        'certificate':cards[1], 'certificate_type':1,'store_manager':name
                    }
        store = Store()
        for k, v in store_data.iteritems():
            if v:
                setattr(store, k, v)
        store.save()
        user_data = {
                    'is_active':1,
                    'head_type':1, 
                    'username':mobile, 
                    'name':name,
                    'mobile':mobile, 
                    'address':address, 
                    'store':store.name, 
                    'store_id':str(store.id), 
                    'category':'1', 
                    'avatar_img':avatar_img, 
                    'loc':[float(i) for i in loc.split(',')], 
                    'tel':[tel],
                    'area':area,
                    'company_logo':logo,
                    'city':city
        }
        new_user  = User()
        for k, v in user_data.iteritems():
            if v:
                setattr(new_user, k, v)
        new_user.set_password(password)
        new_user.save()
        resp['status'], resp['alert'] = 1, u'注册成功！'
    else:
        resp['alert'] = u'验证码不对'
    return json_response(resp)


def sregister(request):
    """  维修员版注册-多次步骤一次性提交

    :uri: /api/v1/account/sregister

    :POST params:
        * avatar_img 头像 请用uploader接口上传
        * name 名称 
        * address 家庭住址
        * password 密码
        * mobile 手机
        * code 验证码
        * card 身份证照片 多个请用,分割
        * electrician 电工证照片
        * gas 煤气证照片
        * refrigeration 制冷证照片
        * train 培训证 多个请用,分割
        * loc x,y 
        * city 城市，请从地图获取
        * district 比如浦东区，请充地图获取
    """
    
    resp    = {'status':0, 'info':{}}
    data =  get_json_data(request) or request.POST
    mobile, code, password, name, avatar_img, address, card, electrician, gas ,\
    refrigeration, train, loc, city, district  = [data.get(i) for i in ['mobile', 'code', 'password', 'name', 'avatar_img', 'address', 'card', 'electrician',  'gas', 'refrigeration', 'train', 'loc', 'city', 'district']]
    if not mobile:
        resp['alert'] = u'电话不得为空'
    elif not code:
        resp['alert'] = u'验证码不得为空'
    elif not password:
        resp['alert'] = u'密码不得为空'
    elif not avatar_img:
        resp['alert'] = u'头像不得为空'
    elif not name:
        resp['alert'] = u'名称不得为空'
    elif not address:
        resp['alert'] = u'地址不得为空'
    elif not card:
        resp['alert'] = u'身份证图片不得为空'
    elif mobile and code and password and avatar_img and name and address:
        verify_code = REDIS.get("rvg_{}".format(mobile))
        if verify_code and verify_code == code:
            if DB.user.find_one({'username':mobile}):
                resp['alert'] = u'该手机号码已存在，不得注册'
                return json_response(resp)
            __p = lambda t:True if t else False
            if True in [__p(electrician) , __p(gas), __p(refrigeration)]:
                resp['status'], resp['alert'] = 1, u'注册成功，请等待审核，审核结果会以短信通知的形式发送到您的注册手机！！'
                item = {
                    'category':'0',
                    'is_active':0,
                    'head_type':1,
                    'name':name,
                    'username':mobile,
                    'mobile':mobile,
                    'avatar_img':avatar_img,
                    'address':address,
                    'card':card.split(','),
                    'electrician':electrician,
                    'gas':gas,
                    'refrigeration':refrigeration,
                    'train':train.split(',') if train else [],
                    'city':city,
                    'district':district
                }
                if ENV == 'PRO':
                    item['is_active'] = 0
                new_user = User()
                for k, v in item.iteritems():
                    setattr(new_user, k, v)
                new_user.set_password(password)
                new_user.save()
            else:
                resp['alert'] = u'电工证，制冷证，煤气证必选其一'
        else:
            resp['alert'] = u'验证码不得为空'

    return json_response(resp)

            






    


    
