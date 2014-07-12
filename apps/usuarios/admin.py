#encoding:utf-8
from apps.usuarios.models import *
from apps.productos.models import *
from django.contrib import admin
from django.contrib.auth.models import Permission
admin.site.register(Perfil_user)
admin.site.register(Permission)
admin.site.register(Producto)
admin.site.register(Stock)
admin.site.register(Categoria)