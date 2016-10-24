# encoding:utf-8
import datetime
import json
from datetime import timedelta
from datetime import datetime as dt
from mongoengine import *
from django.utils.translation import ugettext_lazy as _
from mongoengine.django.auth import User as BaseUser
from settings import DB, FIX_TIME, SERVICE_COMPANY, USER_CATEGORY
from apps.base.utils import distanceByLatLon, pf, pf4
from apps.base.logger import getlogger
from bson.objectid import ObjectId
from formater import Dict2
from apps.base.logger import getlogger

logger = getlogger(__name__)

HEAD_BRAND = {
    2: u'汉堡王',
    3: u'达美乐',
    4: u'永和大王'
}

USER_CATEGORY = {
    '0': u'维修员',
    '1': u'商户',
    '2': u'维修服务商主管',
    '3': u'商户区域经理',
    '4': u'商户OC',
    '5': u'商户管理员',
    '6': u'维修工区域经理'
}

class User(BaseUser):
    head_type           = IntField(default=0) #1为不是连锁，2:连锁, 3为达美乐
    username            = StringField(max_length=100, required=True)
    password            = StringField(verbose_name=_('Password'))
    name                = StringField(required=True)
    screen_name         = StringField()
    address             = StringField()  # 地址
    works               = ListField(StringField())  #工种
    source              = StringField()  # 所培训厂家
    area                = StringField()  # 区域
    city                = StringField()  # 城市
    mobile              = StringField()  # 手机号码
    tel                 = ListField(StringField())  #门店电话
    loc                 = ListField(FloatField())   #坐标
    device_token        = StringField()
    platform            = StringField()
    app_version         = StringField()
    app_model           = StringField() 
    app_edition         = StringField()
    company             = StringField()  # 公司名称
    company_logo        = StringField()  # 公司的logo
    store               = StringField()  # 门店名称
    store_id            = StringField()  # 门店id
    category            = StringField()  # 1为商户，0为维修员 2为维修服务商主管 3商户区域经理 4商户OC 5商户管理员，6：维修工区域经理
    avatar_img          = StringField(default='/static/images/avatar_l.png')  # 头像
    content             = StringField()  # 描述
    
    card                = ListField(StringField())
    card_type           = IntField(default=0)
    card_no             = StringField() 
    card_msg            = StringField()

    electrician         = StringField()
    electrician_type    = IntField(default=0)
    electrician_day1    = StringField() 
    electrician_day2    = StringField() 
    electrician_msg     = StringField()

    gas                 = StringField() 
    gas_type            = IntField(default=0)
    gas_day1            = StringField() 
    gas_day2            = StringField() 
    gas_msg             = StringField()

    refrigeration       = StringField() 
    refrigeration_type  = IntField(default=0)
    refrigeration_day1  = StringField() 
    refrigeration_day2  = StringField() 
    refrigeration_msg   = StringField()

    train               = ListField(StringField())
    train_name          = ListField(StringField())
    train_type          = ListField(IntField(default=0))
    train_day1          = ListField(StringField())
    train_day2          = ListField(StringField())
    train_msg           = ListField(StringField())
    train_brand         = ListField(StringField())
    train_category      = ListField(StringField())

    is_staff            = BooleanField(default=False, verbose_name=_('Staff Status'))
    is_active           = IntField(default=0) #0为冻结 1为激活 -1为拒绝也就是审核失败
    is_superuser        = IntField(default=0) #0为禁止登陆后台 1为管理后台 2为商家管理后台 3为服务商管理后台
    is_update           = BooleanField(default=False, verbose_name=_('update'))
    create_time         = DateTimeField(default=dt.now)
    update_time         = DateTimeField(default=dt.now)



    @property
    def fix_count(self):
        return DB.maintenance_users.find({'status':1, 'user':self.id}).count()

    @property
    def supplier(self):
        return DB.supplier.find()

    @property
    def trainss(self):
        res = [] 
        for index, i in  enumerate(self.train):
            res.append({
                    'logo':i,
                    'desc':self.train_desc[index] if len(self.train_desc) > index else ''
                })
        return res

    @property
    def category_name(self):
        return USER_CATEGORY.get(self.category)

    @property
    def roles(self):
        res = {}
        roles = DB.role.find()
        user_roles = [i['role'] for i in DB.user_role.find({'user':self.id})]
        for role in roles:
            if role['_id'] in user_roles:
                res[role['code']] = True 
            else:
                res[role['code']] = False
        return Dict2(res) 
        
    #上级用户
    def parent_users(self):
        res = []
        for m in DB.member.find({'user':self.id}):
            res.append(User.objects.get(id=m['opt_user']))
        return res

    #下级用户
    def children_users(self):
        res = []
        for m in DB.member.find({'opt_user':self.id}):
            res.append(User.objects.get(id=m['user']))
        return res
    
    def get_user_profile_dict(self):
        if self.category == '1':
            store = DB.store.find_one({'_id':ObjectId(self.store_id)})
            loc   = []
            if store:
                loc = store.get('loc')
            items = {'id': self.id, 'head_type':self.head_type, 'username': self.username, 'name': self.name, 'avatar_img': self.avatar_img, 'category':
                       self.category, 'company': self.company if self.company else u'无品牌', 'store_id':self.store_id, 'store': self.store, 'mobile': self.mobile, 'loc':loc, 'address': self.address, 'is_active':self.is_active, 'content':self.content, 'tel':self.tel, 'company_logo':self.company_logo}
            items['device_count'] = DB.device.find({'store':ObjectId(self.store_id)}).count()
            items['task_count'] = DB.inventory_header.find({'store':self.store_id}).count()
            items['repair_count'] = DB.maintenance.find({'user':self.id}).count()
            if store:
                items['store_address'] = store.get('address') 
                items['store_no'] = store.get('no')
                items['store_name']   = store.get('name')
            return items
        else:
            item =  {
                    'id': self.id, 
                    'head_type':self.head_type,
                    'username': self.username, 
                    'name': self.name, 
                    'avatar_img': self.avatar_img, 
                    'category':self.category, 
                    'source': self.source, 
                    'area': self.area, 
                    'mobile': self.mobile, 
                    'address': self.address,
                    'screen_name':self.screen_name,
                    'card':','.join(self.card),
                    'card_type':self.card_type,
                    'card_no':self.card_no,
                    'card_msg':self.card_msg,

                    'is_active':self.is_active,
                    'content':self.content
                    }
            if self.electrician:
                item['electrician'] = self.electrician
                item['electrician_type'] = self.electrician_type
                item['electrician_day1'] = self.electrician_day1
                item['electrician_day2'] = self.electrician_day2
                item['electrician_msg'] = self.electrician_msg
            if self.gas:
                item['gas'] = self.gas
                item['gas_type'] = self.gas_type
                item['gas_day1'] = self.gas_day1 
                item['gas_day2'] = self.gas_day2 
                item['gas_msg'] = self.gas_msg
            if self.refrigeration:
                item['refrigeration'] = self.refrigeration
                item['refrigeration_type'] = self.refrigeration_type
                item['refrigeration_day1'] = self.refrigeration_day1 
                item['refrigeration_day2'] = self.refrigeration_day2 
                item['refrigeration_msg'] = self.refrigeration_msg
            trains = []

            def _p(x, y, r=''):
                return x[y] if len(x) > y else r
                
            for index, t in enumerate(self.train):
                trains.append({
                        'img':t,
                        'name':_p(self.train_name, index),
                        'type':_p(self.train_type, index, 0),
                        'day1':_p(self.train_day1, index),
                        'day2':_p(self.train_day2, index),
                        'msg':_p(self.train_msg, index)
                    })
            item['trains'] = trains
            return item



    def save(self, *args, **kwargs):
        self.mobile = self.username
        if self.avatar_img and self.avatar_img.startswith('http://'):
            self.avatar_img = self.avatar_img.split('.com')[1]
        return super(User, self).save(*args, **kwargs)

    meta  = {
            'indexes':[[('loc', '2d')], 'username']
            }


