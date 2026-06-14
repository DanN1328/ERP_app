from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.db.models import Sum,Count
from rest_framework import viewsets
from .serializer import *
from django.utils import timezone
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

#LOGIN LOGOUT
def login_view(request):
     if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request,"Usuario o contraseña incorrectos")
     return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
# MENUS
@login_required
def menu(request):
    bancos = Banco.objects.all()
    banco_activo = request.session.get("banco_activo")
    if banco_activo:
        banco_activo = int(banco_activo)
    return render(request, "menu.html",{"Bancos":bancos,"banco_activo": banco_activo})
@login_required
def gastos(request):
    cliente = Cliente.objects.all()
    return render(request, "crearGasto.html",{"Cliente":cliente})
@login_required
def pagos(request):
    gastosP = Gastos.objects.filter(estatus = 'APPROVED')
    return render(request, "pagos.html",{"Gastos":gastosP})

@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes.html",{"Clientes":clientes})

#BUSQUEDA
@login_required
def buscarGastos(request):
    gastosP = Gastos.get_pending_gastos()
    return render(request, "gastosPendientes.html",{"Gastos":gastosP})

@login_required
def pagosAprobados(request):
    aprobados = Pagos.objects.filter(estatus="APPROVED")
    return render(request, "pagosAprobados.html",{"Aprobados":aprobados})

@login_required
def buscarPagos(request):
    pagosP = Pagos.get_pending_pays()
    return render(request, "pagosPendientes.html",{"Pagos":pagosP})

@login_required
def cuentas(request):
    cuentas = Banco.objects.all()
    return render(request, "cuentas.html",{"Cuenta":cuentas})

@login_required
def seleccionarBanco(request):
    if request.method == "POST":
        banco_id = request.POST.get("banco_id")
        request.session["banco_activo"] = banco_id
    return redirect("menu")

#Formularios
@login_required
def detallesGasto(request, id):
    gasto = Gastos.objects.get(gasto_id = id)
    cuentas = Banco.objects.all()
    faltante = gasto.monto_total - gasto.monto_pagado
    return render(request,"crearPagos.html",{"Gastos":gasto,"Cuenta":cuentas, "Faltante": faltante})


#ACCIONES
@login_required
def crearCliente(request):
    if request.method == 'POST':
        nombre = request.POST.get("nombre")
        filtro = Cliente.objects.filter(nombre = nombre).exists()
        if filtro:
            messages.error(request,"ERROR: Este cliente ya existe")
            return redirect("cliente")
        else:
            Cliente.objects.create(
                nombre = nombre
            )
            messages.success(request,"Cliente creado exitosamente")
            return redirect("cliente")
@login_required
def crearGasto(request):
    if request.method == 'POST':
        #Obtenemos los valores
        nombre = request.POST.get("nombre_gasto")
        detalle = request.POST.get("detalle_gasto")
        cliente = request.POST.get("cliente")
        cliente = Cliente.objects.get(id=cliente)
        monto = request.POST.get("monto")

        #Creamos el gasto
        Gastos.objects.create(
            nombre_gasto = nombre,
            detalle_gasto = detalle,
            cliente = cliente,
            monto_total = monto,
            monto_pagado = 0,
            creado_por = request.user,
            fecha_creacion = timezone.now().date(),
            estatus = 'PENDING'
        )
        messages.success(request, 'Gasto creado con éxito')
        return redirect("menu")
@login_required
def crearPago(request, id: int):
    #Obtenemos los valores
    gasto = Gastos.objects.get(gasto_id = id)
    nombre = gasto.nombre_gasto
    detalle = gasto.detalle_gasto
    if(gasto.estatus == 'APPROVED'):
        Pagos.objects.create(
                gasto_id = gasto,
                banco_id = None,
                nombre_pago = nombre,
                detalle_pago = detalle,
                monto_pago = gasto.monto_total,
                creado_por = request.user,
                fecha_creacion = timezone.now().date(),
                estatus = 'PENDING'
            )
        gasto.estatus = "IN-PROCESS"
        gasto.save()
        messages.success(request,"Pago creado correctamente")
        return redirect("menu")
    else:
        messages.error(request, "El pago ya fue creado")
        return redirect("menu")
    """
    pagosP = validarPagoPendientes(gasto.gasto_id)
    if(pagosP == 0 or (pagosP + Decimal(monto) + gasto.monto_pagado)<=gasto.monto_total):
        #Creamos el pago
        Pagos.objects.create(
            gasto_id = gasto,
            banco_id = banco,
            nombre_pago = nombre,
            detalle_pago = detalle,
            monto_pago = monto,
            creado_por = request.user,
            fecha_creacion = timezone.now().date(),
            estatus = 'PENDING'
        )
        messages.success(request, 'Pago creado con éxito')
    elif((pagosP + Decimal(monto) + gasto.monto_pagado) > gasto.monto_total):
        messages.error(request, f'ERROR: el pago actual excedería los pagos pendientes por aprobar del gasto: {gasto.nombre_gasto}, favor de pagar primero los pendientes')
    return redirect("menu")"""

