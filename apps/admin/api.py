# -*- encoding:utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from apps.base.common import json_response, get_user, get_json_data
from apps.base.utils import login as _login
from django.contrib.auth import logout as _logout
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from apps.base.models import User
from apps.base.forms import StuffLoginForm as LoginForm
from apps.base.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from apps.base.logger import getlogger
from bson.son import SON
import pymongo

logger = getlogger(__name__)


def logout(request):
    _logout(request)
    return HttpResponseRedirect('/admin/')


def login(request):
    resp = {'status': 1, 'info': ''}

    form = LoginForm(request.POST)
    if not form.is_valid():
        resp['status'] = 0
        resp['alert'] = u'用户名或密码不符合要求'
        return json_response(resp)

    form_data = form.cleaned_data

    user = authenticate(**form_data)
    if not user:
        resp['status'] = 0
        resp['alert'] = u'用户名或密码错误'
        return json_response(resp)

    if not user.is_superuser:
        resp['status'] = 0
        resp['alert'] = u'你不是管理员，禁止登录'
        return json_response(resp)

    if not user.is_active:
        resp['status'] = 0
        resp['alert'] = u'你已经被禁止登录'
        return json_response(resp)

    user.backend = 'mongoengine.django.auth.MongoEngineBackend'
    result = _login(request, user)
    resp['info'] = user.get_user_profile_dict()
    response = json_response(resp)
    return response


