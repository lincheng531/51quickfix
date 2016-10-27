# encoding:utf-8
import datetime
import json
from datetime import timedelta
from datetime import datetime as dt
from mongoengine import *
from bson.objectid import ObjectId
from django.utils.translation import ugettext_lazy as _
from mongoengine.django.auth import User as BaseUser
from settings import DB, SERVICE_COMPANY, CALL_STATUS, HOME_FEE, CHARGE
from apps.base.utils import distanceByLatLon, pf, pf2, pf3, pf6, countdown_time
from apps.base.logger import getlogger
from base import User, Product, Supplier, Errors, Spare
from store_schemas import Device
from formater import repair_list, repair_status, repair_status2

logger = getlogger(__name__)

MaintenanceStatus = {
    -1: u'取消',
    0: u'新维修单',
    1: u'接单或者出发中',
    2: u'已经完成',
    3: u'到店',
    4: u'维修失败',
    5: u'填写修单未确认',
    6: u'为暂停'
}

MaintenanceState = {1: u'紧急', 2: u'非紧急'}


class Maintenance(Document):
    code = StringField()  # 报修编号
    user = ReferenceField(User)  # 发起叫修单人
    grab_user = ReferenceField(User)  # 接单人
    product = StringField()
    product_id = ReferenceField(Product)
    supplier = StringField()
    supplier_id = ReferenceField(Supplier)
    area = StringField()  # 区域
    city = StringField()  # 城市
    company = StringField()  # 公司名称
    loc = ListField(FloatField())
    store_name = StringField()
    store = StringField()
    store_no = StringField()  # 餐厅编号
    brand = StringField()  # 设备品牌
    logo = ListField(StringField())
    head_type = IntField(default=1)  # 1是标准版 2是汉堡王
    no = StringField()
    device = StringField()  # 设备id
    address = StringField()
    status = IntField()  # 维修单状态 -1：取消 0：新维修单 1：接单或者出发中 2：已经完成  3:到店  4:维修失败 5:填写修单未确认 6:为暂停 7.被返修
    state = IntField()  # 状态 1:紧急 2:非紧急
    later = StringField()  # 迟到原因
    delayed = StringField()  # 延时原因
    content = StringField()  # 故障描述
    error_code = StringField()  # 故障id
    manager_content = StringField()  # 经理意见
    quit_content = StringField()  # 取消内容
    guarantee = IntField(default=0)  # 0为保修外 1为保修内 -1未知

    single_time = DateTimeField()  # 接单时间
    come_time = DateTimeField()  # 预计到店时间
    must_time = DateTimeField()  # 合约到店时间
    arrival_time = DateTimeField()  # 到店时间
    work_time = DateTimeField()  # 工作完成时间
    work_range = IntField()  # 工作时长
    must_range = IntField()  # 到修时效
    stop = IntField(default=-3)  # 是否暂停 是否暂停 -1是申请暂停 0是确认暂停 -2是拒绝暂停
    stop_content = StringField()  # 暂停原因
    stop_reason = StringField()  # 暂停原因
    stop_day = DateTimeField()  # 预计到达时间
    stop_later = IntField(default=0)  # 1为迟到
    stop_come_time = DateTimeField()  # 暂停再来时间
    work_distance = FloatField()  # 接单距离
    members = ListField(StringField())
    quit_status = IntField(default=0)  # 取消状态
    message = StringField()  # 备注

    start_time = DateTimeField()  # 标准版叫修时间段限制
    end_time = DateTimeField()  # 标准版叫修时间段限制
    is_buy = IntField(default=0)  # 1为采购，接单默认签到，无需签到
    reset_fixed = IntField(default=0)  # 1返修，0为不是返修
    reset_maintenance = StringField()  # 返修标的
    be_reset_fixed = IntField(default=0)  # 1被返修, 0为不被返修

    is_collect = IntField(default=0)  # 是否合辑标的原单
    collected = IntField(default=0)  # 是否合辑分单
    collect_maintenance = StringField()  # 合辑标的

    verify_status = IntField(default=-1)  # 为未导入审核状态 0为新的 1为审核失败 2为审核中

    create_time = DateTimeField(default=dt.now)  # 叫修时间
    update_time = DateTimeField(default=dt.now)

    meta = {'indexes': ['user', 'product_id', 'supplier_id', 'head_type', 'device']}

    @property
    def base_work_time(self):
        return self.arrival_time + timedelta(hours=self.work_range)

    @property
    def stop_work_time(self):
        if self.stop_day:
            return self.stop_day + timedelta(hours=self.work_range)

    @property
    def states(self):
        status = {1: u'紧急', 2: u'非紧急'}
        return status.get(int(self.state))

    @property
    def statuss(self):
        return CALL_STATUS.get(self.status)

    @property
    def title(self):
        return "{}:{}".format(self.store_name, self.product)

    @property
    def bill(self):
        return Bill.objects(maintenance=self, opt_user=self.user).first()

    @property
    def user_count(self):
        return DB.maintenance_users.find({'maintenance': self.id, 'opt_user': self.user.id}).count()

    @property
    def apply_count(self):
        return DB.maintenance_users.find(
                {'maintenance': self.id, 'status': {'$in': [1, 2, 3]}, 'opt_user': self.user.id}).count()

    @property
    def confirm_count(self):
        return DB.maintenance_users.find({'maintenance': self.id, 'status': 2, 'opt_user': self.user.id}).count()

    @property
    def details(self):
        return MaintenanceUsers.objects(maintenance=self, opt_user=self.user).order_by('status')

    @property
    def target(self):
        return MaintenanceUsers.objects.filter(
                **{'maintenance': self.id, 'status__in': [1, 2, 3, 4, 5], 'opt_user': self.user.id}).first()

    @property
    def target_user(self):
        mu = DB.maintenance_users.find_one(
                {'maintenance': self.id, 'status': {'$in': [1, 2, 3, 4, 5, 6]}, 'opt_user': self.user.id})
        return DB.user.find_one({'_id': mu['user']}) if mu else {}

    @property
    def skips(self):
        bconfig = Bconfig.objects(user=self.user).first()
        if bconfig and bconfig.content:
            return bconfig.content.split(',')
        return []

    @property
    def status_list(self):
        return repair_list(self)

    @property
    def send_status(self):
        return repair_status(self)

    @property
    def send_status2(self):
        return repair_status2(self)

    @property
    def can_be_fixed(self):
        if not self.work_time:
            return False

        return (dt.now() - self.work_time) < timedelta(days=1)

    def get_reset_fixes(self, user):
        fixes = []
        origin_id = self.reset_maintenance if self.reset_fixed else self.id

        try:
            origin_maintenance = Maintenance.objects.get(id=ObjectId(origin_id))
        except:
            return fixes

        maintenances = Maintenance.objects.filter(reset_maintenance=str(origin_id))

        if maintenances.count():
            fixes.append({'id': origin_maintenance.id, 'create_time': origin_maintenance.create_time})
            fixes.extend([{'id': item.id, 'create_time': item.create_time} for item in maintenances])

        return fixes

    @property
    def get_collections(self):
        collections = []
        collect = None

        if self.is_collect:
            collect = self
        if self.collected:
            collect_id = str(self.collect_maintenance)
            collect = Maintenance.objects.get(id=ObjectId(collect_id))

        if collect:
            collections.append(
                    collect.get_result(collect=False) if collect.head_type > 1 else collect.get_result1(collect=False))
            collections.extend(
                    [item.get_result(collect=False) if item.head_type > 1 else item.get_result1(collect=False) \
                     for item in Maintenance.objects.filter(collect_maintenance=str(collect.id), be_reset_fixed__ne=1,
                                                            grab_user=self.grab_user)])

        else:
            collections.append(
                    self.get_result(collect=False) if self.head_type > 1 else self.get_result1(collect=False))

        return collections

    def users(self, head_type=0):
        users = []
        details = [self.grab_user] if head_type else [User.objects.get(id=ObjectId(i)) for i in self.members]
        for detail in details:
            parent_user = Member.objects.filter(user=detail).first()
            if parent_user and parent_user.opt_user not in users:
                users.append(parent_user.opt_user)
            users.append(detail)
        return list(set(users))

    def get_result1(self):
        item = {
            'id': str(self.id),
            'code': self.code,
            'head_type': self.head_type,
            'logo': self.user.avatar_img,
            'pic': self.logo,
            'no': self.no,
            'company_logo': self.user.company_logo,
            'name': self.user.name,
            'company': self.user.company,
            'mobile': self.user.mobile,
            'store': self.store_name,
            'store_id': self.store,
            'store_no': self.store_no,
            'area': self.area,
            'city': self.city,
            'address': self.address,
            'loc': self.loc,
            'status': self.status,
            'start_time': pf3(self.start_time),
            'end_time': pf3(self.end_time),
            'single_time': pf3(self.single_time),
            'come_time': pf3(self.come_time),
            'create_time': self.create_time,
            'update_time': self.update_time,
            'charge': CHARGE,
            'home_fee': HOME_FEE,
            'reset_fixed': self.reset_fixed,
            'now_time': dt.now().strftime('%Y-%m-%d %H:%M:%S'),
            'can_be_fixed': self.can_be_fixed,
            'is_collect': self.is_collect,
            'collected': self.collected,
            'manager_content': self.manager_content,
        }

        if self.grab_user:
            item['distance'] = "{}km".format(getattr(self, 'work_distance', 0))
            item['target_user_id'] = str(self.grab_user.id)
            item['target_user_mobile'] = self.grab_user.username
            item['target_user_name'] = self.grab_user.name
            item['target_user_logo'] = self.grab_user.avatar_img
            item['target_come_time'] = self.come_time
            item['target_company'] = self.grab_user.company

        results = []
        bills = Bill.objects.filter(opt_user=self.user, maintenance=self).order_by('-id')

        bs = []
        for bill in bills:
            _item = bill.detail1()
            _item['pic'] = self.logo
            _item['description'] = self.content
            bs.append(_item)
        item['bills'] = bs
        return item

    def get_result(self, category=1):
        item = {
            'id': str(self.id),
            'head_type': self.head_type,
            'code': self.code,
            'logo': self.user.avatar_img,
            'pic': self.logo,
            'no': self.no,
            'company_logo': self.user.company_logo,
            'name': self.user.name,
            'product': self.product,
            'product_id': self.product_id.id if hasattr(self, 'product_id') and self.product_id else '',
            'company': self.user.company,
            'supplier': self.supplier,
            'supplier_id': self.supplier_id.id if hasattr(self, 'supplier_id') and self.supplier_id else '',
            'mobile': self.user.mobile,
            'store': self.store_name,
            'store_id': self.store,
            'store_no': self.store_no,
            'area': self.area,
            'city': self.city,
            'address': self.address,
            'loc': self.loc,
            'status': self.status,
            'state': self.state,
            'device': self.device,
            'bk': self.device,
            'brand': self.brand,
            'stop': self.stop,
            'stop_content': self.stop_content,
            'stop_reason': self.stop_reason,
            'stop_day': self.stop_day,
            'stop_work_time': self.stop_work_time,
            'content': self.content,
            'guarantee': self.guarantee,
            'single_time': self.single_time,
            'arrival_time': self.arrival_time,
            'must_time': self.must_time,
            'quit_content': self.quit_content,
            'create_time': self.create_time,
            'update_time': self.update_time,
            'opt_user_logo': self.user.avatar_img,
            'now_time': dt.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_buy': self.is_buy,
            'later': self.later,
            'delayed': self.delayed,
            'reset_fixed': self.reset_fixed,
            'can_be_fixed': self.can_be_fixed,
            'is_collect': self.is_collect,
            'collected': self.collected,
            'manager_content': self.manager_content,
        }

        item['count'] = len(self.members)

        if self.arrival_time:
            item['come_time'] = self.arrival_time
            item['work_time'] = self.arrival_time + timedelta(hours=self.work_range)
        elif self.come_time:
            item['come_time'] = self.come_time
            item['work_time'] = self.come_time + timedelta(hours=self.work_range)
        elif self.must_time:
            item['come_time'] = self.must_time
            item['work_time'] = self.must_time + timedelta(hours=self.work_range)
        else:
            item['work_time'] = dt.now() + timedelta(hours=self.work_range)
        if self.work_time:
            item['work_time'] = self.work_time

        if self.grab_user:
            item['distance'] = "{}km".format(getattr(self, 'work_distance', 0))
            item['target_user_id'] = str(self.grab_user.id)
            item['target_user_mobile'] = self.grab_user.username
            item['target_user_name'] = self.grab_user.name
            item['target_user_logo'] = self.grab_user.avatar_img
            item['target_come_time'] = self.come_time
            item['target_company'] = self.grab_user.company

        if self.reset_fixed:
            if self.members:
                fix_user = User.objects.get(id=ObjectId(self.members[0]))
                item['fix_name'] = fix_user.name or fix_user.username
            else:
                item['fix_name'] = ''
            if self.reset_maintenance:
                prev_mt = Maintenance.objects.filter(id=ObjectId(self.reset_maintenance),
                                                     create_time__lt=self.create_time).order_by('create_time').first()
                next_mt = Maintenance.objects.filter(id=ObjectId(self.reset_maintenance),
                                                     create_time__gt=self.create_time).order_by('-create_time').first()
                if prev_mt:
                    item['fix_prev'] = str(prev_mt.id)
                if next_mt:
                    item['fix_next'] = str(next_mt.id)

        bill = Bill.objects.filter(opt_user=self.user, maintenance=self).first()
        if bill:
            item['bill'] = bill.detail()
            if item['status'] == 3: item['status'] = 5
        return item