@login_required
def crearBanco(request):
    if request.method == 'POST':
        #Obtenemos los valores
        nombre = request.POST.get("nombre")
        fondos = request.POST.get("fondos")

        if (Decimal(fondos) < 0):
            messages.error(request,"No es posible añadir cantidades negativas, FAVOR DE REVISAR")
            return redirect("cuentas")

        Banco.objects.create(
            nombre = nombre,
            fondos = fondos
        )
        messages.success(request, 'Cuenta bancaria creada con éxito')
        return redirect("cuentas")
  
@login_required
def administrarFondos(request):
    if request.method == 'POST':
        id = request.POST.get("banco_id")
        tipo = request.POST.get("tipo")
        monto = Decimal(request.POST.get("monto"))
        
        banco = Banco.objects.get(banco_id=id)
        if tipo == 'deposito':
            if (monto <= 0):
                messages.error(request,"No es posible añadir cantidades en 0 o negativas FAVOR DE REVISAR")
                return redirect("cuentas")
            banco.fondos += monto
            messages.success(request, f'Montos añadidos a la cuenta: {banco.nombre}')
        elif tipo == 'retiro':
            if (monto <= 0):
                messages.error(request,"No es posible eliminar cantidades en 0 o negativas FAVOR DE REVISAR")
                return redirect("cuentas")
            banco.fondos -= monto
            if(banco.fondos <= 0):
                messages.error(request,"No es posible eliminar más de lo que tiene la cuenta")
                banco.fondos += monto
            else:
                messages.success(request, f'Montos eliminados de la cuenta: {banco.nombre}')
        banco.save()
    return redirect("cuentas")

#APROBACIONES
@login_required
def aprobarPago(request, id):
    estatus = Pagos.aprob_pagos(id)
    if estatus == "CANCELLED":
        messages.error(request,"El pago fue cancelado y no se puede modificar")
    elif estatus == 'OTRO':
        messages.error(request, "El pago ya fue revisado")
    elif estatus != "CORRECTO":
        messages.error(request, f"Mensaje de error: {estatus}")
    else:
        messages.success(request, 'Pago aprobado con éxito')
    return redirect("Pagos")

@login_required
def rechazarPago(request, id):
    estatus = Pagos.reject_pagos(id)
    if estatus == "CANCELLED":
        messages.error(request,"El pago ya ha sido cancelado y no se puede revertir")
    elif estatus == "OTRO":
        messages.warning(request,"Este pago ya fue revisado")
    else:
        messages.success(request, 'Pago rechazado exitosamente')
    return redirect("Pagos")

@login_required
def aprobarGasto(request, id):
    estatus = Gastos.aprob_gastos(id)
    if estatus == 'CANCELLED':
        messages.error(request,"El gasto ya fue cancelado y no se puede revertir")
    elif estatus == 'OTRO':
        messages.warning(request,"El gasto ya fue revisado")
    else:
        messages.success(request, 'Gasto aprobado con éxito')
    return redirect("Gastos")

@login_required
def rechazarGasto(request, id):
    estatus = Gastos.reject_gastos(id)
    if estatus == 'CANCELLED':
        messages.error(request,"El gasto ya fue cancelado y no se puede revertir")
    elif estatus == 'OTRO':
        messages.warning(request,"El gasto ya fue revisado")
    else:
        messages.success(request, 'Gasto rechazado')
    return redirect("Gastos")

@login_required
def validarPagoPendientes(gasto):
    suma = Pagos.objects.filter(gasto_id=gasto, estatus='PENDING').aggregate(suma_total=Sum("monto_pago"))
    if (suma["suma_total"] == None):
        return 0
    else:
        return suma["suma_total"]

