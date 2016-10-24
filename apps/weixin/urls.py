import os
from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('apps.weixin',
    ('^$','index.index'),
    ('entry$','index.entry'),
    ('shop/(?P<category>\S{2})$','index.shop'),
    ('about$','index.about'),
    ('link$','index.link'),
    ('brand$','index.brand'),
    ('project$','index.project'),
)