class MaintenanceHistory(Document):
    maintenances = ListField(ReferenceField(Maintenance))
    members = ListField(StringField())
    grab_users = ListField(ReferenceField(User))
    user = ReferenceField(User)
    create_time = DateTimeField(default=dt.now)  # 叫修时间
    update_time = DateTimeField(default=dt.now)


class MaintenanceCollection(Document):
    histories = ListField(ReferenceField(MaintenanceHistory))
    members = ListField(StringField())
    grab_users = ListField(ReferenceField(User))
    user = ReferenceField(User)
    create_time = DateTimeField(default=dt.now)  # 叫修时间
    update_time = DateTimeField(default=dt.now)

    store_name = StringField()
    store = StringField()
    store_no = StringField()  # 餐厅编号
    address = StringField()
    state = IntField()  # 状态 1:紧急 2:非紧急
    must_time = DateTimeField()  # 合约到店时间


    @property
    def states(self):
        status = {1: u'紧急', 2: u'非紧急'}
        return status.get(int(self.state))

    def get_result(self, grab_user=None, members=[]):
        if members:
            member_set = set(members)
            collections = [ \
                item.maintenances[-1].get_result1() \
                    if item.maintenances[-1].head_type == 1 else item.maintenances[-1].get_result() \
                for item in filter(lambda x: set(x.members) & member_set, self.histories)]
        else:
            collections = [ \
                item.maintenances[-1].get_result1() \
                    if item.maintenances[-1].head_type == 1 else item.maintenances[-1].get_result() \
                for item in (filter(lambda x: grab_user in x.grab_users, self.histories) if grab_user else self.histories)]

        return {
            'id': self.id,
            'user_id': self.user.id,
            'grab_users': [item.id for item in self.grab_users],
            'create_time': self.create_time,
            'update_time': self.update_time,
            'collections': collections,
            'store_name': self.store_name,
            'store_id': self.store,
            'store_no': self.store_no,
            'address': self.address,
            'state': self.state,
            'name': self.user.name,
            'logo': self.user.avatar_img,
            'mobile': self.user.mobile,
            'must_time': self.must_time,
        }