# @login_required(2)
def maintenanceList(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    p = int(data.get('page') or request.GET.get('page') or 1)
    # res = Maintenance.objects((Q(be_reset_fixed__ne=1) | Q(is_collect=1)) & Q(collected__ne=1) & Q(user=user)).order_by(
    #         '-create_time').skip((p - 1) * 20).limit(20)
    # result = []
    # for r in res:
    #     if r.head_type == 1:
    #         detail = r.get_result1()
    #     else:
    #         detail = r.get_result(0)
    #     detail['push_count'] = PushHistory.objects.filter(maintenance=str(r['id'])).count()
    #     result.append(detail)
    # resp['info']['results'] = result
    # return json_response(resp)

    query = {}
    status = request.GET.get('status')
    search_q = request.GET.get('q')

    q = Maintenance.objects(**query)

    if status:
        q = Maintenance.objects(Q(status__in=status.split(',')) & (Q(settlement__lt=0) | Q(settlement__exists=False)))

    if status == 'serviceAudit1':  # 服务商待提交
        q = Maintenance.objects(
            Q(status=2) & (Q(audit_repair_result_save=True) & Q(settlement__lt=1)))

    if status == 'serviceAudit2':  # 服务商待商户审核
        q = Maintenance.objects(
            Q(status=2) & Q(settlement=1) & Q(audit_merchant_result__exists=False))

    if status == 'serviceAudit3':  # 商户审核未通过
        q = Maintenance.objects(
            Q(status=2) & (Q(audit_merchant_result=False)))

    if status == 'serviceAudit4':  # 服务商审核未通过
        q = Maintenance.objects(
            Q(status=2) & (Q(audit_repair_result_save=False) & Q(settlement__lt=1)))

    if status == 'merchantAudit1':  # 商户待审核
        q = Maintenance.objects(
            Q(status=2) & Q(settlement=1) & Q(audit_merchant_result__exists=False) & (
                Q(audit_merchant_result_save=True) | Q(audit_merchant_result_save__exists=False)))

    if status == 'merchantAudit2':  # 商户审核未通过
        q = Maintenance.objects(
            Q(status=2) & (Q(audit_merchant_result=False)))

    if status == 'merchantAudit3':  # 商户审核失败
        q = Maintenance.objects(
            Q(status=2) & (Q(audit_merchant_result_save=False) & Q(settlement=1)))

    # if status == 'auditing':
    #     q = Maintenance.objects(
    #         Q(status=2) & (Q(settlement__exists=False) | Q(settlement__lt=2)))
    # if status == 'audited':
    #     q = Maintenance.objects(Q(status=2) & (Q(audit_merchant_result=False) | Q(audit_repair_result=False)))
    if status == 'merchantSettling':
        q = Maintenance.objects(
            Q(status=2) & Q(settlement=2) & Q(audit_merchant_result=True) & Q(audit_repair_result=True) & Q(
                settle_merchant_result__exists=False))

    if status == 'merchantForSettling':
        q = Maintenance.objects(
            Q(status=2) & Q(settlement=2) & Q(audit_merchant_result=True) & Q(audit_repair_result=True) & Q(
                settle_merchant_result=True) & Q(settle_repair_result__exists=False))

    if status == 'repairSettling':
        q = Maintenance.objects(
            Q(status=2) & Q(settlement=2) & Q(audit_merchant_result=True) & Q(audit_repair_result=True) & Q(
                settle_repair_result__exists=False))

    if status == 'repairForSettling':
        q = Maintenance.objects(
            Q(status=2) & Q(settlement=2) & Q(audit_merchant_result=True) & Q(audit_repair_result=True) & Q(
                settle_repair_result=True) & Q(settle_merchant_result__exists=False))

    if status == 'settled':
        q = Maintenance.objects(status=2, settle_merchant_result=True, settle_repair_result=True)

    if search_q:
        q = Maintenance.objects(Q(code=search_q) | Q(store_name=search_q))

    filter_dict = {}
    for item in ('city', 'category', 'state', 'head_type'):
        if request.GET.get(item):
            filter_dict[item] = request.GET.get(item)

    brand_id = request.GET.get('brand')
    if brand_id:
        brand = Brand.objects(id=ObjectId(brand_id)).first()
        if brand:
            filter_dict['brand'] = brand.name

    starttime = request.GET.get('starttime')
    endtime = request.GET.get('endtime')
    if starttime:
        filter_dict['create_time__gte'] = starttime
    if endtime:
        filter_dict['create_time__lte'] = endtime

    q = q.filter(**filter_dict)

    mc = q.order_by('-create_time').skip((p - 1) * 20).limit(20)
    total = q.count()
    totalPage = total / 20 + int(bool((total % 20)))
    result = [item.get_result() for item in mc]
    resp['info']['meta'] = {'totalPage': totalPage, 'currentPage': p, 'totalCount': total}
    resp['info']['results'] = result
    return json_response(resp)


def _process_result(_r):
    _r['id'] = _r['_id']
    _r['user'] = DB.user.find_one({'_id': _r['user']})
    _r['user_count'] = DB.maintenance_users.find({'maintenance': _r['_id'], 'opt_user': _r['user']['_id']}).count()
    _r['apply_count'] = DB.maintenance_users.find(
        {'maintenance': _r['_id'], 'status': 1, 'opt_user': _r['user']['_id']}).count()
    _r['confirm_count'] = DB.maintenance_users.find(
        {'maintenance': _r['_id'], 'status': 2, 'opt_user': _r['user']['_id']}).count()
    _r['head_type_'] = HEAD_BRAND.get(_r.get('head_type', ''), '')
    _r['state_'] = MaintenanceState.get(_r.get('state'), '')
    _r['status_'] = MaintenanceStatus.get(_r.get('status'), '')
    _r['device'] = DB.device.find_one({'_id': ObjectId(_r['device'])})

    mt = Maintenance.objects.get(id=ObjectId(_r['id']))
    _r['status_list'] = mt.status_list
    bill = Bill.objects.filter(maintenance=mt).first()
    if bill:
        _r['bill'] = bill.detail()
        if _r['status'] == 3: _['status'] = 5

    return _r


def update_bill(request, id):
    data = get_json_data(request) or request.POST.dict()
    bill = Bill.objects.get(id=ObjectId(id))
    for item in ['visit', 'labor', 'travel', 'stay_total', 'discount', 'total']:
        try:
            value = int(data.get(item) or 0)
        except:
            continue

        setattr(bill, item, value)

    if data.get('others'):
        try:
            others = json.loads(data['others'])
            bill.others = [{'msg': item.get('key'), 'total': int(item.get('value') or 0)} for item in others]
        except:
            import traceback
            traceback.print_exc()

    bill.save()
    return json_response(True)


def maintenanceDetail(request, id):
    id = ObjectId(id)
    item = DB.maintenance.find_one({'_id': id})
    item = _process_result(item)
    item['store'] = DB.store.find_one({'_id': ObjectId(item.get('store'))})
    grab_user = DB.user.find_one({'_id': ObjectId(item.get('grab_user'))})
    if grab_user:
        item['grab_user'] = grab_user
        item['grab_user']['title'] = USER_CATEGORY.get(grab_user['category'])
    # return render('admin/{}_detail.html'.format(current),locals(),context_instance=RequestContext(request))

    item['audit_repair_user'] = DB.user.find_one({'_id': ObjectId(item.get('audit_repair_user'))}) or {}
    item['audit_merchant_user'] = DB.user.find_one({'_id': ObjectId(item.get('audit_merchant_user'))}) or {}
    item['settle_repair_user'] = DB.user.find_one({'_id': ObjectId(item.get('settle_repair_user'))}) or {}
    item['settle_merchant_user'] = DB.user.find_one({'_id': ObjectId(item.get('settle_merchant_user'))}) or {}
    return json_response(item)


def maintenance_history(request, id):
    current = 'repair'
    user = get_user(request)
    res = Maintenance.objects.get(id=ObjectId(id), head_type=user.head_type)
    store = Store.objects.get(id=ObjectId(res['store']))
    device = Device.objects.get(id=ObjectId(res['device']))
    setattr(res, 'store', store)
    detail = res.get_result()
    bill = res.bill.detail() if res.bill else {}
    return render('store/{}_detail.html'.format(current), locals(), context_instance=RequestContext(request))


def save_audit_repair(request, id):
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(id))
    user = User.objects.get(id=ObjectId(data['user_id']))
    maintenance.audit_repair_result_save = bool(int(data['audit_repair_result']))
    maintenance.audit_repair_note_save = data.get('audit_repair_note')
    maintenance.settlement = 0
    maintenance.save()
    return maintenanceDetail(request, id)


