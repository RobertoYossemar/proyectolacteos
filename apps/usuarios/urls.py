#encoding:utf-8
from django.conf.urls import patterns, url
from views import *
urlpatterns = patterns('',
    url(r'^usuario/$',nueva_inscripcion, name='inscripcion'),
    url(r'^entrar/$',login_view, name='Entrar'),
    url(r'^salir/$',logout_view, name='Salir'),
    url(r'^contactar/$',Recepcion_contactos, name='Contacto'),

)