# 无用
class MaintenanceUsers(Document):
    code = StringField()  # 报修编号
    user = ReferenceField(User)
    opt_user = ReferenceField(User)
    product = StringField()
    logo = ListField(StringField())
    product_id = ReferenceField(Product)
    supplier = StringField()
    supplier_id = ReferenceField(Supplier)
    area = StringField()  # 区域
    city = StringField()  # 城市
    store = StringField()
    store_name = StringField()
    address = StringField()
    brand = StringField()  # 设备品牌
    category = StringField()  # 报修类别
    company = StringField()  # 公司名称
    status = IntField()  # 维修单状态 -1：取消 0：新维修单 1：接单或者出发中  2：完成  3:到店  4：维修失败 5:已经完成未确认
    loc = ListField(FloatField())
    maintenance = ReferenceField(Maintenance)
    content = StringField()  # 故障描述
    error_code = StringField()  # 故障id

    head_type = IntField(default=1)  # 1是默认 2是汉堡王
    no = StringField()
    device = StringField()  # 设备id
    state = IntField()  # 状态 1:紧急 0:非紧急 2:一般
    guarantee = IntField()  # 0为保修外 1为保修内
    manager_content = StringField()  # 经理意见
    quit_content = StringField()  # 取消内容
    single_time = DateTimeField()  # 接单时间
    come_time = DateTimeField()  # 到店时间
    must_time = DateTimeField()  # 到店时间
    arrival_time = DateTimeField()  # 到达时间
    work_time = DateTimeField()  # 工作完成时间
    work_range = IntField()  # 工作时长
    must_range = IntField()  # 到修时长
    work_distance = FloatField()  # 接单距离
    later = StringField()  # 迟到原因
    stop = IntField(default=-3)  # 是否暂停,-1申请暂停,0确认暂停,-2拒绝暂停
    stop_content = StringField()  # 暂停原因
    stop_reason = StringField()  # 暂停原因
    stop_day = DateTimeField()  # 预计到达时间
    stop_later = IntField(default=0)  # 1为迟到
    stop_come_time = DateTimeField()  # 暂停再来时间
    quit_status = IntField(default=0)  # 取消状态

    start_time = DateTimeField()  # 标准版叫修时间段限制
    end_time = DateTimeField()  # 标准版叫修时间段限制

    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)

    meta = {'indexes': ['opt_user', 'maintenance', 'user', 'product_id', 'supplier', 'head_type', 'device']}

    @property
    def base_work_time(self):
        return self.arrival_time + timedelta(hours=self.work_range)

    @property
    def stop_work_time(self):
        if self.stop_come_time:
            return self.stop_come_time + timedelta(hours=self.work_range)
        if self.stop_day:
            return self.stop_day + timedelta(hours=self.work_range)

    @property
    def skips(self):
        bconfig = Bconfig.objects(user=self.opt_user).first()
        if bconfig and bconfig.content:
            return bconfig.content.split(',')
        return []

    @property
    def no(self):
        if self.product_id:
            device = DB.b_k.find_one({'product': self.product_id.id})
            if device: return device.get('product_no')

    @property
    def title(self):
        return "{}:{}".format(self.store_name, self.product)

    def updates(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
            self.save()
            mtc = self.maintenance
            setattr(mtc, key, value)
            mtc.save()

    def get_result(self, category=1):
        device = DB.device.find_one({'_id': ObjectId(self.device)})
        item = {
            'id': str(self.maintenance.id),
            'logo': self.user.avatar_img,
            'pic': self.logo,
            'product': self.product,
            'store_logo': self.user.avatar_img,
            'company_logo': self.opt_user.company_logo,
            'product_id': self.product_id.id if hasattr(self.product_id, 'id') else '',
            'supplier': self.supplier,
            'supplier_id': self.supplier_id.id if hasattr(self.supplier_id, 'id') else '',
            'area': self.area,
            'city': self.city,
            'brand': self.brand,
            'store': self.store_name,
            'name': self.opt_user.name,
            'company': self.opt_user.company,
            'mobile': self.opt_user.mobile,
            'address': self.address,
            'loc': self.loc,
            'status': self.status,
            'state': self.state,
            'device': self.device,
            'bk': self.device,
            'content': self.content,
            'guarantee': self.guarantee,
            'single_time': self.single_time,
            'arrival_time': self.arrival_time,
            'must_time': self.must_time,
            'no': self.no,
            'stop': self.stop,
            'stop_content': self.stop_content,
            'stop_reason': self.stop_reason,
            'stop_day': self.stop_day,
            'stop_work_time': self.stop_work_time,
            'quit_content': self.quit_content,
            'create_time': self.create_time,
            'update_time': self.update_time,
            'now_time': dt.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        if self.status > 0:
            if self.arrival_time:
                item['come_time'] = self.arrival_time
                item['work_time'] = self.arrival_time + timedelta(hours=self.work_range)
            elif self.come_time:
                item['come_time'] = self.come_time
                item['work_time'] = self.come_time + timedelta(hours=self.work_range)
            elif self.must_time:
                item['come_time'] = self.must_time
                item['work_time'] = self.must_time + timedelta(hours=self.work_range)
            else:
                item['work_time'] = dt.now() + timedelta(hours=self.work_range)
            if self.work_time:
                item['work_time'] = self.work_time
            item['opt_user_logo'] = self.opt_user.avatar_img
            item['target_user_id'] = str(self.user.id)
            item['target_user_mobile'] = self.user.username
            item['target_user_name'] = self.user.name
            item['target_user_logo'] = self.user.avatar_img
            item['target_come_time'] = item.get('come_time', self.come_time)
            item['target_company'] = self.user.company
        # loc = self.user.loc
        mloc = self.opt_user.loc if hasattr(self.opt_user, 'loc') else None
        # if loc and len(loc) == 2 and mloc and len(mloc) == 2:
        item['distance'] = "{}km".format(getattr(self, 'work_distance', 0))
        # item['loc']      = loc
        bill = Bill.objects.filter(user=self.user, maintenance=self.maintenance).first()
        if bill:
            item['bill'] = bill.detail()
            if item['status'] == 3: item['status'] = 5
        return item


class Bill(Document):
    opt_user = ReferenceField(User)
    user = ReferenceField(User)
    maintenance = ReferenceField(Maintenance)
    quality = IntField()
    odm = StringField()
    supplier = ReferenceField(Supplier)
    product = ReferenceField(Product)
    error_code = ReferenceField(Errors)
    product_code = StringField()
    analysis = StringField()  # 分析
    measures = StringField()  # 措施
    spare = ListField(DictField())
    spare_price = FloatField(default=0)
    labor = FloatField(default=0)  # 维修费
    travel = FloatField(default=0)  # 交通费
    stay = FloatField(default=0)  # 住宿天数
    stay_total = FloatField(default=0)  # 住宿费
    total = FloatField(default=0)
    status = IntField(default=0)  # 报价单状态：1:为确认（完成） 0:为未确认 -1:为拒绝 -2:餐厅提交报价单 维修工未报价
    state = IntField(default=0)  # 工单状态：2:餐厅确认完成 1:维修结束  0:新的  -1失败
    content = StringField()  # 描述
    reason = StringField()  # 错误描述

    message = StringField()  # 备注
    # 下面为标准版数据
    labor_hour = FloatField(default=0)
    device = ReferenceField(Device)
    others = ListField(DictField())  # 其他费用 用于标准版
    active = IntField(default=1)  # 是否有效，标准版使用
    will_work_time = DateTimeField()  # 预计完成时效
    # 付款状态
    pay_status = IntField(default=0)

    production_date = DateTimeField()  # 生产日期
    expiration_date = StringField()  # expiration_date
    installation_date = DateTimeField()
    confirm_time = DateTimeField()  # 确认时间
    close_time = DateTimeField()  # 维修员结束工单时间
    repair_pic = ListField(StringField())  # 维修图片
    other_message = StringField()  # 其他建议
    confirm_message = StringField()  # 确认工单备注
    # is_buy情况
    express = StringField()  # 工单编号
    express_logo = StringField()  # 快递单图片
    receipt_logo = ListField(StringField())  # 收货照片
    manager_content = StringField()  # 经理意见

    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)

    meta = {'indexes': ['opt_user', 'user', 'maintenance', 'supplier']}

    @property
    def skips(self):
        bconfig = Bconfig.objects(user=self.opt_user).first()
        if bconfig and bconfig.content:
            return bconfig.content.split(',')
        return []

    @property
    def work_time(self):
        come_time = self.maintenance.come_time
        return pf6(((self.confirm_time or self.update_time) - come_time).total_seconds()) if come_time else ''

    def detail1(self):
        device = self.device
        item = {
            'id': str(self.id),
            'quality': self.quality,
            'odm': self.odm,
            'product': device.product.name,
            'product_id': device.product.id,
            'product_code': self.product_code,
            'error_code': self.error_code.no if hasattr(self.error_code, 'no') else '',
            'error_code_id': str(self.error_code.id) if hasattr(self.error_code, 'id') else '',
            'supplier': device.supplier.name,
            'supplier_id': device.supplier.id,
            'labor': self.labor,
            'total': self.total,
            'state': self.state,
            'analysis': self.analysis,
            'pay_status': self.pay_status,
            'measures': self.measures,
            'message': self.message,
            'reason': self.reason,
            'content': self.content,
            'status': self.status,
            'device': self.device.id,
            'brand': device.brand,
            'others': self.others,
            'labor_hour': self.labor_hour,
            'guarantee': device.guarantee,
            'repair_pic': self.repair_pic,
            'receipt_logo': self.receipt_logo,
            'other_message': self.other_message,
            'offer_time': pf3(self.create_time),
            'work_time': pf3(self.will_work_time),
            'confirm_time': pf3(self.confirm_time),
            'close_time': pf3(self.close_time)
        }

        if not item.get('spare'):
            spares = DB.b_spare.find({'bill': self.id})
            t, sps = 0, []
            for s in spares:
                item2 = {
                    'id': str(s['spare']),
                    'name': s.get('name'),
                    'status': s.get('status'),
                    'category': s.get('category'),
                    'count': s.get('count'),
                    'price': s.get('price', 0),
                    'total': s.get('total', 0)
                }
                if s.get('spare'):
                    spare = DB.spare.find_one({'_id': s['spare']})
                    if spare:
                        item2['base_price'] = spare.get('price')
                        item2['no'] = spare.get('no')
                sps.append(item2)
                t += s.get('total', 0)
            item['spare'] = sps
            item['spare_total'] = t
        return item

    def detail(self):
        item = {
            'id': str(self.id),
            'quality': self.quality,
            'odm': self.odm,
            'product_name': self.product.name if hasattr(self.product, 'name') else '',
            'product_id': str(self.product.id) if hasattr(self.product, 'id') else '',
            'product_code': self.product_code,
            'error_code': self.error_code.no if hasattr(self.error_code, 'no') else '',
            'error_code_id': str(self.error_code.id) if hasattr(self.error_code, 'id') else '',
            'supplier': self.supplier.name if hasattr(self.supplier, 'name') else '',
            'supplier_id': str(self.supplier.id) if hasattr(self.supplier, 'id')  else '',
            'labor': self.labor,
            'travel': self.travel,
            'total': self.total,
            'stay': self.stay,
            'stay_total': self.stay_total,
            'status': self.status,
            'analysis': self.analysis,
            'measures': self.measures,
            'message': self.message,
            'reason': self.reason,
            'content': self.content,
            'others': self.others,
            'repair_pic': self.repair_pic,
            'express_logo': self.express_logo,
            'express': self.express,
            'other_message': self.other_message,
            'receipt_logo': self.receipt_logo,
            'other_message': self.other_message,
            'manager_content': self.manager_content,
            'confirm_message': self.confirm_message,
            'production_date': pf(self.production_date),
            'expiration_date': self.expiration_date,
            'installation_date': pf(self.installation_date),
            'confirm_time': pf3(self.confirm_time),
            'close_time': pf3(self.close_time)
        }

        if self.close_time and self.maintenance.status == 2:
            item['countdown_time'] = countdown_time(24, self.close_time)

        if not item.get('spare'):
            spares = DB.b_spare.find({'bill': self.id})
            t, sps = 0, []
            for s in spares:
                item2 = {
                    'id': str(s['spare']),
                    'name': s.get('name'),
                    'status': s.get('status'),
                    'category': s.get('category'),
                    'count': s.get('count'),
                    'price': s.get('price', 0),
                    'total': s.get('total', 0)
                }
                if s.get('spare'):
                    spare = DB.spare.find_one({'_id': s['spare']})
                    if spare:
                        item2['base_price'] = spare.get('price')
                        item2['no'] = spare.get('no')
                sps.append(item2)
                t += s.get('total', 0)
            item['spare'] = sps
            item['spare_total'] = t
        return item


class Repair(Document):
    user = ReferenceField(User)
    product = ReferenceField(Product)
    supplier = ReferenceField(Supplier)
    product_code = StringField()
    production_date = DateTimeField()
    installation_date = DateTimeField()
    expiration_date = DateTimeField()
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)

    meta = {'indexes': ['user', 'product', 'supplier']}


