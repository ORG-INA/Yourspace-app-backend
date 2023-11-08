from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

class ApiRoot(APIView):
    def get(self, request, format=None):
        return Response({
            'marcas': reverse('marca-list', request=request, format=format),
            'categorias': reverse('categoria-list', request=request, format=format),
            'temporadas_evento': reverse('temporadaevento-list', request=request, format=format),
            'productos': reverse('producto-list', request=request, format=format),
            'inventario': reverse('inventario-list', request=request, format=format),
            'adquisiciones_inventario': reverse('adquisicioninventario-list', request=request, format=format),
            'carros': reverse('carro-list', request=request, format=format),
            'carros_productos': reverse('carroproductos-list', request=request, format=format),
            'compras': reverse('compra-list', request=request, format=format),
        })