def save_audit_merchant(request, id):
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(id))
    user = User.objects.get(id=ObjectId(data['user_id']))
    maintenance.audit_merchant_result_save = bool(int(data['audit_merchant_result']))
    maintenance.audit_merchant_note_save = data.get('audit_merchant_note')
    maintenance.save()
    return maintenanceDetail(request, id)


def save_settlement(request, id):
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(id))
    user = User.objects.get(id=ObjectId(data['user_id']))

    if user.category in ('1', '3', '4', '5', '7'):
        maintenance.settle_merchant_result_save = True
        maintenance.settle_merchant_note_save = data.get('settle_note')

    if user.category in ('0', '2', '6', '7'):
        maintenance.settle_repair_result_save = True
        maintenance.settle_repair_note_save = data.get('settle_note')

    maintenance.save()
    return maintenanceDetail(request, id)


def audit_repair(request, id):
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(id))
    user = User.objects.get(id=ObjectId(data['user_id']))
    maintenance.settlement = 1
    maintenance.audit_repair_user = user
    maintenance.audit_repair_date = datetime.datetime.now()
    maintenance.audit_repair_result = bool(int(data['audit_repair_result']))
    maintenance.audit_repair_note = data.get('audit_repair_note')
    maintenance.save()
    return maintenanceDetail(request, id)


def audit_merchant(request, id):
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(id))
    user = User.objects.get(id=ObjectId(data['user_id']))
    maintenance.settlement = 2
    maintenance.audit_merchant_user = user
    maintenance.audit_merchant_date = datetime.datetime.now()
    maintenance.audit_merchant_result = bool(int(data['audit_merchant_result']))
    maintenance.audit_merchant_note = data.get('audit_merchant_note')
    maintenance.save()
    return maintenanceDetail(request, id)