class BSpare(Document):
    bill = ReferenceField(Bill)
    name = StringField()
    status = IntField()  # 1为保修期内 0为保修期外
    category = IntField()  # 自然 人为
    count = IntField()  # 配件数
    total = FloatField()  # 总价
    price = FloatField()  # 单价
    spare = ReferenceField(Spare)  # 配件id
    device = StringField()  # 配件id
    guarantee = StringField()  # 1D 1M 1Y
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)

    @property
    def over(self):
        return 0 if self.guarantee_time and dt.now() > self.guarantee_time  else 1

    @property
    def guarantee_time(self):
        if self.guarantee:
            if self.guarantee[-1] == 'Y':
                count = float(self.guarantee.replace('Y', ''))
                return self.create_time + timedelta(days=count * 365)
            elif self.guarantee[-1] == 'M':
                count = float(self.guarantee.replace('M', ''))
                return self.create_time + timedelta(days=count * 30)
            elif self.guarantee[-1] == 'D':
                count = float(self.guarantee.replace('D', ''))
                return self.create_time + timedelta(days=count)


class Review(Document):
    user = ReferenceField(User)
    opt_user = ReferenceField(User)
    ask1 = IntField(required=True)
    ask2 = IntField(required=True)
    ask3 = IntField(required=True)
    ask4 = IntField(required=True)
    content = StringField()
    maintenance = ReferenceField(Maintenance)
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)

    def detail(self):
        return {
            'user_id': self.user.id,
            'user_name': self.user.name,
            'opt_user_id': self.opt_user.id,
            'opt_user_name': self.opt_user.name,
            'ask1': self.ask1,
            'ask2': self.ask2,
            'ask3': self.ask3,
            'ask4': self.ask4,
            'maintenance': self.maintenance.id,
            'content': self.content
        }


