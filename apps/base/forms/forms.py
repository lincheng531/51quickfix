#!/user/bin/env python
#encoding:utf-8

from pprint import pprint
from bson.objectid import ObjectId
from django import forms
from mongoengine import *
from datetime import datetime as dt
from settings import DB
from apps.base.models import User, Supplier, Product
from django.core.exceptions import ValidationError
from dateutil import parser as dt_parser
from django.utils.translation import ugettext as _



class StuffLoginForm(forms.Form):
    username = forms.CharField(
        label=_('admin username'), max_length=14, min_length=6, required=True)
    password = forms.CharField(label=_(
        'password'), max_length=20, min_length=6, required=True, widget=forms.PasswordInput)

class SearchAccountForm(forms.Form):
    is_active = forms.ChoiceField(label=_(u'审核状态'), required=True, choices=[(0, u'审核中'), (1, u'已审核'), (-1, u'审核未通过')])
    name   = forms.ChoiceField(label=_(u'名称'), required=True, choices=[(str(i['_id']), i['name']) for i in DB.user.find()])
    mobile = forms.ChoiceField(label=_(u'手机号码'), required=True, choices=[(str(i['_id']), i['mobile']) for i in DB.user.find()])

class SearchMaintenanceForm(forms.Form):
    store = forms.ChoiceField(label=_(u'门店名称'), required=True, choices=[(i.get('store'), i.get('store')) for i in DB.user.find() if i.get('store')])

class SearchBillForm(forms.Form):
    odm = forms.ChoiceField(label=_(u'ODM'), required=True, choices=[(str(i['_id']), i.get('odm')) for i in DB.bill.find()])
    errorcode = forms.ChoiceField(label=_(u'Error Code'), required=True, choices=[(str(i['_id']), i.get('no')) for i in DB.errors.find()])
    opt_user = forms.ChoiceField(label=_(u'商家'), required=True, choices=[(str(i['_id']), i.get('name')) for i in DB.user.find()])
    user = forms.ChoiceField(label=_(u'维修员'), required=True, choices=[(str(i['_id']), i.get('name')) for i in DB.user.find()])

class SearchProductForm(forms.Form):
    name = forms.CharField(label=_(u'名称'), required=True)


class SupplierForm(forms.Form):
    name = forms.CharField(label=_(u'名称'), required=True)


class ProductForm(forms.Form):
    name = forms.CharField(label=_(u'名称'), required=True)
    logo = forms.CharField(label=_(u'图像'), required=True)
    cert = forms.ChoiceField(
        label=_(u'证书'), choices=((u'电工证', u'电工证'), (u'煤气证', u'煤气证'), (u'制冷正', u'制冷证')))
    supplier = forms.ChoiceField(label=_(u'厂家'), required=True, choices=[(str(i['_id']), i['name']) for i in DB.supplier.find()])

    def clean_supplier(self):
        sid = self.cleaned_data['supplier']
        return Supplier.objects.get(id=ObjectId(sid))


class VerifyForm(forms.Form):
	name = forms.CharField(label=_(u'名称'), required=True)
	is_active = forms.ChoiceField(label=_(u'审核'), choices=(
	    ('1', u'审核通过'),('0', u'审核中'), ('-1', u'审核不通过')), widget=forms.RadioSelect)
	content = forms.CharField(label=_(u'原因'), widget=forms.Textarea(
	    attrs={'cols': 3, 'rows': 3}), required=False)

class SpareForm(forms.Form):
    name = forms.CharField(label=_(u'备件名称'), required=True)
    price = forms.FloatField(label=_(u'单价'), required=True)

class ErrorsForm(forms.Form):
    no    = forms.CharField(label=_(u'错误代码'), required=True)
    price = forms.FloatField(label=_(u'单价'), required=True)

class RepairForm(forms.Form):
    user    = forms.ChoiceField(label=_(u'商家'), choices=[(i.id, i.name) for i in User.objects(category='1')])
    product = forms.ChoiceField(label=_(u'产品名称'), choices=[(i.id, i.name) for i in Product.objects.all()])
    supplier = forms.ChoiceField(label=_(u'供应商'), choices=[(i.id, i.name) for i in Supplier.objects.all()])
    product_code = forms.CharField(label=_(u'编码'),required=True)
    production_date     = forms.CharField(label=_(u'生产日期'),required=True)
    installation_date   = forms.CharField(label=_(u'安装日期'),required=True)
    expiration_date     = forms.CharField(label=_(u'维修日期'),required=True)

    def clean_user(self):
        user = self.cleaned_data['user']
        return User.objects.get(id=ObjectId(user))

    def clean_product(self):
        product = self.cleaned_data['product']
        return Product.objects.get(id=ObjectId(product))

    def clean_supplier(self):
        supplier = self.cleaned_data['supplier']
        return Supplier.objects.get(id=ObjectId(supplier))
    
    def clean_production_date(self):
        production_date = self.cleaned_data['production_date']
        return dt.strptime(production_date, '%Y-%m-%d')


    def clean_installation_date(self):
        installation_date = self.cleaned_data['installation_date']
        return dt.strptime(installation_date, '%Y-%m-%d')

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        return dt.strptime(expiration_date, '%Y-%m-%d')


class BconfigForm(forms.Form):
    user        = forms.ChoiceField(label=_(u'商家'), choices=[(i.id, i.name) for i in User.objects(category='1')])
    content     = forms.CharField(label=_(u'不需要填写的字段'),widget=forms.Textarea(attrs={'rows':10,'cols':40}),required=True)


class AccountAppendForm(forms.Form):
    no   = forms.CharField(label=_(u'餐厅编号'), required=True)
    name  = forms.CharField(label=_(u'用户名'), required=True)
    mobile = forms.CharField(label=_(u'手机号码'), required=True)

class AccountAppend1Form(forms.Form):
    area    = forms.CharField(label=_(u'区域'), required=True)
    city    = forms.CharField(label=_(u'城市'), required=True)
    company = forms.CharField(label=_(u'服务商'), required=True)
    provider_manager_name   = forms.CharField(label=_(u'维修主管名称'), required=True)
    provider_manager_mobile = forms.CharField(label=_(u'维修主管手机'), required=True)
    service_name   = forms.CharField(label=_(u'维修工名称'), required=True)
    service_mobile = forms.CharField(label=_(u'维修工手机'), required=True)
    electrician    = forms.CharField(label=_(u'电工操作证号'), required=False)
    refrigeration  = forms.CharField(label=_(u'制冷证号码'), required=False)
    area_manager_name   = forms.CharField(label=_(u'区域经理名称'), required=True)
    area_manager_mobile = forms.CharField(label=_(u'区域经理手机号码'), required=True)
  
