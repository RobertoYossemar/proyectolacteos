#encoding:utf-8
from django.db import models
from apps.productos.models import *
from apps.usuarios.models import *
from django.contrib.auth.models import User

class Pedido(models.Model):
    cliente=models.ForeignKey(User)
    producto=models.ManyToManyField(Producto)
    cantidad=models.IntegerField()
    precio_total=models.FloatField()
    fecha=models.DateTimeField(auto_now_add=True)
    Estado=models.BooleanField(default=True)
    def __unicode__(self):
        return self.producto


class Carrito(models.Model):
    id_sesion=models.CharField(max_length=200)
    estado=models.BooleanField ( default = False )
    producto=models.ForeignKey(Producto)
    cantidad=models.IntegerField()


class factura(models.Model):
    N_Autorizacion=models.CharField(max_length=15,verbose_name="N_autorizacion")
    llave=models.CharField(max_length=20,verbose_name="llave")
    Dato=models.ForeignKey(Pedido)
    def __unicode__(self):
        return self.N_Autorizacion



