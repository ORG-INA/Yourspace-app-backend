# Create your views here.
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.request import Request
from inventario.models import AdquisicionInventario, Inventario
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import Marca, Categoria, TemporadaEvento, Producto
from .serializers import IngresarProductoEInventarioSerializer, MarcaSerializer, CategoriaSerializer, TemporadaEventoSerializer, ProductoSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from main.permissions import IsStaffUser

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

    # def list(self, request: Request, *args, **kwargs):
    #     print("Es staff?: ", request.user.is_staff)
    #     if not request.user.is_staff:
    #         return Response({"detail": "No tienes permisos para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
    #     return super().list(request, *args, **kwargs) 

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsStaffUser()]
        return []

class TemporadaEventoViewSet(viewsets.ModelViewSet):
    queryset = TemporadaEvento.objects.all()
    serializer_class = TemporadaEventoSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsStaffUser()]
        return []

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsStaffUser()]
        return []
    
    def get_queryset(self):
        # Aquí puedes personalizar tu consulta utilizando select_related y prefetch_related
        return Producto.objects.select_related('marca').prefetch_related('categorias', 'temporadas_evento')

class ProductoInventarioView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsStaffUser()]
        return []

    def post(self, request):
        serializer = IngresarProductoEInventarioSerializer(data=request.data)
        if serializer.is_valid():
            # Crear una instancia de Producto
            producto = Producto.objects.create(
                nombre=serializer.validated_data['nombre'],
                descripcion=serializer.validated_data.get('descripcion'),
                precio=serializer.validated_data['precio'],
                descuento=serializer.validated_data.get('descuento'),
                marca=serializer.validated_data.get('marca'),
                imagen=serializer.validated_data.get('imagen')                
            )

            # Asignar las categorías al producto utilizando el método set()
            categorias = serializer.validated_data['categorias']
            producto.categorias.set(categorias)

            # Crear una instancia de Inventario
            inventario = Inventario.objects.create(
                producto=producto,
                cantidad_disponible=serializer.validated_data['cantidad']
            )

            # Crear una instancia de AdquisicionInventario
            adquisicion_inventario = AdquisicionInventario.objects.create(
                producto=inventario,
                cantidad=serializer.validated_data['cantidad'],
                fecha=serializer.validated_data['fecha'],
                precio_unidad=serializer.validated_data['precio']
            )

            return Response({'message': 'Producto creado exitosamente'}, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request):
   
        try:
            id_producto = request.data.get('id_producto')
            if id_producto:
                try:
                    producto = Producto.objects.get(pk=id_producto)
                    # Realiza la actualización del producto aquí
                    # Asegúrate de usar el serializer para validar y actualizar los datos.
                    serializer = IngresarProductoEInventarioSerializer(producto, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        inventario = Inventario.objects.get(pk=request.data.get('id_inventario'))
                        inventario.cantidad_disponible = serializer.validated_data['cantidad']
                        inventario.save()
                        print(inventario.cantidad_disponible)
                        return Response({'message': 'Producto actualizado exitosamente'}, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Producto.DoesNotExist:
                    return Response({'error': 'El producto no existe'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Se requiere un ID de producto válido en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

def paginar_productos(request, page):
    productos = Producto.objects.order_by('id_producto')  # Ordena por el índice autoincremental
    paginator = Paginator(productos, 5)  # Divide en páginas de 10 elementos

    try:
        page = int(page)
    except ValueError:
        page = 1

    page_data = paginator.get_page(page)
    
    serialized_data = [{'id_producto': p.id_producto, 'nombre': p.nombre, 'descripcion': p.descripcion, 'precio': p.precio, 'descuento': p.descuento} for p in page_data]

    return JsonResponse({'productos': serialized_data})

def get_object_by_id_or_name(model, value):
    if value.isdigit():
        return get_object_or_404(model, pk=value)
    else:
        try:
            # Verificar si el modelo tiene un campo 'nombre'
            if hasattr(model, 'nombre'):
                return get_object_or_404(model, nombre=value)
            # Verificar si el modelo tiene un campo 'nombre_marca'
            elif hasattr(model, 'nombre_marca'):
                return get_object_or_404(model, nombre_marca=value)
            # Verificar si el modelo tiene un campo 'nombre_categoria'
            elif hasattr(model, 'nombre_categoria'):
                return get_object_or_404(model, nombre_categoria=value)
        except model.DoesNotExist:
            return None  # Manejar el caso en que no se encuentre el objeto


def filtrar_productos(request, marca, categoria, temporada):
    # Maneja el valor "null" o "undefined" como None
    if marca.lower() == "null" or marca.lower() == "undefined":
        marca = None
    if categoria.lower() == "null" or categoria.lower() == "undefined":
        categoria = None
    if temporada.lower() == "null" or temporada.lower() == "undefined":
        temporada = None

    # Construir un diccionario con los parámetros que se proporcionaron
    filtros = {}

    if marca:
        marca_obj = get_object_by_id_or_name(Marca, marca.capitalize())
        filtros['marca'] = marca_obj
    
    if categoria:
        # Cambiar get_object_or_404 por filter
        categoria_objs = get_object_by_id_or_name(Categoria, categoria.capitalize())
        filtros['categorias__in'] = [categoria_objs]
    
    if temporada:
        # Cambiar get_object_or_404 por filter
        temporada_objs = get_object_by_id_or_name(TemporadaEvento, temporada)
        filtros['temporadas_evento__in'] = [temporada_objs]

    print(filtros)
    
    if filtros.get('marca') is None and filtros.get('categorias__in') is None and filtros.get('temporadas_evento__in') is None:
        return JsonResponse({'productos': ProductoSerializer(Producto.objects.all(), many=True).data})

    # Realiza la consulta para obtener los productos que cumplen con los filtros
    productos_filtrados = Producto.objects.filter(**filtros)
    print(productos_filtrados)
    # Utiliza el serializer para convertir los resultados a JSON
    serializer = ProductoSerializer(productos_filtrados, many=True)
    productos_serializados = serializer.data

    # Puedes hacer lo que necesites con los productos_filtrados, como renderizarlos en un template
    return JsonResponse({'productos': productos_serializados})