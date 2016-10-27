#!/user/bin/env python
#encoding:utf-8

import os
from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     
    ('^upload/$','apps.api.uploader.upload'),

    ('^account/loc$','apps.api.account.loc'),
    ('^account/download$','apps.api.account.download'),
    ('^account/feedback$','apps.api.account.feedback'),
    ('^account/remove$','apps.api.account.remove'),
    ('^account/rember$','apps.api.account.rember'),
    ('^account/signin$','apps.api.account.signin'),
    ('^account/update_profile$','apps.api.account.update_profile'),
    ('^account/active$','apps.api.account.active'),
    ('^account/resend_code$','apps.api.account.resend_code'),
    ('^account/signup$','apps.api.account.signup'),
    ('^account/signout$','apps.api.account.signout'),
    ('^account/forget$','apps.api.account.forget'),
    ('^account/reset_pwd$','apps.api.account.reset_pwd'),
    ('^account/is_authenticated$','apps.api.account.is_authenticated'),
    ('^account/verify_profile$','apps.api.account.verify_profile'),
    ('^account/upload_img','apps.api.account.upload_img'),
    ('^account/validate/(?P<mobile>\S{11})','apps.api.account.validate'),
    ('^account/verify_mobile/(?P<mobile>\S{11})/(?P<code>\S{4})$','apps.api.account.verify_mobile'),
    ('^account/profile/(?P<uid>\S{24})$','apps.api.account.profile'),
    
    ('^account/send_mobile/(?P<mobile>\S{11})/(?P<code>\S{4})$','apps.api.account.send_mobile'), 
    ('^account/verify_mobile/(?P<mobile>\S{11})/(?P<code>\S{4})$','apps.api.account.verify_mobile'), 
    ('^account/mregister$','apps.api.account.mregister'),
    ('^account/sregister$','apps.api.account.sregister'),

    ('^account/send_code/(?P<code>\S{4})$','apps.api.account.send_code'),
    ('^account/verify_code$','apps.api.account.verify_code'),
    
    ('^article/list$','apps.api.article.list'),
    ('^article/detail/(?P<aid>\S{24})$','apps.api.article.detail'),
    
    ('^basics/region$','apps.api.basics.region'),
    ('^basics/store$','apps.api.basics.store'),
    ('^basics/brand$','apps.api.basics.brand'),
    ('^basics/product$','apps.api.basics.product'),
    ('^basics/equipment$','apps.api.basics.equipment'),
    ('^basics/history/(?P<oid>\S{24})$','apps.api.basics.history'),
    ('^basics/device/(?P<id>\S{24})$','apps.api.basics.device_detail'),

    ('^service/scan$','apps.api.service.scan'),
    ('^service/later/(?P<oid>\S{24})$','apps.api.service.later'),
    ('^service/delayed/(?P<oid>\S{24})$','apps.api.service.delayed'),
    
    ('^service/grabs$','apps.api.service.grabs'),
    ('^service/grab/(?P<oid>\S{24})$','apps.api.service.grab'),
    ('^service/repairs$','apps.api.service.repairs'),
    ('^service/repair/(?P<oid>\S{24})$','apps.api.service.repair'),
    ('^service/collection/(?P<id>\S{24})$','apps.api.service.collection'),
    ('^service/bill/(?P<oid>\S{24})$','apps.api.service.bill'),
    #标准版提交工单
    ('^service/bill1/(?P<oid>\S{24})$','apps.api.service.bill1'),
    ('^service/bill2/(?P<oid>\S{24})$','apps.api.service.bill2'),
    ('^service/bill3/(?P<oid>\S{24})$','apps.api.service.bill3'),
    ('^service/review/(?P<oid>\S{24})$','apps.api.service.review'),
    ('^service/later$','apps.api.service.later'),
    ('^service/stop/(?P<oid>\S{24})$','apps.api.service.stop'),
    ('^service/close/(?P<oid>\S{24})$','apps.api.service.close'),
    ('^service/delete_bill/(?P<oid>\S{24})$','apps.api.service.delete_bill'),
    
    ('^merchant/errors$','apps.api.merchant.errors'),
    ('^merchant/spares$','apps.api.merchant.spares'),
    ('^merchant/suppliers$','apps.api.merchant.suppliers'),
    ('^merchant/products$','apps.api.merchant.products'),
    ('^merchant/call$','apps.api.merchant.call'),
    ('^merchant/call_repeat/(?P<oid>\S{24})$','apps.api.merchant.call_repeat'),
    ('^merchant/call_quit/(?P<oid>\S{24})$','apps.api.merchant.call_quit'),

    ('^merchant/update_restaurant/(?P<oid>\S+)$','apps.api.merchant.update_restaurant'),
    ('^merchant/update_assets/(?P<oid>\S{24})$','apps.api.merchant.update_assets'),
    ('^merchant/update_qrcode/(?P<rid>\S+)$','apps.api.merchant.update_qrcode'),
    ('^merchant/update_device/(?P<oid>\S{24})$','apps.api.merchant.update_device'),
    ('^merchant/delete_device/(?P<rid>\S{24})$','apps.api.merchant.delete_device'),

    ('^merchant/maintenances$','apps.api.merchant.maintenances'),
    ('^merchant/maintenance/(?P<oid>\S{24})$','apps.api.merchant.maintenance'),
    ('^merchant/collection/(?P<id>\S{24})$','apps.api.merchant.collection'),
    ('^merchant/maintenance_confirm/(?P<oid>\S{24})/(?P<cid>\S{24})$','apps.api.merchant.maintenance_confirm'),
    ('^merchant/confirm/(?P<oid>\S{24})$','apps.api.merchant.confirm'),
    ('^merchant/review/(?P<oid>\S{24})$','apps.api.merchant.review'),
    ('^merchant/fault$','apps.api.merchant.fault'),
    ('^merchant/scan$','apps.api.merchant.scan'),
    ('^merchant/call_history/(?P<oid>\S{24})$','apps.api.merchant.call_history'),
    ('^merchant/add_bill/(?P<oid>\S{24})$','apps.api.merchant.add_bill'),
    ('^merchant/confirm_bill/(?P<oid>\S{24})$','apps.api.merchant.confirm_bill'),
    ('^merchant/delete_bill/(?P<oid>\S{24})$','apps.api.merchant.delete_bill'),
    ('^merchant/reset_fixed/(?P<oid>\S{24})$','apps.api.merchant.reset_fixed'),
    ('^merchant/collect/(?P<id>\S{24})$','apps.api.merchant.collect'),

    ('^provider/online$','apps.api.provider.online'),
    ('^provider/opinion/(?P<oid>\S{24})$','apps.api.provider.opinion'),
    ('^provider/repairs$','apps.api.provider.repairs'),
    ('^provider/repair/(?P<oid>\S{24})$','apps.api.provider.repair'),
    ('^provider/collection/(?P<id>\S{24})$','apps.api.provider.collection'),
    ('^provider/dispatch/(?P<oid>\S{24})$','apps.api.provider.dispatch'),

    ('^task/list$','apps.api.task.list'),
    ('^task/check/(?P<oid>\S{24})$','apps.api.task.check'),
    ('^task/inventory/(?P<oid>\S{24})$','apps.api.task.inventory'),
    ('^task/scan/(?P<oid>\S{24})$','apps.api.task.scan'),


)


