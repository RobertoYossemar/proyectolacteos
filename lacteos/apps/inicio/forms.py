#encobing:utf-8
from django.forms import ModelForm
from django import forms
from apps.inicio.models import Perfil,Perfil_user
from apps.productos.models import Producto,Stock,Categoria
class Perform(ModelForm):
    class Meta:
        model= Perfil
class perfil_userForm(ModelForm):
    class Meta:
        model= Perfil_user
        exclude=['user','per_user']
#logueo de usuarios
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    passsword = forms.CharField(widget=forms.PasswordInput(render_value=False))
#productos
class FormStock(ModelForm):
    class Meta:
        model=Stock
        exclude = ['reg_pro']

class FormCategoria(ModelForm):
    class Meta:
        model=Categoria
class ProductoForm(ModelForm):
    class Meta:
        model=Producto


