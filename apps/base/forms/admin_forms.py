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
from django.core.exceptions import ValidationError
from dateutil import parser as dt_parser
from django.utils.translation import ugettext as _  
from django.utils.safestring import mark_safe
from settings import DB, DEVICE_CATEGORY

		
class StoreEditAppendForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(StoreEditAppendForm, self).__init__(*args, **kwargs)

	licence_type    = forms.ChoiceField(label=_(u'营业执照审核'), required=True, widget=forms.RadioSelect(attrs={'v':'licence', 'class':'licence'}), choices=[(1, u'审核正常'),(-1, u'审核失败'), (0, u'审核中')])
	licence_day 	= forms.DateField(label=_(u'起始时间'), required=False, widget=forms.DateInput(attrs={'class':'licence1'}))
	licence_day1    = forms.DateField(label=_(u'结束时间'), required=False, widget=forms.DateInput(attrs={'class':'licence1'}))
	licence_msg     = forms.CharField(label=_(u'失败原因'), required=False, widget=forms.Textarea(attrs={'cols':42, 'rows':3, 'class':'licence0'}))

	certificate_type = forms.ChoiceField(label=_(u'税务登记证审核'), required=True, widget=forms.RadioSelect(attrs={'v':'certificate','class':'certificate'}), choices=[(1, u'审核正常'),(-1, u'审核失败'), (0, u'审核中')])
	certificate_day  = forms.DateField(label=_(u'起始时间'), required=False, widget=forms.DateInput(attrs={'class':'certificate1'}))
	certificate_day1 = forms.DateField(label=_(u'结束时间'), required=False, widget=forms.DateInput(attrs={'class':'certificate1'}))
	certificate_msg  = forms.CharField(label=_(u'失败原因'), required=False, widget=forms.Textarea(attrs={'cols':42, 'rows':3, 'class':'certificate0'}))


class AccountPassword(forms.Form):
	password   = forms.CharField(label=_(u'登陆密码'), required=False, widget=forms.PasswordInput)



class AccountEditForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(AccountEditForm, self).__init__(*args, **kwargs)
		brands = [('','')]
		brands.extend([(i.get('name'), i.get('name')) for i in DB.brand.find()])
		categorys = [('','')]
		categorys.extend([(i,i) for i in DEVICE_CATEGORY])
		for index, train in enumerate(self.user.train):
			if train:
				self.fields['train_type_{}'.format(index)] = forms.ChoiceField(label=_(u'审核'), widget=forms.RadioSelect(attrs={'class':'train{}'.format(index)}), required=True, choices=[(1, u'审核通过'), (-1, u'审核失败'), (0, u'审核中')])
				self.fields['train_name_{}'.format(index)] = forms.CharField(label=_(u'证件名称'), required=False, widget=forms.TextInput(attrs={'class':'train{}1'.format(index)}))
				self.fields['train_brand_{}'.format(index)] = forms.ChoiceField(label=_(u'品牌'), widget=forms.Select(attrs={'class':'train{}1'.format(index)}),required=False, choices=brands)
				self.fields['train_category_{}'.format(index)] = forms.ChoiceField(label=_(u'设备'), widget=forms.Select(attrs={'class':'train{}1'.format(index)}), required=False, choices=categorys)
				self.fields['train_day1_{}'.format(index)] = forms.DateField(label=_(u'有效期起始'), required=False, widget=forms.DateInput(attrs={'class':'train{}1'.format(index)}))
				self.fields['train_day2_{}'.format(index)] = forms.DateField(label=_(u'有效期结束'), required=False, widget=forms.DateInput(attrs={'class':'train{}1'.format(index)}))
				self.fields['train_msg_{}'.format(index)] = forms.CharField(label=_(u'原因'), required=False, widget=forms.Textarea(attrs={'cols':42, 'rows':3, 'class':'train{}0'.format(index)}))

	card_type   = forms.ChoiceField(label=_(u'审核'), required=True, widget=forms.RadioSelect(attrs={'class':'card'}), choices=[(1, u'审核通过'), (-1, u'审核失败'), (0, u'审核中')])
	screen_name = forms.CharField(label=_(u'用户名'), required=False, widget=forms.TextInput(attrs={'class':'card1'}))
	card_no     = forms.CharField(label=_(u'身份证号码'), required=False, widget=forms.TextInput(attrs={'class':'card1'}))
	card_msg    = forms.CharField(label=_(u'失败原因'), required=False, widget=forms.Textarea(attrs={'class':'card0', 'cols':42, 'rows':3}))

	electrician_type  = forms.ChoiceField(label=_(u'审核'), widget=forms.RadioSelect(attrs={'v':'electrician', 'class':'electrician'}), required=True, choices=[(1, u'审核通过'), (-1, u'审核失败'), (0, u'审核中')])
	electrician_day1  = forms.DateField(label=_(u'有效期起始'), required=False, widget=forms.DateInput(attrs={'class':'electrician1'}))
	electrician_day2  = forms.DateField(label=_(u'有效期结束'), required=False, widget=forms.DateInput(attrs={'class':'electrician1'}))
	electrician_msg   = forms.CharField(label=_(u'失败原因'), required=False, widget=forms.Textarea(attrs={'cols':42, 'rows':3, 'class':'electrician0'}))

	gas_type  = forms.ChoiceField(label=_(u'审核'), required=True, widget=forms.RadioSelect(attrs={'v':'gas', 'class':'gas'}), choices=[(1, u'审核通过'), (-1, u'审核失败'), (0, u'审核中')])
	gas_day1  = forms.DateField(label=_(u'有效期起始'), required=False, widget=forms.DateInput(attrs={'class':'gas1'}))
	gas_day2  = forms.DateField(label=_(u'有效期结束'), required=False, widget=forms.DateInput(attrs={'class':'gas1'}))
	gas_msg   = forms.CharField(label=_(u'失败原因'), required=False, widget=forms.Textarea(attrs={'class':'gas0', 'cols':42, 'rows':3}))

	refrigeration_type  = forms.ChoiceField(label=_(u'审核'), required=True, widget=forms.RadioSelect(attrs={'v':'refrigeration', 'class':'refrigeration'}), choices=[(1, u'审核通过'), (-1, u'审核失败'), (0, u'审核中')])
	refrigeration_day1  = forms.DateField(label=_(u'有效期起始'), required=False, widget=forms.DateInput(attrs={'class':'refrigeration1'}))
	refrigeration_day2  = forms.DateField(label=_(u'有效期结束'), required=False, widget=forms.DateInput(attrs={'class':'refrigeration1'}))
	refrigeration_msg   = forms.CharField(label=_(u'原因'), required=False, widget=forms.Textarea(attrs={'cols':42, 'rows':3, 'class':'refrigeration0'}))




