class Role(Document):
    name        = StringField() #权限名称
    code        = StringField() #对应的方法
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)

class UserRole(Document):
    user        = ReferenceField(User)
    role        = ReferenceField(Role)
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)

class Errors(Document):
    no          = StringField()
    price       = FloatField(default=0)
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)
    meta = {'indexes': ['no']}
    
    
class Supplier(Document):
    name        = StringField()
    name2        = StringField()
    initial     = StringField() #首字母
    create_time = DateTimeField(default=dt.now)
    update_time = DateTimeField(default=dt.now)
    meta = {'indexes': ['name','name2']}


class Brand(Document):
    name        = StringField() #品牌
    name2       = StringField() #品牌
    initial     = StringField() #首字母
    create_time = DateTimeField(default=dt.now)  
    update_time = DateTimeField(default=dt.now)
    meta = {'indexes': ['name','name2']} 

class Product(Document):
    head_type           = IntField() #餐厅的类别
    category            = StringField() #类别
    efcategory          = StringField() #设备设施类别
    ecategory           = StringField() #分类
    no                  = StringField() #编号
    barcode             = StringField() #二维码 无用
    purchase_code       = StringField() #采购码
    description         = StringField() #描述
    name                = StringField() #设备名称
    model               = StringField() #型号
    specification       = StringField() #规格
    initial             = StringField() #首字母
    logo                = StringField() #图像
    cert                = StringField()
    brand_name          = StringField() #品牌名称
    supplier            = ReferenceField(Supplier) #厂家 
    brand               = ReferenceField(Brand) #品牌
    repair_time         = IntField() #月份
    create_time         = DateTimeField(default=dt.now)
    update_time         = DateTimeField(default=dt.now)
    meta = {'indexes': ['name','category','no','model','brand_name']}

    def detail(self):
        return {'id':self.id, 'category':self.category, 'name':self.name, 'brand':self.brand, 'model':self.model, 'specifications':self.specification, 'initial':self.initial}

    def spare(self):

        spares = Spare.objects(__raw__={'product_name':self.name, 'brand':self.brand.id, 'model':self.model})
        if spares.count() > 0:
            return list(spares)
        return list(Spare.objects(__raw__={'product_name':self.name, 'brand':self.brand.id}))