class Bconfig(Document):
    user = ReferenceField(User)
    content = StringField()
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)

    meta = {'indexes': ['user']}

    def skip(self):
        return [i.strip() for i in self.content.split('|')]


class Member(Document):
    opt_user = ReferenceField(User)
    user = ReferenceField(User)
    category = IntField()  # 2为汉堡王
    area = StringField()  # 区
    city = StringField()  # 城市
    company = StringField()  # 哪个公司
    store = StringField()  # 负责哪个公司
    head_type = IntField()  # 汉堡王：2
    active = IntField(default=1)  # 1为有效 0为失效
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)

    meta = {'indexes': ['head_type', 'area', 'city', 'company']}


class Verify(Document):
    opt_user = ReferenceField(User)  # 餐厅审核人
    user = ReferenceField(User)  # 服务商审核人
    head_type = IntField()  # 2为汉堡王 3为达美乐 4为永和
    status = IntField(default=0)  # 0为新的 1为未通过 2为审核中 3确认结算
    code = StringField()  # 编号
    company = StringField()  # 餐厅
    device = ReferenceField(Device)
    maintenance = ReferenceField(Maintenance)
    opt_user_message = StringField()  # 餐厅审核人备注
    user_message = StringField()  # 服务商审核人
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)
    confirm_time = DateTimeField(default=dt.now)
    refuse_time = DateTimeField(default=dt.now)
    meta = {'indexes': ['head_type', 'status']}

    @property
    def total(self):
        total = 0
        bills = Bill.objects.filter(maintenance=self.maintenance)
        for bill in bills:
            total += bill.total
        return total
