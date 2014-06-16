from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.usuarios.forms import Perform,perfil_userForm,LoginForm,ContactanosF
from django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth import login,authenticate,logout
from django.core.mail import EmailMultiAlternatives

def iniciopag(request):
    return render_to_response('index.html', context_instance=RequestContext(request))
#inscripcion de un nuevo usuario
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
#recepcion de contactos
def Recepcion_contactos(request):
    info_enviado = False
    email = ""
    titulo = ""
    texto = ""
    if request.method == "POST":
        formulario = ContactanosF(request.POST)
        if formulario.is_valid():
            info_enviado = True
            email = formulario.cleaned_data['Email']
            titulo = formulario.cleaned_data['Titulo']
            texto = formulario.cleaned_data['Texto']
            to_admin = 'ocamporoberto97@gmail.com'
            html_content = "Informacion recibida de [%s]<br><br><br>***Mensaje***<br><br>%s" % (email, texto)
            msg = EmailMultiAlternatives('Correo de Contacto', html_content, 'from@server.com', [to_admin])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    else:
        formulario = ContactanosF()
    ctx = {'form': formulario, "email": email, "titulo": titulo, "texto": texto, "info_enviado": info_enviado}
    return render_to_response('usuario/contactar.html', ctx, context_instance=RequestContext(request))