class Spare(Document):
    no              = StringField() #编号
    name            = StringField() #名称
    product_name    = StringField() #标准设备名称
    brand           = ReferenceField(Brand)
    brand_name      = StringField() #零件品牌
    content         = StringField() #描述
    model           = StringField() #型号
    price           = FloatField(default=0)
    guarantee       = StringField() #1D 1M 1Y
    warranty1       = IntField()    #整机保固周期（月）零件
    warranty2       = IntField()    #整机保固周期（月）人工
    warranty3       = IntField()    #零件更换后保固周期（月）
    product         = ReferenceField(Product)
    create_time     = DateTimeField(default=dt.now)
    update_time     = DateTimeField(default=dt.now)
    meta            = {'indexes': ['name','no','product']}


class Region(Document):
    rid             = StringField() 
    code            = StringField() 
    name            = StringField() 
    parent_id       = StringField() 
    level           = StringField() 
    order           = StringField() 
    name_en         = StringField() 
    short_name_en   = StringField() 
    meta = {'indexes': ['rid','code','name']}


class ErrorCode(Document):
    head_type       = IntField() #1为所有 2为汉堡王 3为达美乐
    product         = ReferenceField(Product)
    error           = StringField() #故障名称
    code            = StringField() #故障代码
    phen            = StringField() #故障现象说明
    spare           = StringField() #更换零配件名称
    spare_code      = StringField() #零配件编号
    status          = IntField()    #1：紧急 2：一般
    create_time     = DateTimeField(default=dt.now)
    update_time     = DateTimeField(default=dt.now)
    meta = {'indexes': ['head_type','product']}

    def get_result(self):
        items = {'content':self.error, 'status':self.status,'id':str(self.id)}
        call  = DB.call.find_one({'name':self.product.ecategory, 'status_type':self.status})
        if call:
            items.update({'must_time':call.get('status_time1'), 'fix_time':call.get('status_time2')})
        else:
            to_time, fix_time = FIX_TIME[self.status]
            items.update({'must_time':to_time, 'fix_time':fix_time})
        return items

class Feedback(Document):
    user = ReferenceField(User)
    content = StringField() 
    create_time     = DateTimeField(default=dt.now)
    update_time     = DateTimeField(default=dt.now)




    