#Pago de aprobados
@login_required
def pagar(request,id_gasto):
    try:
        pago = Pagos.objects.get(gasto_id=id_gasto,estatus="APPROVED")
    except Pagos.DoesNotExist:
        messages.error(request,"El pago no existe.")
        return redirect("/pagosAprobados/")
    
    if request.method == 'POST':
        pago = Pagos.objects.get(gasto_id=id_gasto,estatus="APPROVED")
        banco = request.POST.get("cuenta")
        monto = Decimal(request.POST.get("monto"))
        estatus = Pagos.pagar_aprobados(id_gasto,monto,banco)
        fondos = Banco.objects.get(banco_id=banco)
        
        if(estatus not in ["PAGOCOMPLETADO", "PAGOPARCIAL"]):
            messages.error(request,f"ERROR: {estatus}")
        elif(estatus == "PAGOCOMPLETADO"):
            pago.estatus = "PAID"
            pago.save()

            #Creamos el detalle de pago 
            pago = Pagos.objects.get(gasto_id=id_gasto)
            DetallePago.objects.create(
                pago = pago,
                banco = fondos,
                monto = monto,
                fecha_pago = timezone.now().date(),
                usuario = request.user
            )
            messages.success(request,"Pago realizado correctamente")
        elif(estatus == "PAGOPARCIAL"):
            #Creamos el detalle de pago 
            pago = Pagos.objects.get(gasto_id=id_gasto)
            DetallePago.objects.create(
                pago = pago,
                banco = fondos,
                monto = monto,
                fecha_pago = timezone.now().date(),
                usuario = request.user
            )
            messages.success(request,"Pago parcial realizado correctamente")
        return redirect("/pagosAprobados/")
    else:
        messages.error(request,"El pago ya fue procesado")
        return redirect("/pagosAprobados/")


#Dashboard superior
@login_required
def dashboard(request):
    banco_activo = request.session.get("banco_activo")
    gastos_pendientes = Gastos.objects.filter(estatus='PENDING').count()
    pagos_pendientes = Pagos.objects.filter(estatus='PENDING').count()
    clientes = Cliente.objects.count()

    if banco_activo:
        fondos_totales = Banco.objects.filter(banco_id=banco_activo).aggregate(total=Sum("fondos"))["total"]
    else:
        fondos_totales = Banco.objects.aggregate(total=Sum('fondos'))["total"]
    return JsonResponse({
        "Fondos_Totales":round(Decimal(fondos_totales or 0), 2),
        "Gastos_Pendientes":gastos_pendientes,
        "Pagos_Pendientes": pagos_pendientes,
        "Clientes":clientes
    })

#Gráficos

def grafico_gastos_mes(request):
    pagos = DetallePago.objects.values('fecha_pago').annotate(total=Sum('monto')).order_by('fecha_pago')
    contexto = []
    for i in pagos:
        contexto.append({
            "fecha":i["fecha_pago"].strftime("%m-%d"),
            "total":float(i["total"])
        })
    return JsonResponse(contexto,safe=False)


def grafico_gastos_estatus(request):
    gastos = Gastos.objects.values("estatus").annotate(monto=Count('gasto_id'))
    return JsonResponse(list(gastos),safe=False)


def pagosPorBanco(request):
    banco_activo = request.session.get("banco_activo")
    pagos = DetallePago.objects.all()

    if banco_activo:
        pagos = pagos.filter(banco_id=banco_activo)

    datos = pagos.values('fecha_pago', 'banco__nombre').annotate(total=Sum('monto')).order_by('fecha_pago')
    return JsonResponse(list(datos), safe=False)


def gastosCliente(request):
    gastos = Gastos.objects.values('cliente_id__nombre').annotate(total=Sum('monto_total')).order_by('total')
    return JsonResponse(list(gastos),safe=False)

#APIS

class gastoViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Gastos.objects.all()
    serializer_class = gastoSerializers
    permission_classes = [IsAuthenticated]

class pagosViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Pagos.objects.all()
    serializer_class = pagoSerializers
    permission_classes = [IsAuthenticated]

class detallePagoViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = DetallePago.objects.all()
    serializer_class = detallePagoSerializers
    permission_classes = [IsAuthenticated]

class bancoViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Banco.objects.all()
    serializer_class = bancoSerializers
    permission_classes = [IsAuthenticated]