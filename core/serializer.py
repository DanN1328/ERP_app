from rest_framework import serializers
from .models import Gastos, Banco, DetallePago, Pagos

#Vamos a serializar los datos
class gastoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Gastos
        #fields = '__all__'
        fields = ('nombre_gasto','cliente','monto_total','monto_pagado','estatus')
    
class detallePagoSerializers(serializers.ModelSerializer):
    class Meta:
        model = DetallePago
        fields = '__all__'

class bancoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banco
        fields = '__all__'
    
class pagoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pagos
        fields = ('nombre_pago','monto_pago','fecha_creacion','estatus')