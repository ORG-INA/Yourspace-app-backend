from django.urls import path
from . import views

from rest_framework import routers
from .views import ProductoInventarioView, MarcaViewSet, CategoriaViewSet, TemporadaEventoViewSet, ProductoViewSet


urlpatterns = [
    path('inventario/nuevo/', ProductoInventarioView.as_view(), name='producto e inventario'),
    path('productos/pagina/<int:page>/', views.paginar_productos, name='productos')
]

router = routers.DefaultRouter()
router.register(r'marcas', MarcaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'temporadas_evento', TemporadaEventoViewSet)
router.register(r'productos', ProductoViewSet)


urlpatterns += router.urls