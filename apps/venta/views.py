#encoding:utf-8
from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from apps.productos.models import *
from apps.venta.models import *
from apps.usuarios.forms import *
import datetime
import math
import hashlib
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import StringIO

def carrito_mostrar(request):
    if not "contador" in request.session:
        request.session['contador'] = 0
    return HttpResponse(request.session['contador'])


def cargar_carrito(request,id):
    pro=Producto.objects.get(id=int(id))
    fcarr=fcarrito()
    return render_to_response("ventas/fcarrito.html",{'fcarr':fcarr,'pro':pro},context_instance=RequestContext(request))

def carrito_add(request,id):
    if request.method=="POST":
        cant=request.POST['cantidad']
        if int(cant)>0:
            if not "id_sesion" in request.session:
                request.session["id_sesion"]=hashlib.md5(str(datetime.datetime.now())).hexdigest()
            pro=Producto.objects.get(id=int(id))
            carr=Carrito.objects.create(id_sesion=request.session["id_sesion"],estado=False,producto=pro,cantidad=int(cant))
            contador=request.session['contador']
            request.session['contador']=contador+1
    return HttpResponse(request.session['contador'])

def confirmar_compra(request):
    if request.user.is_authenticated():
        id_sesion=request.session["id_sesion"]
        carr=Carrito.objects.filter(id_sesion=id_sesion)
        pre_total = 0
        cantidad = 0
        for i in carr:
            pre_total += float(i.producto.Precio * i.cantidad)
            cantidad += i.cantidad
        return render_to_response("ventas/confirmar_compra.html",{'carr':carr,'pre_total':pre_total},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/entrar/")

def eliminar_de_carrito(request,id):
    if "contador" in request.session:
        contador=request.session['contador']
        request.session['contador']=contador-1
        carr=Carrito.objects.get(id=int(id))
        carr.delete()
        return HttpResponseRedirect("/confirmar/compra/")
    else:
        return HttpResponseRedirect("/productos/")
def realizar_transaccion(request):
    if request.user.is_authenticated():
        usuario=request.user
        u=User.objects.get(username=usuario)
        """Aqui para realizar la transaccion solo lo agregaremos en nuestra tabla pedido"""
        id_sesion=request.session["id_sesion"]
        carr=Carrito.objects.filter(id_sesion=id_sesion)
        """RECORREMOS EL CARRITO EN UN FOR PARA REALIZAR LA TRANSACCION"""
        pre_total=0
        cantidad=0
        for i in carr:
            pre_total+=float(i.producto.Precio*i.cantidad)
            cantidad+=i.cantidad
        trans=Pedido.objects.create(cliente=u,cantidad=cantidad,precio_total=pre_total)
        for i in carr:
            #pre_total=float(i.producto.Precio*i.cantidad)
            """SELECCIONAMOS EL PRODUCTO PARA REDUCIR EL STOCK"""
            pro=Producto.objects.get(id=i.producto.id)
            sto=Stock.objects.get(reg_pro_id=i.producto.id)
            #trans=Pedido.objects.create(cliente=u,cantidad=i.cantidad,precio_total=pre_total)
            """NUESTRA CLASE TIENE UNA RELACION DE MUCHOS A MUCHOS ASI QUE LA AGREGAMOS DE ESTA FORMA"""
            trans.producto.add(pro)
            trans.save()
            #stock=pro.stock
            sto.cantidad=sto.cantidad-i.cantidad
            sto.save()
            pro.save()
        """Eliminamos el carrito"""
        carr.delete()
        request.session['contador']=0
        return HttpResponseRedirect("/codigo/"+ str(trans.id)+"/")
    else:
        return HttpResponseRedirect("/entrar/")

def Vpedido(request):
    ped = Pedido.objects.filter(Estado=True)
    cliente = Perfil_user.objects.all()
    mensaje = "Pedido Pendiente"
    return render_to_response('ventas/Pendientes.html', {'ped': ped, 'cliente': cliente, 'sms': mensaje},
                              context_instance=RequestContext(request))


def modVpedido(request, id_ped):
    if request.user.is_authenticated():
        ped = get_object_or_404(Pedido, pk=id_ped)
        if request.method == 'POST':
            forped = fpedido(request.POST, request.FILES, instance=ped)
            if forped.is_valid():
                forped.save()
                return HttpResponseRedirect('/producto/Pendiente/')
        else:
            forped = fpedido(instance=ped)
        return render_to_response('ventas/modificarped.html', {'formuped': forped},
                                  context_instance=RequestContext(request))
    else:
        HttpResponseRedirect('/')



def generar_pdf(html):
    resultado = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")), resultado)
    if not pdf.err:
        return HttpResponse(resultado.getvalue(), mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")

'''def FACTURA(request,id):
    if request.user.is_authenticated():
        perfil=Perfil.objects.filter(id=id)
        ventas=Pedido.objects.get(id=id)
        usuarios=Perfil_user.objects.get(user=request.user)
        html=render_to_string('ventas/factura.html',{'pagesize':'A8','perfil':perfil,'ventas':ventas,'usuarios':usuarios},context_instance=RequestContext(request))
        return generar_pdf(html)
    else:
        return HttpResponseRedirect('/')'''''

'''def geneFactura(request, id):
    if request.user.is_authenticated():
        #clienteNit=Perfil.objects.get(id=id)
        u=request.user
        #return HttpResponse(u)
        cliente = Perfil_user.objects.get(user=u)
        ci=Perfil.objects.get(ci=cliente.per_user)
        return HttpResponse(ci)
        pedido = Pedido.objects.get(id=id)
        #pedidos=Pedido.objects.filter(id=id)
        #productos2=Producto.objects.filter(id=id)
        productos=Producto.objects.get(id=id)
        autoriz='2901091557'
        nfactura=""+str(pedido.id)
        nnit=""+str(clienteNit.CI_NIT)
        strfecha=(str(pedido.fecha)[:10]).replace("-","")
        strmonto=str(int(math.ceil(pedido.precio_total/100)*100))
        strllave="!@#$%&/()=?P"
        codigo = calculo(autoriz, nfactura, nnit, strfecha, strmonto,strllave)
        #return HttpResponse(codigo)
        html= render_to_string('ventas/codigo.html', {
            'pagesize': 'A4',
            'clienteNit':clienteNit,
            'productos': productos,
            #'productos2': productos2,
            'cliente': cliente,
            'pedido': pedido,
            #'pedidos': pedidos,
            'codigo': codigo,
        }, context_instance=RequestContext(request))
        return generar_pdf(html)
    else:
        return HttpResponseRedirect("/")'''

def genfactura(request,id):
    venta=Pedido.objects.get(id=id)
    cliente=Perfil_user.objects.get(user=request.user)
    pedido=Pedido.objects.filter(id=id)
    carr=Carrito.objects.all()
    if request.user.is_authenticated():
        autoriz='2901091557'
        nfactura=""+str(venta.id)
        nnit=""+str(cliente.CI_NIT)
        strfecha=(str(venta.fecha)[:10]).replace("-","")
        strmonto=str(int(math.ceil(venta.precio_total/100)*100))
        strllave="!@#$%&/()=?P"
        codigo = calculo(autoriz, nfactura, nnit, strfecha, strmonto,strllave)
        html=render_to_string('ventas/factura.html',{'pagesize':'A8','venta':venta,'cliente':cliente,'pedido':pedido,'codigo':codigo,'carr':carr},context_instance=RequestContext(request))
        return generar_pdf(html)
    else:
        return HttpResponseRedirect('/')



def calculo(auto, factura, nit, fecha, monto, llave):
    auto += str(digito(auto))
    factura += str(digito(factura))
    nit += str(digito(nit))
    fecha += str(digito(fecha))
    monto += str(digito(monto))
    suma = int(auto) + int(factura) + int(nit) + int(fecha) + int(monto)
    modulo = getModulo(suma)
    base64 = getBase64(modulo)
    return getRC4(base64, llave)


def getBase64(numero):
    diccionario = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                   "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d",
                   "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                   "y", "z", "+", "/"]
    cociente = 1
    resto = 0
    palabra = ""
    while cociente > 0:
        cociente = numero / 64
        resto = numero % 64
        palabra = diccionario[resto] + palabra
        numero = cociente
    return palabra


def invertir(numero):
    return numero[::-1]


def digito(numero):
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
    mul = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
           [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
           [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
           [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
    per = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
           [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
           [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]
    num_inv = invertir(numero)
    i = 0
    check = 0
    while i < len(num_inv):
        aux1 = (i + 1) % 8
        aux2 = int(num_inv[i])
        aux3 = per[aux1][aux2]
        check = mul[check][aux3]
        i += 1
    return inv[check]


def getModulo(numero):
    return numero % 1073741823


def getRC4(numero, llave):
    estado = []
    codigo = ""
    nrohex = ""
    x, y, index1, index2, nmen, i, op1, aux, op2 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    while i <= 255:
        estado.append(1)
        estado[i] = i
        i += 1
    i = 0
    while i <= 255:
        if llave[index1] == " ":
            op1 = 191
        else:
            op1 = ord(llave[index1])
        index2 = (op1 + estado[i] + index2) % 256
        aux = estado[i]
        estado[i] = estado[index2]
        estado[index2] = aux
        index1 = (index1 + 1) % len(llave)
        i = i + 1
    i = 0
    while i < len(numero):
        x = (x + 1) % 256
        y = (estado[x] + y) % 256
        aux = estado[x]
        estado[x] = estado[y]
        estado[y] = aux
        op1 = ord(numero[i])
        op2 = estado[(estado[x] + estado[y]) % 256]
        nmen = op1 ^ op2
        nrohex = hex(nmen).upper()[2:]
        if len(nrohex) == 1:
            nrohex = "0" + nrohex
        codigo = codigo + nrohex + "-"
        i += 1
    return codigo[0:len(codigo) - 1]