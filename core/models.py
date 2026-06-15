from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

ESTATUS_GASTO = [
    ("PENDING", "Pendiente"),
    ("APPROVED", "Aprobado"),
    ("CANCELLED", "Cancelado"),
    ("PAID", "Pagado"),
    ("IN-PROCESS","Procesando")
]
# Create your models here.

#Tabla de clientes
class Cliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.nombre
    
#Tabla de banco
class Banco (models.Model):
    
    banco_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    fondos = models.DecimalField(max_digits=12,decimal_places=2)

#Tabla de gastos
class Gastos(models.Model):
    gasto_id = models.BigAutoField(primary_key=True)
    nombre_gasto = models.CharField(max_length=100)
    detalle_gasto = models.TextField()
    cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT)
    monto_total = models.DecimalField(max_digits=12,decimal_places=2)
    monto_pagado = models.DecimalField(max_digits=12,decimal_places=2)
    creado_por = models.ForeignKey(User,on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=12,choices=ESTATUS_GASTO,default="PENDING")

    #Función para buscar gastos pendientes
    def get_pending_gastos():
        gastosP = Gastos.objects.filter(estatus = "PENDING")
        return gastosP

    #Función para aprobar gasto
    def aprob_gastos(id_gasto: int):
        gasto = Gastos.objects.get(gasto_id = id_gasto)
        if(gasto.estatus == 'CANCELLED'):
            return "CANCELLED"
            #raise Exception ("El gasto ya fue cancelado y no se puede aprobar")

        if(gasto.estatus != 'PENDING'):
            return "OTRO"
            #raise Exception ("El gasto ya fue revisado")
        gasto.estatus = "APPROVED"
        gasto.save()
        return "APPROVED"
            
    #Función para aprobar gasto
    def reject_gastos(id_gasto: int):
        gasto = Gastos.objects.get(gasto_id = id_gasto)
        if(gasto.estatus == 'CANCELLED'):
            return "CANCELLED"
            #raise Exception ("El gasto ya fue cancelado")
        if(gasto.estatus != 'PENDING'):
            return "OTRO"
            #raise Exception ("El gasto ya fue revisado")
        gasto.estatus = "CANCELLED"
        gasto.save()
        return "APPROVED"