def settlement_clear(request, id):
    data = get_json_data(request) or request.POST.dict()
    maintenance = Maintenance.objects.get(id=ObjectId(id))
    user = User.objects.get(id=ObjectId(data['user_id']))

    if user.category in ('1', '3', '4', '5', '7'):
        maintenance.settle_merchant_result = True
        maintenance.settle_merchant_user = user
        maintenance.settle_merchant_date = datetime.datetime.now()
        maintenance.settle_merchant_note = data.get('settle_note')

    if user.category in ('0', '2', '6', '7'):
        maintenance.settle_repair_result = True
        maintenance.settle_repair_user = user
        maintenance.settle_repair_date = datetime.datetime.now()
        maintenance.settle_repair_note = data.get('settle_note')

    if maintenance.settle_repair_result and maintenance.settle_merchant_result:
        maintenance.settlement = 3

    maintenance.save()
    return maintenanceDetail(request, id)


def store(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    head_type, no = [data.get(i) for i in ['head_type', 'no']]
    resp['info']['results'] = DB.store.find_one({'no': no, 'head_type': int(head_type)})
    return json_response(resp)


def user(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    mobile = data.get('mobile')
    resp['info']['results'] = DB.user.find_one({'mobile': mobile})
    return json_response(resp)


def repairs(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = get_user(request)
    loc = request.GET.get('loc')
    results = [item for item in DB.user.find({'category': '0'}).sort([('city', 1)])]
    if loc:
        loc = loc.split(',')
        for item in results:
            userloc = item.get('loc') or (999999999, 999999999)
            item['max_distance'] = (userloc[0] - float(loc[0])) ** 2 + (userloc[1] - float(loc[1])) ** 2

        # users = list(User.objects(
        #     __raw__={"loc": SON([("$near", loc), ("$maxDistance", 10 * 10000000000000000 / 111.12)]),
        #              'category': '0', 'is_active': 1, 'device_token': {'$ne': None}}))

        # results = [{
        #     'city': item.city,
        #     'area': item.area,
        #     'name': item.name,
        #     'mobile': item.mobile,
        # } for item in users]
        results.sort(key=lambda x: x['max_distance'])
    resp['info']['results'] = results
    return json_response(resp)


def categoryList(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    level = request.GET.get('level', '1')
    parent = request.GET.get('parent')
    key_dict = {'1': 'category', '2': 'efcategory', '3': 'ecategory', '4': 'brand'}
    key = key_dict[level]
    filter_dict = {}
    if parent:
        parent_key = key_dict.get(str((int(level) - 1)))
        if parent_key:
            filter_dict[parent_key] = parent

    resp['info']['results'] = DB.device.find(filter_dict).distinct(key)
    return json_response(resp)


# def deviceList(request):
#     resp = {'status': 1, 'info': {}, 'alert': ''}
#     data = get_json_data(request) or request.POST.dict()
#     filter_dict = {}
#     resp['info']['results'] =  DB.device.find(filter_dict)
#     return json_response(resp)


def call(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    # now = dt.now()
    # data = get_json_data(request) or request.POST.dict()
    # loggend_user = User.objects.get(id=ObjectId(data.get('logged_user')))
    # head_type = int(data.get('type', 1))
    # store = None
    # store_no = data.get('store_no')
    # if store_no:
    #     store = Store.objects.filter(head_type, no = store_no).first()
    #
    # if not store:
    #     import pdb;pdb.set_trace()
    #     pass
    #
    #
    # mobile = data.get('mobile')
    # user = User.objects.filter(username=mobile).first()
    # if not user:
    #     import pdb;pdb.set_trace()
    #
    # selectedDevice = data.get('selectedDevice')
    # if selectedDevice:
    #     device = Device.objects.get(id=ObjectId(selectedDevice))
    # else:
    #     import pdb;pdb.set_trace()
    #     pass
    #
    #
    # if not device:
    #     resp['status'], resp['alert'] = 0, u'没有找到该设备'
    #     return json_response(resp)
    #
    # users = data.get('users')
    #
    # maintenance = Maintenance(**{}).save()
    #
    # if len(users) > 0:
    #     # 推送短信规则
    #     send_time = now.strftime('%H:%M')
    #
    #     members = [str(i.id) for i in users]
    #
    #     maintenance = {
    #         'user': loggend_user.id,
    #         'store_name': store.name,
    #         'store': str(store.id),
    #         'address': store.address,
    #         'company': user.company,
    #         'product': device.name,
    #         'product_id': product.id,
    #         'supplier': supplier.name,
    #         'supplier_id': supplier.id,
    #         'area': store.area,
    #         'city': store.city,
    #         'loc': store.loc,
    #         'status': 0,
    #         'brand': product.brand.name,
    #         'head_type': loggend_user.head_type,
    #         'device': str(device.id),
    #         'no': device.no,
    #         'store_no': store.no,
    #         'logo': logo.split(',') if logo else [],
    #         'content': error,
    #         'error_code': eid,
    #         'create_time': dt.now(),
    #         'update_time': dt.now(),
    #         'members': members
    #     }
    #
    #     maintenance['code'] = _send_count(loggend_user.head_type)
    #     maintenance['guarantee'] = device.guarantee
    #     maintenance['start_time'] = pf8(start_time)
    #     maintenance['end_time'] = pf8(end_time)
    #     # mtceid = DB.maintenance.save(maintenance)
    #     mtceid = Maintenance(**maintenance).save()
    #
    #     # 新增报价单
    #     Bill(**{
    #         'opt_user': loggend_user, 'maintenance': mtceid.id,
    #         'supplier': device.supplier, 'product': device.product,
    #         'total': 0, 'analysis': '', 'measures': '', 'status': -2,
    #         'state': 1, 'device': device
    #     }).save()
    #
    #     if MaintenanceHistory.objects(maintenances=mtceid).count():
    #         resp['status'], resp['alert'] = 0, u'订单已经存在维修历史, 请联系管理员'
    #         return json_response(resp)
    #
    #     mhid = MaintenanceHistory(**{
    #         'user': loggend_user,
    #         'maintenances': [mtceid],
    #         'members': members,
    #     }).save()
    #
    #     mc_data = {
    #         'user': loggend_user,
    #         'histories': [mhid],
    #         'store_name': store.name,
    #         'store': str(store.id),
    #         'store_no': store.no,
    #         'address': store.address,
    #         'members': members,
    #     }
    #
    #     if loggend_user.head_type > 1:
    #         mc_data['state'] = maintenance.get('state')
    #         mc_data['must_time'] = maintenance.get('must_time')
    #
    #     mcid = MaintenanceCollection(**mc_data).save()
    #
    #     title = PUSH0.format(store.name, product.name)
    #     sdata = {'type': 0, 'oid': str(mtceid.id), 'cid': str(mcid.id)}
    #
    #     resp['info']['id'] = str(mtceid.id)
    #
    #     for user in users:
    #         PushHistory(**{'maintenance': str(mtceid.id), 'opt_user': loggend_user.id, 'user': user.id, 'data': sdata,
    #                        'title': title, 'head_type': 0, 'active': 0}).save()
    #
    #     for member in mtceid.users():
    #         push_message(member.id, title, sdata)
    #     resp['alert'] = u'派单成功！请耐心等候维修工回复吧！'
    # else:
    #     resp['status'], resp['alert'] = 0, u'该区域未找到相应的维修人员'
    # resp['info']['count'] = len(users)
    # return json_response(resp)


def batchOp(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    data = get_json_data(request) or request.POST.dict()
    user = User.objects.get(id=ObjectId(data['user_id']))
    type = data.get('type')
    ids = [ObjectId(id) for id in data.get('ids').split(',')]

    if type == 'audit':
        result = Maintenance.objects(id__in=ids)
        for maintenance in result:
            if user.category in ('0', '2', '6', '7'):
                maintenance.settlement = 1
                maintenance.audit_repair_user = user
                maintenance.audit_repair_date = datetime.datetime.now()
                maintenance.audit_repair_result = maintenance.audit_repair_result_save
                if maintenance.audit_repair_result is None:
                    maintenance.audit_repair_result = True
                maintenance.audit_repair_note = maintenance.audit_repair_note_save or ''
                maintenance.save()

            if user.category in ('1', '3', '4', '5', '7'):
                if maintenance.settlement != 1:
                    resp['status'] = 0
                    resp['alert'] = u'存在服务商未审核的订单'
                    continue
                maintenance.settlement = 2
                maintenance.audit_merchant_user = user
                maintenance.audit_merchant_date = datetime.datetime.now()
                maintenance.audit_merchant_result = maintenance.audit_merchant_result_save
                if maintenance.audit_merchant_result is None:
                    maintenance.audit_merchant_result = True
                maintenance.audit_merchant_note = maintenance.audit_merchant_note_save or ''
                maintenance.save()

    if type == 'settle':
        result = Maintenance.objects(id__in=ids)
        for maintenance in result:
            if user.category in ('1', '3', '4', '5', '7'):
                maintenance.settle_merchant_result = maintenance.settle_merchant_result_save
                if maintenance.settle_merchant_result is None:
                    maintenance.settle_merchant_result = True
                maintenance.settle_merchant_user = user
                maintenance.settle_merchant_date = datetime.datetime.now()
                maintenance.settle_merchant_note = maintenance.settle_merchant_note_save or ''

            if user.category in ('0', '2', '6', '7'):
                maintenance.settle_repair_result = maintenance.settle_repair_result_save
                if maintenance.settle_repair_result is None:
                    maintenance.settle_repair_result = True
                maintenance.settle_repair_user = user
                maintenance.settle_repair_date = datetime.datetime.now()
                maintenance.settle_repair_note = maintenance.settle_repair_note_save or ''

            if maintenance.settle_repair_result and maintenance.settle_merchant_result:
                maintenance.settlement = 3

            maintenance.save()

    return json_response(resp)


def stats(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    result = {}

    q = Maintenance.objects()

    result['total'] = q.count()
    result['unfix'] = q.filter(status=0).count()
    result['fixing'] = q.filter(status__in=[1, 3, 5]).count()
    result['fixed'] = q.filter(status=2).count()
    result['cancelled'] = q.filter(status=-1).count()

    today = datetime.date.today()
    result['total_today'] = q.filter(create_time__gte=today).count()
    result['unfix_today'] = q.filter(status=0, create_time__gte=today).count()
    result['fixing_today'] = q.filter(status__in=[1, 3, 5], create_time__gte=today).count()
    result['fixed_today'] = q.filter(status=2, create_time__gte=today).count()
    result['cancelled_today'] = q.filter(status=-1, create_time__gte=today).count()

    result['head_type'] = len(HEAD_BRAND)
    result['stores'] = Store.objects.count()
    result['stores_sh'] = Store.objects(city='上海市').count()
    result['merchant'] = User.objects(category__in=('1', '3', '4', '5'), is_active=1).count()

    repair_qs = User.objects(category__in=('0', '2', '6'), is_active=1)
    result['service'] = len({item.company for item in repair_qs if item.company})
    result['repairer'] = repair_qs.count()

    resp['info']['result'] = result
    return json_response(resp)


def brandList(request):
    resp = {'status': 1, 'info': {}, 'alert': ''}
    resp['info']['results'] = [item for item in DB.brand.find().sort('initial', pymongo.ASCENDING)]
    return json_response(resp)


def test(request):
    import pdb;
    pdb.set_trace()
    return HttpResponse('test')
