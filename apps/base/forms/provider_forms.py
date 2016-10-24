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
from apps.base.models import User, Supplier, Product, Device, Store, Region, Brand, Role, Region
from django.core.exceptions import ValidationError
from dateutil import parser as dt_parser
from django.utils.translation import ugettext as _  
from django.utils.safestring import mark_safe
from custom_widget import SelectatorWidget

	
class ProviderAccountAppendForm(forms.Form):
	def __init__(self, *args, **kwargs):

		self.category  = kwargs.pop('category', '1')
		self.method    = kwargs.pop('method') 
		self.company   = kwargs.pop('company')
		super(ProviderAccountAppendForm, self).__init__(*args, **kwargs)
		if self.category == '2':
			self.fields['repair_user'] = forms.MultipleChoiceField(label=_(u'下属维修工'), widget=SelectatorWidget(attrs={'multiple':'','width':'400px'}),choices=[(i.id, i.name) for i in User.objects(__raw__={'company':self.company, 'category':'0'})])

		#if self.category == '6':
		#	self.fields['manager'] = forms.ChoiceField(label=_(u'主管'),choices=[(i.id, i.name) for i in User.objects(__raw__={'company':self.company, 'category':'2'})])
		

	city            = forms.ChoiceField(label=_(u'城市'), required=True, choices=[(c.name, c.name) for c in Region.objects(__raw__={'rid':{'$regex':'c'}}).order_by('-name')])
	name        	= forms.CharField(label=_(u'名称'), required=True)
	mobile         	= forms.CharField(label=_(u'手机号码'), required=True)
	password        = forms.CharField(label=_(u'登陆密码'), required=False, widget=forms.PasswordInput)

	def clean_mobile(self):
		mobile = self.cleaned_data['mobile']
		if mobile and self.method == 'save':
			if User.objects.filter(username=mobile).first():
				raise ValidationError(u'手机号码不得重复')
		return mobile

	def clean_password(self):
		password = self.cleaned_data['password']
		if self.method == 'save':
			if len(password) < 6:
				raise ValidationError(u'密码不得小于6个字符')
		return password
 














