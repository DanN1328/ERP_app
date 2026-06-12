from rest_framework import serializers
from .models import Gastos, Pagos

#Vamos a serializar los datos
class gastoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Gastos
        #fields = '__all__'
        fields = ('nombre_gasto','cliente','monto_total','monto_pagado','estatus')
    
class pagoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pagos
        fields = '__all__'