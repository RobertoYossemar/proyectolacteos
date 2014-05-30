from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.inicio.forms import Perform,perfil_userForm,LoginForm
from django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
def nueva_inscripcion(request):
    if request.method =='POST':
        formulario = UserCreationForm(request.POST)
        formularioUsuario=Perform(request.POST,request.FILES)
        formPerfil = perfil_userForm(request.POST,request.FILES)
        if formulario.is_valid()and formularioUsuario.is_valid() and formPerfil.is_valid():
            u =formulario.save()
            persona = formularioUsuario.save()
            perfil = formPerfil.save()
            perfil.user = u
            perfil.per_user = persona
            perfil.save()
        return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
        formPerfil =perfil_userForm()
        formularioUsuario=Perform()
    return  render_to_response('usuario/reg_usuario.html',{'formulario':formulario,'formPerfil':formPerfil,'formularioUsuario':formularioUsuario},context_instance=RequestContext(request))
#logueo
def login_view(request):
    mensaje = "Introduzca su Nombre y Password Correctamente"
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            form =LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['passsword']

                usuario = authenticate(username=username,password=password)
                if usuario is not None and usuario.is_active:
                    login(request,usuario)
                    return HttpResponseRedirect('/')
                else:
                    mensaje = "usuario y/o password incorrecto"
        form = LoginForm()
        ctx ={'form':form,'mensaje':mensaje}
        return render_to_response('usuario/login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')