# encoding:utf-8
import datetime
import json
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from mongoengine import *
from bson.objectid import ObjectId 
from django.utils.translation import ugettext_lazy as _
from mongoengine.django.auth import User as BaseUser
from settings import DB, CALL_STATUS
from apps.base.utils import distanceByLatLon, pf
from apps.base.logger import getlogger
from base import User, Product, Supplier, Errors, Brand

logger = getlogger(__name__)

#推送表
class Push(Document):
    area                = StringField() #区域
    city                = StringField() #城市
    head_type           = IntField() #2 为汉堡王
    provider            = StringField() #服务商主管
    service             = StringField() #维修师傅
    company             = StringField()
    area_manager        = ListField(StringField()) #二级推送
    manager             = ListField(StringField())  #汉堡王区域负责人
    hq                  = ListField(StringField())  #汉堡王总部负责人
    create_time         = DateTimeField(default=dt.now)
    update_time         = DateTimeField(default=dt.now)


#餐厅
class Store(Document):
    head_type               = IntField() #1为所有 2为汉堡王 3为达美乐
    rid                     = StringField() #唯一标识
    old_rid                 = StringField() #旧唯一标识
    uid                     = StringField() #流水号
    area                    = StringField() #位置:华东区 华南区 华北区 加盟区
    city                    = StringField() #城市
    district                = StringField() #区
    address                 = StringField() #地址
    name                    = StringField() #名称
    no                      = StringField() #餐厅编号
    brand                   = StringField() #品牌
    delivery_time           = DateTimeField() #交店时间
    opening_time            = DateTimeField() #开业时间
    close_time              = DateTimeField() #关店时间
    tel                     = StringField() #固定电话
    company                 = StringField() #公司
    loc                     = ListField(FloatField()) #坐标地址
    fax                     = StringField()    #传真
    store_manager           = StringField()    #门店经理
    mobile                  = StringField()    #餐厅经理电话
    phone                   = StringField()    #手机号码
    logo                    = ListField(StringField(default='/static/images/avatar_l.png')) #logo图片
    #card                    = StringField() #营业执照不得为空
    #over_day                = DateTimeField() #过期时间
    #card1                   = StringField() #税务登记证不得为空
    #over_day1               = DateTimeField() #过期时间
    operation_supervision   = StringField()  #营运督导
    zipcode                 = StringField()    #餐厅编号
    email                   = StringField()    #邮件地址
    franchisee              = StringField()    #加盟商
    business_hours          = StringField()    #营业时间
    business_type           = StringField()    #营业类型 加盟和直营
    initial                 = StringField()    #首字母
    is_active               = IntField(default=1) #-1为审核不通过，0为未审核，1为审核通过 
    
    licence                 = StringField()    #营业执照
    licence_type            = IntField(default=0) #1和通过 0为失败
    licence_day             = DateTimeField()  #有效时期开始
    licence_day1            = DateTimeField()  #有效期结束
    licence_msg             = StringField()    #失败原因
    certificate             = StringField()    #税务登记证
    certificate_type        = IntField(default=0) #1和通过 0为失败
    certificate_day         = DateTimeField()  #有效时期开始
    certificate_day1        = DateTimeField()  #有效期结束
    certificate_msg         = StringField()    #失败原因

    create_time             = DateTimeField(default=dt.now)
    update_time             = DateTimeField(default=dt.now)

    meta = {'indexes': ['rid','head_type']}
    
    def status_list(self):
        results = []
        mtcs = DB.maintenance_users.find({'store':str(self.id), 'status':{'$in':[2, 3, 4, 5]}}).sort('_id', -1)
        for m in mtcs:
            user = DB.user.find_one({'_id':m['user']})
            if user:
                results.append({
                        'name':user['name'],
                        'mobile':user['username'],
                        'product':m.get('product'),
                        'brand':m.get('brand',''),
                        'company':m.get('company'),
                        'city':m.get('city'),
                        'error':m.get('content'),
                        'status':CALL_STATUS.get(m.get('status')),
                        'create_time':m.get('create_time').strftime('%Y-%m-%d')
                    })
        return results

    @property
    def  over_status(self):
        return 1 if self.address and self.area and self.address and self.no and self.opening_time else 0

    @property
    def device_count(self):
        return DB.device.find({'store':self.id}).count()

    @property
    def devices(self):
        #return DB.device.find({'store':self.id})
        return Device.objects.filter(store=self)


