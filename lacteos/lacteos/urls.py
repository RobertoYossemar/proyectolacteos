from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', 'apps.usuarios.views.iniciopag', name='inicio'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
    url(r'^',include("apps.usuarios.urls")),
    url(r'^',include("apps.productos.urls")),
)
