from apps.inicio.models import Perfil,Perfil_user
from apps.productos.models import Producto,Stock,Categoria
from django.contrib import admin
from django.contrib.auth.models import Permission
admin.site.register(Perfil)
admin.site.register(Perfil_user)
admin.site.register(Producto)
admin.site.register(Stock)
admin.site.register(Categoria)
admin.site.register(Permission)