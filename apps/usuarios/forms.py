#encoding:utf-8
from django.forms import ModelForm
from django import forms
from apps.usuarios.models import *
from apps.productos.models import *
from apps.venta.models import *
from django.forms import Textarea

class perfil_userForm(ModelForm):
    class Meta:
        model = Perfil_user
        exclude = ['user', 'per_user']

#logueo de usuarios
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    passsword = forms.CharField(widget=forms.PasswordInput(render_value=False))

#Recepcion de correos electronicos a uncorreo externo
class ContactanosF(forms.Form):
    Email = forms.EmailField(widget=forms.TextInput())
    Titulo = forms.CharField(widget=forms.TextInput())
    Texto = forms.CharField(widget=forms.Textarea())

#productos
class FormStock(ModelForm):
    class Meta:
        model = Stock
        exclude = ['reg_pro']


class FormCategoria(ModelForm):
    class Meta:
        model = Categoria


class ProductoForm(ModelForm):
    class Meta:
        model = Producto


class fbuscar(forms.Form):
    texto = forms.CharField(max_length=50, label="Buscar productos")


class fpedido(ModelForm):
    class Meta:
        model = Pedido
        exclude = ['cliente','producto','cantidad','precio_total']

class FacturaForm(ModelForm):
    class Meta:
        model = factura

class fcarrito(ModelForm):
    class Meta:
        model = Carrito
        exclude = ['producto', 'id_sesion', 'estado']


class NoticiaForm(ModelForm):
    class Meta:
        model = Noticias


class RecetasForm(ModelForm):
    class Meta:
        model = Recetas
        widgets = {
            'content': Textarea(attrs={'cols': 80, 'rows': 20}),
        }