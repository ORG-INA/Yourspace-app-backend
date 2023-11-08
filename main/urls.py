from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import ApiRoot


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", ApiRoot.as_view(), name='api-root'),
    path('api/products/', include('productos.urls')),
    path('api/purchases/', include('compras.urls')),
    path('api/inventory/', include('inventario.urls')),
    path('api/users/', include('usuarios.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
