from django.urls import include, path
from rest_framework.routers import DefaultRouter

from compras.views import CarroProductosViewSet, CarroViewSet, CompraViewSet

router = DefaultRouter()
router.register(r'carros', CarroViewSet)
router.register(r'carros-productos', CarroProductosViewSet)
router.register(r'compras', CompraViewSet)

urlpatterns = [
    # ... otras rutas ...
    path('', include(router.urls)),
]
