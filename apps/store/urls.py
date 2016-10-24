import os
from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.store',
    ('^$','overview.index'),
    ('assets/list$','assets.list'),
    ('assets/append/(?P<oid>\S{24})$','assets.append'),
    ('assets/edit/(?P<oid>\S{24})$','assets.edit'),
    ('assets/detail/(?P<oid>\S{24})$','assets.detail'),
    ('assets/store/(?P<oid>\S{24})$','assets.store'),
    ('assets/store/append$','assets.store_append'),
    ('assets/store/edit/(?P<oid>\S{24})$','assets.store_edit'),
    ('assets/store/close/(?P<oid>\S{24})$','assets.store_close'),
    ('assets/inventory$','assets.inventory'),
    ('assets/region$','assets.region'),
    ('assets/qrcode$','assets.qrcode'),
    ('assets/dump$','assets.dump'),

    ('repair/list$','repair.list'),
    ('repair/dump$','repair.dump'),
    ('repair/detail/(?P<oid>\S{24})$','repair.detail'),
   
    
    ('inventory/list$','inventory.list'),
    ('inventory/append$','inventory.append'),
    ('inventory/dump$','inventory.dump'),
    ('inventory/store$','inventory.store'),
    ('inventory/detail/(?P<oid>\S{24})$','inventory.detail'),
    ('inventory/notify/(?P<hid>\S{24})/(?P<oid>\S{24})$','inventory.notify'),
    ('inventory/detail2/(?P<hid>\S{24})/(?P<oid>\S{24})$','inventory.detail2'),

    ('account/list$','account.list'),
    ('account/profile$','account.profile'),
    ('account/append/(\d+)$','account.append'),
    ('account/detail/(?P<oid>\S{24})$','account.detail'),
    ('account/edit/(?P<oid>\S{24})$','account.edit'),
    ('account/active/(?P<oid>\S{24})/(?P<category>\S{1})$','account.active'),

    ('role/list$','role.list'),
    ('role/detail$','role.detail'),
    ('role/edit$','role.edit'),

    ('brand/list$','brand.list'),
    ('brand/append$','brand.append'),
    ('brand/detail/(?P<oid>\S{24})$','brand.detail'),

    ('supplier/list$','supplier.list'),
    ('supplier/append$','supplier.append'),
    ('supplier/detail/(?P<oid>\S{24})$','supplier.detail'),

    ('product/list$','product.list'),
    ('product/append$','product.append'),
    ('product/detail/(?P<oid>\S{24})$','product.detail'),
    ('product/edit/(?P<oid>\S{24})$','product.edit'),
    ('product/spare/detail/(?P<cid>\S{24})/(?P<oid>\S{24})$','product.spare_detail'),

    ('call/list$','call.list'),
    ('call/append$','call.append'),
    ('call/detail/(?P<oid>\S{24})$','call.detail'),


)

