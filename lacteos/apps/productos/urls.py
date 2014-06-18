from django.conf.urls import patterns, url
from views import *
urlpatterns = patterns('',
    url(r'^categorias/$',lista_categorias, name='Categorias'),
    url(r'^categorias/nueva/$',nueva_categoria, name='Nuevacat'),
    url(r'^producto/$',lista_productos2, name='Productos'),
    url(r'^productos/(?P<id_cat>\d+)/$',lista_productos, name='Producto'),
    url(r'^productoselec/$',lista_categorias, name='Seleccionar categoria'),
    url(r'^producto/nuevo/$',Crear_Producto, name='Nuevo Producto'),
    url(r'^principal/update/(?P<id_prod>\d+)/$',Modificar_Producto,name='Modificar Producto'),
    url(r'^producto/buscar/$',Buscar_producto,name='Buscar Producto'),
    url(r'^Noticias/$',Lista_Noticias,name='Noticias'),
    url(r'^noticia/nueva/$',nueva_noticia,name='Noticias'),
    url(r'^reportes/$',reportes,name='reportes'),


)
