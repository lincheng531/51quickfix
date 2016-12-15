import os
from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.admin',
    ('^$','overview.index'),
    ('overview$','overview.overview'),
    ('detail$','overview.detail'),
    (r'^login$','index.login'),
    ('logout$','index.logout'),
    
    ('upload$','uploader.upload'),

    ('store/list/(?P<category>\S{1})$','store.list'),
    ('store/detail/(?P<oid>\S{24})$','store.detail'),
    ('store/active/(?P<oid>\S{24})/(?P<category>(\d+))/$','store.active'),
    
    ('account/list/(?P<category>\S{1})/(?P<status>\S{1})$','account.list'),
    ('account/detail/(?P<oid>\S{24})$','account.detail'),
    ('account/active/(?P<oid>\S{24})/(?P<category>\S{1})$','account.active'),
    ('account/profile$','account.profile'),
    
    #('product/list$','product.list'),
    #('product/detail/(?P<oid>\S{24})$','product.detail'),
    #('product/edit/(?P<oid>\S{24})$','product.edit'),
    #('product/append$','product.append'),
    #('product/delete/(?P<oid>\S{24})$','product.delete'),

    #('repair/list$','repair.list'),
    #('repair/detail/(?P<oid>\S{24})$','repair.detail'),
    #('repair/edit/(?P<oid>\S{24})$','repair.edit'),
    #('repair/append$','repair.append'),
    #('repair/delete/(?P<oid>\S{24})$','repair.delete'),

    #('bill/list$','bill.list'),
    #('bill/detail/(?P<oid>\S{24})$','bill.detail'),
    #('bill/edit/(?P<oid>\S{24})$','bill.edit'),
    #('bill/append$','bill.append'),
    #('bill/delete/(?P<oid>\S{24})$','bill.delete'),

    #('errors/list$','errors.list'),
    #('errors/detail/(?P<oid>\S{24})$','errors.detail'),
    #('errors/edit/(?P<oid>\S{24})$','errors.edit'),
    #('errors/append$','errors.append'),
    #('errors/delete/(?P<oid>\S{24})$','errors.delete'),

    #('spare/list$','spare.list'),
    #('spare/detail/(?P<oid>\S{24})$','spare.detail'),
    #('spare/edit/(?P<oid>\S{24})$','spare.edit'),
    #('spare/append$','spare.append'),
    #('spare/delete/(?P<oid>\S{24})$','spare.delete'),

    #('supplier/list$','supplier.list'),
    #('supplier/detail/(?P<oid>\S{24})$','supplier.detail'),
    #('supplier/edit/(?P<oid>\S{24})$','supplier.edit'),
    #('supplier/append$','supplier.append'),
    #('supplier/delete/(?P<oid>\S{24})$','supplier.delete'),

    #('push/list$','push.list'),
    #('push/detail/(?P<oid>\S{24})$','push.detail'),
    #('push/edit/(?P<oid>\S{24})$','push.edit'),
    #('push/append$','push.append'),
    #('push/delete/(?P<oid>\S{24})$','push.delete'),

    #('account/list$','account.list'),
    #('account/detail/(?P<oid>\S{24})$','account.detail'),
    #('account/edit/(?P<oid>\S{24})$','account.edit'),
    #('account/append$','account.append'),
    #('account/append1$','account.append1'),
    #('account/delete/(?P<oid>\S{24})$','account.delete'),
    #('account/profile$','account.profile'),
    


    ('maintenance/detail/(?P<oid>\S{24})$','maintenance.detail'),
    #('maintenance/edit/(?P<oid>\S{24})$','maintenance.edit'),
    #('maintenance/append$','maintenance.append'),
    #('maintenance/delete/(?P<oid>\S{24})$','maintenance.delete'),

    #('bconfig/list$','bconfig.list'),
    #('bconfig/detail/(?P<oid>\S{24})$','bconfig.detail'),
    #('bconfig/edit/(?P<oid>\S{24})$','bconfig.edit'),
    #('bconfig/append$','bconfig.append'),
    #('bconfig/delete/(?P<oid>\S{24})$','bconfig.delete'),

    url(r'api/v1/test', 'api.test'),
    url(r'api/v1/login$', 'api.login'),
    url(r'api/v1/maintenance/list$', 'api.maintenanceList'),
    url(r'api/v1/maintenance/(?P<id>\S{24})$','api.maintenanceDetail'),
    url(r'api/v1/maintenance/(?P<id>\S{24})/audit/repair$','api.audit_repair'),
    url(r'api/v1/maintenance/(?P<id>\S{24})/audit/merchant$','api.audit_merchant'),
    url(r'api/v1/maintenance/(?P<id>\S{24})/settlement$','api.settlement_clear'),
    url(r'api/v1/store$','api.store'),
    url(r'api/v1/user$','api.user'),
    url(r'api/v1/repairs$','api.repairs'),
    url(r'api/v1/categories','api.categoryList'),
    url(r'api/v1/maintenance/call','api.call'),

)