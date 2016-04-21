from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import Login, PDVSALogout
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
                       url(r'^$', RedirectView.as_view(url=reverse_lazy('login'))),
                       url(r'^Login/$', Login.as_view(), name='login'),
                       url(r'^logout/$', PDVSALogout, name='logout'),
                       url(r'^control/', include('control.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
