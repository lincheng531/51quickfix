from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.website',
    ('^$', 'views.index'),
    ('intro', 'views.intro'),
)