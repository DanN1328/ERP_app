from django.urls import path, include
from rest_framework import routers
from core import views



#Este enrutador nos permite manejar multiples rutas
router = routers.DefaultRouter()
router.register(r'pagos',views.pagosViewSets)
router.register(r'gastos',views.gastoViewSets)
router.register(r'bancos',views.bancoViewSets)
router.register(r'detallePagos',views.detallePagoViewSets)

urlpatterns = [
    path('',include(router.urls))
]