class Device(Document): 
    head_type           = IntField() #1为所有 2为汉堡王 3为达美乐
    rid                 = StringField() #唯一标识
    old_rid             = StringField() #旧唯一标识
    uid                 = StringField() #流水号
    store               = ReferenceField(Store)
    no                  = StringField() #固定资产编号
    restaurant_name     = StringField() #餐厅名称
    restaurant_no       = StringField() #餐厅编号
    product_no          = StringField() #设备编号
    po_no               = StringField() #PO NO
    name                = StringField() #设备名称
    product             = ReferenceField(Product)
    supplier			= ReferenceField(Supplier)
    status              = StringField()
    area                = StringField() #区域 
    city                = StringField() #城市
    description         = StringField() #描述 
    qty                 = StringField() #数量
    price               = StringField() #单价 
    amount              = FloatField() #合计
    installation        = StringField() #安装费 厂商 Installation  
    freight             = FloatField() #运输费 粤中 Freight
    other_fee           = FloatField() #其它费用 Other Fee 
    remarks             = StringField() #备注 Remarks    
    provider            = StringField() #提供者 Provider 服务商
    model               = StringField() #型号
    production_date     = DateTimeField() #生产日期
    installation_date   = DateTimeField() #安装日期
    expiration_date     = DateTimeField() #过保日期
    category            = StringField() #类别
    efcategory          = StringField() #设备设施类别
    ecategory           = StringField() #分类
    brand               = StringField() #品牌
    efassets            = StringField() #固定资产编码号
    wccode              = StringField() #财务类别代码
    manufacturer        = StringField() #制作厂商
    specifications      = StringField() #规格
    psnumber            = StringField() #生产序列号
    state               = StringField() #使用状态
    storage             = StringField() #存放地
    purchase_date       = StringField() #购置日期
    company             = StringField() #单位
    scrap_time          = StringField() #报废时限
    per_month           = FloatField()  #每月折旧金额
    must_time           = FloatField()  #到店时间
    work_time           = FloatField()  #工作时间
    initial             = StringField()
    tax_rate            = FloatField() #税率
    tax                 = FloatField() #税额
    amount              = FloatField() #合计（不含税）
    remarks             = StringField() #备注
    logo                = ListField(StringField()) #logo
    create_time         = DateTimeField(default=dt.now)
    update_time         = DateTimeField(default=dt.now)

    meta = {'indexes': ['rid','head_type','store']}

    def get_result(self):
        return {
            "id": str(self.id),
            "head_type": self.head_type,
            "rid": self.rid,
            "uid": self.uid,
            "store": {
                'id': str(self.store.id),
                'name': self.store.name,
            },
            "name": self.name,
            "product": str(self.product.id),
            "supplier": self.supplier.name,
            "model": self.model,
            "category": self.category,
            "efcategory": self.efcategory,
            "ecategory": self.ecategory,
            "brand": self.brand,
            "specifications": self.specifications,
            "logo": self.logo,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "expiration_date": self.expiration_date,
            "psnumber": self.psnumber,
            "manufacturer": self.manufacturer,
            "provider": self.provider,
        }

    @property
    def over_status(self):
        return 1 if self.name and self.brand and self.model and self.specifications else 0
    
    @property
    def guarantee_time(self):
        if self.expiration_date:
            return self.expiration_date
        opening_time = self.store.opening_time
        if not opening_time:
            return -2 
        repair_time  = self.product.repair_time
        if not repair_time:
            return -1 
        return opening_time + relativedelta(months=+repair_time)
    
    @property
    def guarantee(self):
        if self.head_type == 2:
            opening_time = self.store.opening_time
            if not opening_time:
                return -2 
            repair_time  = self.product.repair_time
            if not repair_time:
                return -1
            over_time = opening_time + relativedelta(months=+repair_time) 
            return 1 if over_time > dt.now() else 0

        return 1

    @property
    def product_id(self):
        return str(self.product.id) if self.product else ''

    def assets(self): 
        results = []
        mtcs = DB.maintenance.find({'device':str(self.id)}).sort('_id', -1)
        for m in mtcs:
            mtuc =  DB.maintenance_users.find_one({'maintenance':m['_id'], 'status':{'$in':[1, 2, 3, 4, 5]}, 'opt_user':m['user']})
            if mtuc:
                user = DB.user.find_one({'_id':mtuc['user']})
                if user:
                    results.append({
                            'status':CALL_STATUS.get(mtuc.get('status')),
                            'error':mtuc.get('content'),
                            'create_time':mtuc.get('create_time').strftime(u'%Y年%m月%d日'),
                            'city':mtuc.get('city'),
                            'company':mtuc.get('company'),
                            'name':user.get('name'),
                            'mobile':user.get('mobile')
                        })
        return results
    
    def detail(self):
        guarantee = self.guarantee
    	return {'no':self.no, 'name':self.name, 'brand':self.brand, 'status':self.status, 'id':str(self.id), 'guarantee':guarantee, 'product':self.product_id}

    
