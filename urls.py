import os
from django.conf.urls import patterns, include, url
import settings

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$',  'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),

    (r'^admin/', include('apps.admin.urls')),
    #(r'^merchant/', include('apps.merchant.urls')),

    (r'^store/', include('apps.store.urls')),
    (r'^provider/', include('apps.provider.urls')),
    (r'^api/v1/', include('apps.api.urls_v1')),
    (r'^home/', include('apps.website.urls')),
    (r'^', include('apps.website.urls')),
)
