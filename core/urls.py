from django.urls import path, include
from rest_framework import routers
from core import views



#Este enrutador nos permite manejar multiples rutas
router = routers.DefaultRouter()
router.register(r'pagos',views.pagosViewSets)
router.register(r'gastos',views.gastoViewSets)

urlpatterns = [
    path('',include(router.urls))
]