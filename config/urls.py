"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("menu/", views.menu, name="menu"),
    path("cuentasBancarias/",views.cuentas, name="cuentas"),
    path("crear-banco/",views.crearBanco),
    path("movimiento-banco/",views.administrarFondos),
    path("seleccionar-banco/",views.seleccionarBanco),
    path("Gastos/",views.gastos),
    path("Pagos/",views.pagos),
    path("clientes/",views.clientes,name="cliente"),
    path("crearCliente/",views.crearCliente),
    path("buscarGastos/", views.buscarGastos, name="Gastos"),
    path("buscarPagos/", views.buscarPagos, name="Pagos"),
    path("aprobarPago/<int:id>", views.aprobarPago),
    path("rechazarPago/<int:id>", views.rechazarPago),
    path("aprobarGasto/<int:id>", views.aprobarGasto),
    path("rechazarGasto/<int:id>", views.rechazarGasto),
    path("crearGastos/",views.crearGasto),
    path("crearPago/<int:id>", views.crearPago),
    path("detallePagos/<int:id>",views.detallesGasto),
    path("pagosAprobados/",views.pagosAprobados),
    path('api/v1/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/v1/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('api/v1/', include('core.urls')),
    path("charts/dashboardskpi/", views.dashboard),
    path("charts/gastos_mes/",views.grafico_gastos_mes),
    path("charts/gastos_estatus/",views.grafico_gastos_estatus),
    path("charts/pagosBanco/",views.pagosPorBanco),
    path("charts/gastosCliente/",views.gastosCliente),
    path("pagarPago/<int:id_gasto>",views.pagar),
]
