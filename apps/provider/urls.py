import os
from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.provider',
    ('repair/list$','repair.list'),
    ('repair/dump$','repair.dump'),
    ('repair/detail/(?P<oid>\S{24})$','repair.detail'),
    ('repair/edit/(?P<oid>\S{24})$','repair.edit'),
    ('repair/spare/(?P<oid>\S{24})$','repair.spare'),

    ('verify/list$','verify.list'),
    ('verify/close$','verify.close'),
    
    ('account/list$','account.list'),
    ('account/profile$','account.profile'),
    ('account/append/(\d+)$','account.append'),
    ('account/detail/(?P<oid>\S{24})$','account.detail'),
    ('account/edit/(?P<oid>\S{24})$','account.edit'),
    ('account/active/(?P<oid>\S{24})/(?P<category>\S{1})$','account.active'),

)

