#encoding:utf-8
from django.conf.urls import patterns, url
from views import *
urlpatterns = patterns('',
    url(r'^productos/mostrar/carrito/$',carrito_mostrar),
    url(r'^productos/cargar/carrito/(\d+)/$',cargar_carrito),
    url(r'^productos/carrito/add/(\d+)/$',carrito_add),
    url(r'^carrito/eliminar/(?P<id>\d+)/$',eliminar_de_carrito),
    url(r'^confirmar/compra/$',confirmar_compra),
    url(r'^producto/comprar/final/$',realizar_transaccion),
    url(r'^producto/Pendiente/$',Vpedido),
    url(r'^producto/modipend/(?P<id_ped>\d+)/$',modVpedido),
   # url(r'^factura/(?P<id>\d+)/$',FACTURA),
    url(r'^codigo/(?P<id>\d+)/$',genfactura),
)