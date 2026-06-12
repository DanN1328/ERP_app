from django.contrib import admin

# Register your models here.
from .models import (
    Cliente,
    Banco,
    Gastos,
    Pagos,
    Movimientos,
    DetallePago
)

admin.site.register(Cliente)
admin.site.register(Banco)
admin.site.register(Gastos)
admin.site.register(Pagos)
admin.site.register(Movimientos)
admin.site.register(DetallePago)