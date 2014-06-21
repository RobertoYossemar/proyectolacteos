from django.forms import ModelForm
from django import forms
from apps.usuarios.models import Perfil,Perfil_user
from apps.productos.models import Producto,Stock,Categoria,Noticias,Recetas
from django.forms import Textarea
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
#Recepcion de correos electronicos a uncorreo externo
class ContactanosF(forms.Form):
    Email=forms.EmailField(widget=forms.TextInput())
    Titulo=forms.CharField(widget=forms.TextInput())
    Texto=forms.CharField(widget=forms.Textarea())
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
class BuscarProd(forms.Form):
    buscar=forms.CharField()

class NoticiaForm(ModelForm):
    class Meta:
        model=Noticias
        widgets = {
            'content': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
class RecetasForm(ModelForm):
    class Meta:
        model=Recetas
        widgets = {
            'content': Textarea(attrs={'cols': 80, 'rows': 20}),
        }