class PushHistory(Document):  
    opt_user        = ReferenceField(User)
    user            = ReferenceField(User)
    maintenance     = StringField()
    title           = StringField()
    data            = DictField()
    to_mobile       = StringField()
    to_name         = StringField()
    head_type       = IntField(default=0) #0为叫修呼叫
    category        = IntField(default=1) #1为维修工 2维修工上海负责人 3汉堡王上海负责人 4汉堡王总部
    status          = IntField(default=1) #0为发送失败 1为发送成功
    active          = IntField(default=0) #0为未完成 1未完成
    create_time     = DateTimeField(default=dt.now)
    update_time     = DateTimeField(default=dt.now)
    meta = {'indexes': ['maintenance','head_type','category']}


class Call(Document):
    head_type       = IntField() #2为汉堡王 3为打达美乐
    city            = StringField() #城市
    product         = ReferenceField(Product)
    name            = StringField() #产品名称
    brand           = ReferenceField(Brand) #产品型号
    model           = StringField() 
    specification   = StringField()
    warranty_in     = StringField() #保固期内
    warranty_out1   = StringField() #保固外 （主服务商）
    warranty_out2   = StringField() #保固外（备选服务商1）
    warranty_out3   = StringField() #保固外（备选服务商2）
    create_time     = DateTimeField(default=dt.now)
    update_time     = DateTimeField(default=dt.now)
    meta = {'indexes': ['city']}


class Charge(Document):
    head_type       = IntField() #2汉堡王 3达美乐
    company         = StringField() #公司
    area            = StringField() #覆盖区域
    status          = IntField() #1为紧急 2为非紧急
    time_slot       = StringField() #时间段 
    head_type       = IntField() #类型 汉堡王为2
    fix_time        = FloatField() #规定修复时效（h） 
    fix_time_type   = IntField() #8-20 为1 其他为2        
    quickfix        = FloatField() #紧急维修->规定到修时效（h）
    quickfix1       = FloatField() #紧急维修->人工费 RMB/h  规定修复时效内 
    quickfix2       = FloatField() #紧急维修->人工费 RMB/h  超出时效1小时内 
    quickfix3       = FloatField() #紧急维修->最高人工费 RMB  超出时效1小时以上
    quickfix4       = FloatField() #紧急维修->住宿费 RMB/人/晚  
    traffic1        = FloatField() #交通费->市内 紧急   交通费（距离为报修点与最近的服务商点）
    traffic2        = FloatField() #交通费->市外 100km—150km 交通费（距离为报修点与最近的服务商点）
    traffic3        = FloatField() # 交通费->市外 150km—200km 交通费（距离为报修点与最近的服务商点）
    create_time     = DateTimeField(default=dt.now)
    update_time     = DateTimeField(default=dt.now)
    meta = {'indexes': ['head_type','area','time_slot']}


class InventoryHeader(Document):
    head_type   = IntField()
    title       = StringField() #盘点标题
    start_time  = DateTimeField()
    end_time    = DateTimeField()
    total       = IntField(default=0)
    complete    = IntField(default=0)
    status      = IntField(default=0) #0为未盘点
    store       = ListField(StringField())
    scope       = StringField()
    create_time = DateTimeField(default=dt.now)  
    update_time = DateTimeField(default=dt.now) 

     
    @property
    def stores(self):
        res = []
        stores = Store.objects.filter(id__in=[ObjectId(i) for i in self.store])
        for store in stores:
            lost = InventoryDetail.objects.filter(header=self, store=store, status=0).count()
            complete = InventoryDetail.objects.filter(header=self, store=store, status=2).count()
            miss     = InventoryDetail.objects.filter(header=self, store=store, status=1).count()
            item = {'lost':lost, 'complete':complete+miss, 'total':lost+complete+miss, 'miss':miss}
            if lost == 0:
                item['status'] = 2
            elif complete == 0:
                item['status'] = 0
            else:
                item['status'] = 1
            for k, v in item.iteritems():
                setattr(store, k, v)
            store.save(store)
            res.append(store)
        return res
    

class InventoryDetail(Document):
    header      = ReferenceField(InventoryHeader)
    device      = ReferenceField(Device) 
    store       = ReferenceField(Store)
    status      = IntField(default=0) #0为未盘点 1为缺失 2为存在
    cate        = IntField(default=0) #0为手工盘点 1为自动盘点
    content     = StringField() #使用说明
    logo        = ListField(StringField()) #盘点图片
    product     = ReferenceField(Product)
    brand       = StringField()
    ecategory   = StringField()
    category    = StringField()
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)








