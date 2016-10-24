#!/user/bin/env python
#encoding:utf-8

try:
	import simplejson as json
except:
	import json
from bson.objectid import ObjectId
from django import forms
from mongoengine import *
from datetime import datetime as dt 
from settings import DB, DEVICE_TYPE, DEVICE_CATEGORY, AREA, COMPANY, AREA_CONNECTOR
from apps.base.models import User, Supplier, Product, Device, Store, Region, Brand, Role, Call
from django.core.exceptions import ValidationError
from dateutil import parser as dt_parser
from django.utils.translation import ugettext as _  
from django.utils.safestring import mark_safe
from custom_widget import SelectatorWidget



class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
  
class SpareEditForm(forms.Form):
	brand        = forms.ChoiceField(label=_(u'设备品牌'), required=True, choices=[(str(i.id), i.name) for i in Brand.objects.filter()])
	product_name = forms.CharField(label=_(u'设备名称'), required=True)
	model        = forms.CharField(label=_(u'型号'), required=False)
	no           = forms.CharField(label=_(u'零件编号'), required=False)
	name         = forms.CharField(label=_(u'零件名称'), required=True)
	brand_name   = forms.CharField(label=_(u'零件品牌'), required=False)
	price        = forms.FloatField(label=_(u'零件单价'), required=True)
	warranty1    = forms.FloatField(label=_(u'整机保固周期（月）零件'),required=False)
	warranty2    = forms.FloatField(label=_(u'整机保固周期（月）人工'),required=False)
	warranty3    = forms.FloatField(label=_(u'零件更换后保固周期（月）'),required=False)
	content      = forms.CharField(label=_(u'备注'), required=False, widget=forms.Textarea(attrs={'cols':40, 'rows':3}))
	def clean_brand(self):
		return Brand.objects.get(id=ObjectId(self.cleaned_data['brand']))

class RepairSearchForm(forms.Form):
	def companys():
		c = [('','')]
		c.extend([(i, i) for i in User.objects.filter(category='0').distinct('company')])
		return c
	provider  = forms.ChoiceField(label=_(u'服务商'), choices=companys())
	start_day = forms.DateField(label=_(u'叫修时间1'), required=True, widget=forms.TextInput(attrs={'id':'start_day1'}))
	end_day   = forms.DateField(label=_(u'叫修时间2'), required=True, widget=forms.TextInput(attrs={'id':'end_day1'}))

class AssetsEditForm(forms.Form):
	category            = forms.ChoiceField(label=_(u'类别'), widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), required=True, choices=[(i, i) for i in DEVICE_TYPE.keys()]) 
	#store               = forms.ChoiceField(label=_(u'餐厅'), required=True, choices=[(str(i.id), '{}-{}'.format(i.no,i.name)) for i in Store.objects.filter()])
	no                  = forms.CharField(label=_(u'固定资产编号'),required=False)
	efcategory          = forms.ChoiceField(label=_(u'设备设施类别'), required=True, choices=[(i,i) for i in DEVICE_CATEGORY]) #设备设施类别
	product             = forms.ChoiceField(label=_(u'设备名称'), required=True, choices=[(i.id, '{}-{}-{}'.format(i.name, i.brand_name, i.supplier.name if i.supplier else '')) for i in Product.objects.filter().order_by('-name')]) #设备名称
	#brand               = forms.ChoiceField(label=_(u'品牌'), required=True, choices=[(i.name, i.name) for i in Brand.objects.filter().order_by('-name')]) #品牌
	model               = forms.CharField(label=_(u'型号'), required=False) #型号
	specifications      = forms.CharField(label=_(u'规格'), required=False) #规格
	psnumber            = forms.CharField(label=_(u'生产序列号'), required=False) #生产序列号
	#supplier			= forms.ChoiceField(label=_(u'供应商'), required=True, choices=[(i.id, i.name) for i in Supplier.objects.filter().order_by('-name')])
	expiration_date     = forms.DateField(label=_(u'过保日期'), required=False) #过保日期
	
	def __init__(self, *args, **kwargs):
		self.oid = kwargs.pop('oid', None)
		super(AssetsEditForm, self).__init__(*args, **kwargs)

	def clean_product(self):
		osd = self.cleaned_data['product']
		return Product.objects.get(id=ObjectId(osd))
		

