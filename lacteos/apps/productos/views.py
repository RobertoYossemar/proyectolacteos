from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.productos.models import Producto,Categoria,Stock
from apps.inicio.forms import FormCategoria,FormStock,ProductoForm
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
@permission_required('principal.add_categoria',login_url='/categorias')
def nueva_categoria(request):#esta funcion devuelve el formulario creado en form.py
    if request.method == 'POST':
        formulario = FormCategoria(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/categorias')# nos nmanda al index
    else:
        formulario = FormCategoria()
    return render_to_response('producto/nueva_categoria.html', {'formulario': formulario}, context_instance=RequestContext(request))
def nuevo_stock(request):
    if request.method == 'POST':
        formulario = FormStock(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/stock')# nos nmanda al index
    else:
        formulario = FormStock()
    return render_to_response('producto/nuevo_produc.html', {'formulario': formulario}, context_instance=RequestContext(request))

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render_to_response('producto/lista_categorias.html', {'lista': categorias}, context_instance=RequestContext(request))
#@permission_required('principal.add_categoria',login_url='/')

def lista_productos(request):
    productos = Producto.objects.filter(Estado = True)
    stock = Stock.objects.all()
    categoria = Categoria.objects.all()
    return render_to_response('producto/lista_producto.html', {'lista': productos,'listastock':stock,'listacategoria':categoria}, context_instance=RequestContext(request))
#def lista_productos(request,id_cat):
 #   productos = Producto.objects.filter(RegistroCateg__id=id_cat,Estado=True)
  #  stock=Stock.objects.all()
   # return render_to_response('producto/lista_producto.html',{'lista':productos,'listastock':stock},context_instance=RequestContext(request))
def lista_stock(request):
    stocks = Stock.objects.all()
    return render_to_response('producto/lista_producto.html', {'lista': stocks})
@permission_required('principal.add_producto',login_url='/productos')
def Crear_Producto(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            formularioproducto = ProductoForm(request.POST, request.FILES)
            formulariostock = FormStock(request.POST)
            if formularioproducto.is_valid() and formulariostock.is_valid():
                pro = formularioproducto.save()
                stock = formulariostock.save()
                stock.reg_pro=pro
                stock.save()
                return HttpResponseRedirect('/productos/')
        else:
            formularioproducto = ProductoForm()
            formulariostock = FormStock()
        return render_to_response('producto/nuevo_produc.html', {'formularioproducto':formularioproducto, 'formulariostock':formulariostock}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
@permission_required('principal.change_producto',login_url='/productos')
def Modificar_Producto(request, id_prod):
    if request.user.is_authenticated():
        stocks = get_object_or_404(Stock,pk = id_prod)
        productos = get_object_or_404(Producto, pk=id_prod)
        if request.method == 'POST':
            formulario = ProductoForm(request.POST, request.FILES, instance=productos)
            formulariostock = FormStock(request.POST,request.FILES,instance=stocks)
            if formulario.is_valid()and formulariostock.is_valid():
                formulario.save()
                formulariostock.save()
                return HttpResponseRedirect('/productos/')
        else:
            formulario = ProductoForm(instance=productos)
            formulariostock = FormStock()
        return render_to_response('producto/modifica_produc.html', {'formulario': formulario,'formulariostock':formulariostock},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
