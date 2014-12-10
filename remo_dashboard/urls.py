from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'remo_dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^events', 'dashboard.views.events', name='events'),
    url(r'^metrics-challenge', 'dashboard.views.metrics_challenge', name='metrics-challenge'),
    url(r'^$', 'dashboard.views.home', name='home'),
)