#Tabla de pagos
class Pagos(models.Model):
    pago_id = models.BigAutoField(primary_key=True)
    gasto_id = models.ForeignKey(Gastos,on_delete=models.PROTECT)
    banco_id = models.ForeignKey(Banco, on_delete=models.PROTECT,default='1',null=True)
    nombre_pago = models.CharField(max_length=100)
    detalle_pago = models.TextField()
    monto_pago = models.DecimalField(max_digits=12,decimal_places=2)
    creado_por = models.ForeignKey(User,on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=12,choices=ESTATUS_GASTO,default="PENDING")

    #Función para buscar gastos pendientes
    def get_pending_pays():
        paysP = Pagos.objects.filter(estatus = "PENDING")
        return paysP
    
    #Función para aprobar pagos
    def aprob_pagos(id_pago: int):
        pago = Pagos.objects.get(pago_id = id_pago)
        if (pago.estatus == 'CANCELLED'):
            return "PAGO CANCELADO"
            #raise Exception("El pago fue cancelado y no se puede modificar")
        if(pago.estatus != 'PENDING'):
            return "OTRO"
            #raise Exception ("El pago ya fue revisado")
        pago.estatus = "APPROVED"
        pago.save()
        return "CORRECTO"
        """
        flag = Pagos.pagar_gasto(id_pago)
        if flag != "PAGADO":
            pago.estatus = "PENDING"
            pago.save()
            return flag
        else:
            return "CORRECTO"
            """
    def pagar_aprobados(gasto, monto, banco):
        fondos = Banco.objects.get(banco_id=banco)
        detalleGasto = Gastos.objects.get(gasto_id=gasto)
        #Monto a pagar del pago actual más el monto ya pagado
        sumaPagos=monto + detalleGasto.monto_pagado
        if(sumaPagos > detalleGasto.monto_total):
            return "PAGO EXCEDENTE DE MONTO TOTAL"
        elif(fondos.fondos < monto):
            return "CUENTA SIN SUFICIENTES FONDOS"
        elif(sumaPagos < detalleGasto.monto_total):
            detalleGasto.monto_pagado = sumaPagos
            detalleGasto.save()
            fondos.fondos -= monto
            fondos.save()
            return "PAGOPARCIAL"
        elif(sumaPagos == detalleGasto.monto_total):
            detalleGasto.monto_pagado = monto
            detalleGasto.estatus = "PAID"
            detalleGasto.save()
            fondos.fondos -= monto
            fondos.save()
            return "PAGOCOMPLETADO"
        else:
            return "Revisar montos"




    #Función para cancelar pagos
    def reject_pagos(id_pago: int):
        pago = Pagos.objects.get(pago_id = id_pago)
        if (pago.estatus == 'CANCELLED'):
            return "CANCELLED"
            #raise Exception("El pago fue cancelado y no se puede modificar")
        if(pago.estatus != 'PENDING'):
            return "OTRO"
            #raise Exception ("El pago ya fue revisado")
        pago.estatus = "CANCELLED"
        pago.save()
        gasto = pago.gasto_id
        gasto.estatus = "APPROVED"
        gasto.save()
        return "REJECT"

    #Función para pagar
    def pagar_gasto(id_pago: int):
        pago = Pagos.objects.get(pago_id = id_pago)
        #Validamos la cuenta bancaria y sus fondos
        fondos = pago.banco_id.fondos
        if(fondos < pago.monto_pago):
            pago = Pagos.objects.get(pago_id = id_pago)
            pago.estatus = 'PENDING'
            pago.save()
            return "SIN FONDOS EN LA CUENTA"
            #raise Exception("La cuenta bancaria no tiene suficientes fondos")

        if pago.gasto_id.estatus != "APPROVED":
            return "GASTO NO ESTA APROBADO"
            #raise Exception("El gasto no está aprobado")
        
        if pago.estatus != "APPROVED":
            return "PAGO NO ESTA APROBADO"
            #raise Exception("El pago no está aprobado")
        
        if pago.estatus == "PAID":
            return "ESTE PAGO YA FUE REALIZADO"
            #raise Exception("Este pago ya fue realizado")
        
        pagado = pago.gasto_id.monto_pagado
        monto = pagado + pago.monto_pago
        gasto = Gastos.objects.get(gasto_id = pago.gasto_id.gasto_id)
        if (monto == gasto.monto_total):
            banco = Banco.objects.get(banco_id = pago.banco_id.banco_id)
            monto_anterior = banco.fondos
            banco.fondos = banco.fondos - pago.monto_pago
            banco.save()
            Movimientos.movdb(pago.pago_id, monto_anterior)
            pago.estatus = 'PAID'
            pago.save()
            gasto.estatus = "PAID"
            gasto.monto_pagado = gasto.monto_total
            gasto.save()
            return "PAGADO"
        elif(monto < gasto.monto_total):
            banco = Banco.objects.get(banco_id = pago.banco_id.banco_id)
            monto_anterior = banco.fondos
            banco.fondos = banco.fondos - pago.monto_pago
            Movimientos.movdb(pago.pago_id, monto_anterior)
            gasto.monto_pagado = monto
            pago.estatus = "PAID"
            banco.save()
            pago.save()
            gasto.save()
            return "PAGADO"
        else:
            return "ERROR revisar montos"
            #raise Exception("ERROR revisar montos")

#Tabla movimientos bancarios
class Movimientos(models.Model):
    movimiento_id = models.BigAutoField(primary_key=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    id_pago = models.ForeignKey(Pagos,on_delete=models.PROTECT)
    pago = models.DecimalField(max_digits=12,decimal_places=2)
    monto_anterior = models.DecimalField(max_digits=12,decimal_places=2)
    monto_resultante = models.DecimalField(max_digits=12,decimal_places=2)

    def movdb(id: int, monto: float):
        pagos = Pagos.objects.get(pago_id = id)
        print(f"Monto actual : {pagos.banco_id.fondos} y Monto resultante: {monto - pagos.monto_pago}")
        Movimientos.objects.create(
            fecha_movimiento = timezone.localtime().date(),
            id_pago = pagos,
            pago = pagos.monto_pago,
            monto_anterior = monto,
            monto_resultante = monto - pagos.monto_pago
        )
#Modelo de detalles de pagos
class DetallePago(models.Model):
    detalle_pago_id = models.AutoField(primary_key=True)
    pago = models.ForeignKey(Pagos,on_delete=models.PROTECT,)
    banco = models.ForeignKey(Banco,on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=12,decimal_places=2)
    fecha_pago = models.DateField()
    usuario = models.ForeignKey(User,on_delete=models.PROTECT)