class StoreEditForm(forms.Form):
	name        	= forms.CharField(label=_(u'名称'), required=True)
	no          	= forms.CharField(label=_(u'餐厅编号'), required=True)
	tel             = forms.CharField(label=_(u'固定电话'), required=False)
	fax             = forms.CharField(label=_(u'传真'), required=False)
	address         = forms.CharField(label=_(u'地址'), required=True, widget=forms.Textarea(attrs={'cols':40, 'rows':3}))
	delivery_time   = forms.DateField(label=_(u'交店时间'), required=False)
	opening_time    = forms.DateField(label=_(u'开业时间'), required=True)
	store_manager   = forms.CharField(label=_(u'门店经理'), required=True)
	mobile          = forms.CharField(label=_(u'手机号'), required=True)

	def __init__(self, *args, **kwargs):
		self.oid  = kwargs.pop('oid', None)
		self.user = kwargs.pop('user', None)
		super(StoreEditForm, self).__init__(*args, **kwargs)
		company   = forms.ChoiceField(label=_(u'公司'), required=True,choices=[(c,c) for c in COMPANY.get(self.user.head_type, [])])
		area      = forms.ChoiceField(label=_(u'区域'), required=True, choices=[(a, a) for a in AREA.get(self.user.head_type, [])])
		ccity     = list(Region.objects(__raw__={'rid':{'$regex':'c'}}).order_by('-name'))
		cdistrict = list(Region.objects(__raw__={'rid':{'$regex':'d'}}).order_by('-name'))
		city      = forms.ChoiceField(label=_(u'城市'), required=True, choices=[(c.name, c.name) for c in ccity])
		district  = forms.ChoiceField(label=_(u'区'), required=True, choices=[(d.name, d.name) for d in cdistrict])
		self.fields['company'] = company
		self.fields['area'] = area
		self.fields['city'] = city
		self.fields['district'] = district


	def clean_name(self):
		name = self.cleaned_data['name']
		if self.oid and name:
			if Store.objects.filter(id__ne=self.oid,name=name).first():
				raise ValidationError(u'餐厅名称不得重复')
		return name

	def clean_no(self):
		no = self.cleaned_data['no']
		if self.oid and no:
			if Store.objects.filter(id__ne=self.oid, no=no).first():
				raise ValidationError(u"餐厅编号不得重复")
		return no


class AssetsStoreForm(forms.Form):
	pass

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(AssetsStoreForm, self).__init__(*args, **kwargs)
		ac = [('', u'全部')]
		ac.extend([(i, i) for i in AREA[self.user.head_type]])
		area  = forms.ChoiceField(label=_(u'区域'), widget=forms.Select(attrs={'onchange':'window.location.href="?area="+this.options[this.selectedIndex].value','style':'margin-right:20px;margin-left:6px;'}), required=False,choices=ac)
		cc = [('', u'全部')]
		cc.extend([(i, i) for i in COMPANY[self.user.head_type]])
		company = forms.ChoiceField(label=_(u'所属公司'), widget=forms.Select(attrs={'onchange':'window.location.href="?company="+this.options[this.selectedIndex].value', 'style':'width:200px;margin-left:6px;'}), required=False,choices=cc)
		self.fields['area'] = area
		self.fields['company'] = company

class AssetsSearchForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(AssetsSearchForm, self).__init__(*args, **kwargs)
		cc = [('',u'全部')]
		cc.extend([(i,i) for i in DEVICE_TYPE.keys()])
		category  = forms.ChoiceField(label=_(u'大类'), required=False, widget=forms.Select(attrs={'onchange':'window.location.href="?category="+this.options[this.selectedIndex].value'}), choices=cc)
		ec = [('',u'全部')]
		ec.extend([(i,i) for i in Product.objects.distinct('ecategory')])
		ecategory = forms.ChoiceField(label=_(u'分类'), required=False, widget=forms.Select(attrs={'onchange':'window.location.href="?ecategory="+this.options[this.selectedIndex].value'}), choices=ec)
		self.fields['category'] = category
		self.fields['ecategory'] = ecategory


class StorePassword(forms.Form):
	password = forms.CharField(label=_(u'登陆密码'), required=False, widget=forms.PasswordInput)

class StoreRoleEdit(forms.Form):
	role = forms.MultipleChoiceField(label=_(u'权限'), widget=forms.CheckboxSelectMultiple, required=True, choices=[(str(i.id), i.name) for i in Role.objects.all()])


class BrandEditForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.category = kwargs.pop('category', 'view')
		super(BrandEditForm, self).__init__(*args, **kwargs)

	name = forms.CharField(label=_(u'名称'), required=True)

	def clean_name(self):
		name = self.cleaned_data['name']
		if self.category == 'append':
			if DB.brand.find_one({'name':name}):
				raise ValidationError(u'名称不得重复')
		return name

class SupplierEditForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.category = kwargs.pop('category', 'view')
		super(SupplierEditForm, self).__init__(*args, **kwargs)

	name = forms.CharField(label=_(u'名称'), required=True)

	def clean_name(self):
		name = self.cleaned_data['name']
		if self.category == 'append':
			if DB.supplier.find_one({'name':name}):
				raise ValidationError(u'名称不得重复')
		return name

