from django.urls import include, path
from rest_framework.routers import DefaultRouter

from inventario.views import AdquisicionInventarioViewSet, InventarioViewSet

urlpatterns = []
router = DefaultRouter()
router.register(r'inventarios', InventarioViewSet)
router.register(r'adquisiciones-inventario', AdquisicionInventarioViewSet)

urlpatterns += router.urls

