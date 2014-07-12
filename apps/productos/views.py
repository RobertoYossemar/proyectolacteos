#encoding:utf-8
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.productos.models import *
from apps.usuarios.forms import *
from django.shortcuts import  get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import StringIO

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

def lista_productos2(request):
    productos = Producto.objects.filter(Estado = True)
    stock = Stock.objects.all()
    categoria = Categoria.objects.all()
    return render_to_response('producto/lista_producto2.html', {'lista': productos,'listastock':stock,'listacategoria':categoria}, context_instance=RequestContext(request))
def lista_productos(request,id_cat):
    productos = Producto.objects.filter(RegistroCateg__id=id_cat,Estado=True)
    stock=Stock.objects.all()
    return render_to_response('producto/lista_producto.html',{'lista':productos,'listastock':stock},context_instance=RequestContext(request))
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
                return HttpResponseRedirect('/categorias/')
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
                return HttpResponseRedirect('/categorias/')
        else:
            formulario = ProductoForm(instance=productos)
            formulariostock = FormStock(instance=stocks)
        return render_to_response('producto/modifica_produc.html', {'formulario': formulario,'formulariostock':formulariostock},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
@permission_required('principal.change_categoria',login_url='/categorias/')
def Modificar_categoria(request, id_cat):
    if request.user.is_authenticated():
        categoria = get_object_or_404(Categoria, id=id_cat)
        if request.method == 'POST':
            formulario = FormCategoria(request.POST, request.FILES, instance=categoria)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect('/categorias/')
        else:
            formulario = FormCategoria(instance=categoria)

        return render_to_response('producto/modificar_categoria.html', {'formulario': formulario},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/modi')
def portal(request):
    formulario=fbuscar()
    return render_to_response("producto/portal.html",{'fbuscar':formulario},context_instance=RequestContext(request))



def buscar(request):
    if request.method=="POST":
        """Aqui ira otra busqueda igual que abajo"""
        return HttpResponse("hecho")
    else:
        texto=request.GET["texto"]
        busqueda=(
            Q(NombreProduc__icontains=texto) |
            #Q(descripcion__icontains=texto) |
            Q(Precio__icontains=texto)
        )
        resultados=Producto.objects.filter(busqueda).distinct()
        html="<ul class='ul_lista'>"
        for i in resultados:
            html=html+"<li><a href='/productos/"+str(i.id)+"/'>"+i.NombreProduc+"</a></li>"
        html=html+"<ul>"
        return HttpResponse(html)

def Lista_Noticias(request):
    noticias=Noticias.objects.all()
    return render_to_response('noticias.html', {'lista': noticias},context_instance=RequestContext(request))
def nueva_noticia(request):
    if request.method == 'POST':
        formulario = NoticiaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/Noticias')
    else:
        formulario = NoticiaForm()
    return render_to_response('nueva_noticia.html', {'formulario': formulario}, context_instance=RequestContext(request))
@permission_required('principal.change_receta',login_url='/Recetas/')
def Modificar_receta(request, id_cat):
    if request.user.is_authenticated():
        receta = get_object_or_404(Recetas, id=id_cat)
        if request.method == 'POST':
            formulario = RecetasForm(request.POST, request.FILES, instance=receta)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect('/Recetas/')
        else:
            formulario = RecetasForm(instance=receta)

        return render_to_response('producto/mod_receta.html', {'formulario': formulario},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/modreceta/')

def Lista_Recetas(request):
    recetas=Recetas.objects.all()
    return render_to_response('recetas.html', {'lista': recetas},context_instance=RequestContext(request))
def nueva_receta(request):
    if request.method == 'POST':
        formulario = RecetasForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/Recetas')
    else:
        formulario = RecetasForm()
    return render_to_response('nueva_receta.html', {'formulario': formulario}, context_instance=RequestContext(request))
"""
def reportes(request):
    productos=Producto.objects.all()
    pdf=create_pdf(productos,"plantilla.prep")
    pdb.set_trace()
    folderPdf=os.path.join(ruta,"static\\reportes\\productos.pdf")
    open(folderPdf,'w+').write(pdf)
    return HttpResponseRedirect("/static/reportes/productos.pdf")
def create_pdf(catalog, template):
    DATA_DIR=os.path.join(ruta,"static\\data")
    RML_DIR = os.path.join(ruta,"static\\rml")
    templateName = os.path.join(RML_DIR, template)
    template = preppy.getModule(templateName)
    namespace = {
        'productos':catalog,
        'RML_DIR': RML_DIR
    }
    rml = template.getOutput(namespace)
    open(os.path.join(DATA_DIR,'latest.rml'), 'w+').write(rml)
    buf = StringIO.StringIO()
    rml2pdf.go(rml, outputFileName=buf)
    return buf.getvalue()"""

def crear_reporte(request):
    productos = Producto.objects.all()
    stock = Stock.objects.all()
    html = render_to_string("reporte.html", {'pagesize': 'A4', 'productos': productos, 'stock': stock},
                            context_instance=RequestContext(request))
    return generar_pdf(html)


def reporteventa(request):
    ventas = Pedido.objects.all()
    usuarios = Perfil_user.objects.all()
    html = render_to_string("reporvetans.html", {'pagesize': 'A4', 'ventas': ventas, 'usuarios': usuarios},
                            context_instance=RequestContext(request))
    return generar_pdf(html)

def reporteUsusarios(request):
    cliente=Perfil_user.objects.all()
    html=render_to_string("ventas/usuarios.html",{'pagesize': 'A4','cliente':cliente,},
                          context_instance=RequestContext(request))
    return generar_pdf(html)
def reporteFiltro(request):
    if request.method == "POST":
        tipo = request.POST["sopcion"]
        if tipo == "1":
            f = request.POST["tfecha"]

            #return HttpResponse(f)
            busqueda = (
                Q(fecha__icontains=f))
            usuarios = Perfil_user.objects.all()
            ventas = Pedido.objects.filter(busqueda)
            #print  ventas
            #return HttpResponse(ventas.count)
            html = render_to_string("repor_por_fecha.html", {'pagesize': 'A4', 'ventas': ventas, 'usuarios': usuarios},
                                    context_instance=RequestContext(request))
            return generar_pdf(html)
        if tipo == "2":
            productos = Producto.objects.all()
            stock = Stock.objects.all()
            html = render_to_string("reporte.html", {'pagesize': 'A4', 'productos': productos, 'stock': stock},
                            context_instance=RequestContext(request))
            return generar_pdf(html)
        if tipo == "3":
            usuarios = Perfil_user.objects.all()
            ventas = Pedido.objects.all()
            html = render_to_string("repor_por_fecha.html", {'pagesize': 'A4', 'ventas': ventas, 'usuarios': usuarios},
                                    context_instance=RequestContext(request))
            return generar_pdf(html)
    else:
        return HttpResponseRedirect("/entrar/")


def generar_pdf(html):
    resultado = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")), resultado)
    if not pdf.err:
        return HttpResponse(resultado.getvalue(), mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")


def reportesgral(request):
    if request.user.is_authenticated():
        return render_to_response('reportesgral.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')