class ProductAppendForm(forms.Form):
	category         = forms.ChoiceField(label=_(u'类别'), required=True, choices=[(i, i) for i in DEVICE_TYPE.keys()])
	efcategory       = forms.ChoiceField(label=_(u'设备设施类别'), required=True, choices=[(i, i) for i in DEVICE_CATEGORY])
	#ecategory        = forms.CharField(label=_(u'分类'), required=True)
	no               = forms.CharField(label=_(u'编号'), required=False)
	purchase_code    = forms.CharField(label=_(u'采购码'), required=False)
	description      = forms.CharField(label=_(u'描述'), required=False, widget=forms.Textarea(attrs={'cols':40, 'rows':3}))
	name             = forms.CharField(label=_(u'设备名称'), required=True)
	model            = forms.CharField(label=_(u'型号'), required=False)
	specification    = forms.CharField(label=_(u'规格'), required=False)
	supplier         = forms.ChoiceField(label=_(u'厂家'), required=True, choices=[(str(i.id), i.name) for i in Supplier.objects.filter()])
	brand            = forms.ChoiceField(label=_(u'品牌'), required=True, choices=[(str(i.id), i.name) for i in Brand.objects.filter()])
	repair_time      = forms.CharField(label=_(u'保固期'), required=True) 

	def clean_supplier(self):
		return Supplier.objects.get(id=ObjectId(self.cleaned_data['supplier']))

	def clean_brand(self):
		return Brand.objects.get(id=ObjectId(self.cleaned_data['brand'])) 

class CallEditForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.category = kwargs.pop('category', 'view')
		super(CallEditForm, self).__init__(*args, **kwargs)

	city            = forms.ChoiceField(label=_(u'城市'), required=True, choices=[(i.name, i.name) for i in Region.objects(__raw__={'parent_id':{'$regex':'p'}})])
	model           = forms.CharField(label=_(u'型号'), required=False)
	specification   = forms.CharField(label=_(u'规格'), required=False)
	brand           = forms.ChoiceField(label=_(u'品牌'), required=True, choices=[(str(i.id), i.name) for i in Brand.objects.filter()])
	warranty_in     = forms.CharField(label=_(u'保固期内'), required=True)
	warranty_out1   = forms.CharField(label=_(u'保固外 （主服务商）'), required=False)
	warranty_out2   = forms.CharField(label=_(u'保固外（备选服务商1）'), required=False)
	warranty_out3   = forms.CharField(label=_(u'保固外（备选服务商2）'), required=False)
	name            = forms.ChoiceField(label=_(u'标准设备'), required=True, choices=[(i, i) for i in Product.objects.distinct('name')])

	def clean_brand(self):
		return Brand.objects.get(id=ObjectId(self.cleaned_data['brand']))

	def clean_name(self):
		query = {}
		for k, v in self.cleaned_data.iteritems():
			if k in ['city', 'name', 'model', 'specification', 'brand'] and v:
				if k == 'brand':v = v.id
				query[k] = v
		if query:
			if Call.objects(__raw__=query).first() and self.category == 'append':
				raise ValidationError(u'请勿输入重复的标准设备对应服务商表')
		return self.cleaned_data['name']


class StoreAccountAppendForm(forms.Form):
	def __init__(self, *args, **kwargs):

		self.category  = kwargs.pop('category', '1')
		self.head_type = kwargs.pop('head_type')
		self.method    = kwargs.pop('method')
		self.store_id  = kwargs.pop('store_id')
		store_ids      = []
		if self.store_id:
			store_ids = [ObjectId(i) for i in self.store_id.split(',')]

		super(StoreAccountAppendForm, self).__init__(*args, **kwargs)
		if self.category == '1':
			stores = [(i.id, '{}{}'.format(i.no, i.name)) for i in Store.objects.filter(head_type=self.head_type).order_by('-city')]
			self.fields['store'] = forms.ChoiceField(label=_(u'负责餐厅'), required=True, choices=stores)
		elif self.category == '3':
			self.fields['area'] = forms.ChoiceField(label=_(u'负责区域'),required=True, choices=[(i, i) for i in AREA_CONNECTOR[self.head_type]])
		elif self.category == '4':
			self.fields['store'] = forms.MultipleChoiceField(label=_(u'负责餐厅'), widget=SelectatorWidget(attrs={'multiple':'','width':'400px'}), required=True, choices=[(i.id, '{}({})'.format(i.name, i.no)) for i in Store.objects.filter(head_type=self.head_type).order_by('-no')])

	name        	= forms.CharField(label=_(u'名称'), required=True)
	mobile         	= forms.CharField(label=_(u'手机号码'), required=True)
	password        = forms.CharField(label=_(u'登陆密码'), required=False, widget=forms.PasswordInput)

	#def clean_mobile(self):
	#	mobile = self.cleaned_data['mobile']
	#	if mobile and self.method == 'save':
	#		if User.objects.filter(username=mobile).first():
	#			raise ValidationError(u'手机号码不得重复')
	#	return mobile

	def clean_password(self):
		password = self.cleaned_data['password']
		if self.method == 'save':
			if len(password) < 6:
				raise ValidationError(u'密码不得小于6个字符')
		return password
 
	def clean_area(self):
		area = self.cleaned_data['area']
		if area and area not in AREA_CONNECTOR[self.head_type].keys():
			raise ValidationError(u'不在指定的区域')
		return area

	def clean_store(self):
		store = self.cleaned_data['store']
		if store:
			if self.category == '4':
				return Store.objects.filter(id__in =[ObjectId(i) for i in store])
			return Store.objects.get(id=ObjectId(store))














