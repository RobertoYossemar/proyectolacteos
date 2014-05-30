from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',

    #url(r'^$', 'apps.views.home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
    url(r'^$', 'apps.inicio.views.iniciopag'),
    #logueo
    url(r'^login/$','apps.usuarios.views.login_view',name='vista_login'),
    url(r'^logout/$','apps.usuarios.views.logout_view',name='vista_logout'),
    #usuarios
    url(r'^usuario/nueva/$', 'apps.usuarios.views.nueva_inscripcion'),
    #url(r'^productos/', include('apps.productos.urls')),
    #url(r'^auth/', include('ajax.apps.autenticacion.urls')),
    #productos
    url(r'^$','apps.productos.views.lista_categorias'),
    url(r'^$','apps.productos.views.lista_productos'),
    url(r'^categorias/$','apps.productos.views.lista_categorias'),
    url(r'^categoria/nueva/$','apps.productos.views.nueva_categoria'),
    url(r'^productos/$','apps.productos.views.lista_productos'),
    #url(r'^productos/(?P<id_cat>\d+)/$','apps.productos.views.lista_productos'),
    url(r'^productoselec/$','apps.productos.views.lista_categorias'),
    url(r'^producto/nuevo/$','apps.productos.views.Crear_Producto'),
    url(r'^principal/update/(?P<id_prod>\d+)/$', 'apps.productos.views.Modificar_Producto'),

)
