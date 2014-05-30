from apps.inicio.models import Perfil,Perfil_user
from apps.inicio.forms import Perform,perfil_userForm
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
def iniciopag(request):
    return render_to_response('index.html', context_instance=RequestContext(request))
