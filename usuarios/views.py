from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken, RefreshToken
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView, TokenViewBase
from rest_framework.views import APIView


from . models import User
from . serializers import RegisterUserSerializer, MyTokenObtainPairSerializer, CustomTokenRefreshSerializer, CustomTokenBlacklistSerializer


@api_view(['POST'])
@authentication_classes([])
def register(request):
    data = request.data
    print(data)
    user = User.objects.create(
        email = data['email'],
        name = data['name'],
        last_name = data['last_name'],
        password = make_password(data['password']),
    )
    serializer = RegisterUserSerializer(user, many=False)
    return Response(serializer.data)

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        print("request", request)
        response = super().post(request, *args, **kwargs)
        # Si la autenticación es exitosa, establece la cookie
        if response.status_code == 200:
            token = response.data.get('access', None)
            refresh = response.data.get('refresh', None)
            response.set_cookie('token', str(token), httponly=True, samesite='Strict', secure=True, path='/', expires=900)
            response.set_cookie('refresh', str(refresh), httponly=True, samesite='Strict', secure=True, path='/', expires=604800)

        return response
    
class CustomTokenVerifyView(TokenViewBase):
    def post(self, request, *args, **kwargs):
        # Obtén el token del encabezado HTTP_AUTHORIZATION
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if authorization_header and authorization_header.startswith('Bearer '):
            token = authorization_header[len('Bearer '):]
        else:
            # Si el token no se encuentra en el encabezado, maneja el error apropiado
            return Response({"detail": "Token not provided in HTTP_AUTHORIZATION"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intenta analizar el token y verificar su validez
            token = UntypedToken(token)
            token.verify()
        except Exception as e:
            # Si hay un error al verificar el token, maneja el error apropiado
            return Response({"detail": f"Token verification failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # El token es válido
        return Response({"isValid": True, "isStaff":token.get('is_staff')}, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenViewBase):
    serializer_class = CustomTokenRefreshSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            token = response.data.get('access', None)
            refresh = response.data.get('refresh', None)
            
            if token and refresh:
                # Actualiza las cookies con los nuevos tokens de acceso y refresco
                response.set_cookie('token', str(token), httponly=True, samesite='Strict', secure=True, path='/', expires=900)
                response.set_cookie('refresh', str(refresh), httponly=True, samesite='Strict', secure=True, path='/', expires=604800)
            else:
                # Maneja el caso en el que no se proporcionen los nuevos tokens
                return Response({"detail": "Failed to refresh tokens"}, status=status.HTTP_400_BAD_REQUEST)

        return response

class LogoutView(TokenViewBase):
    serializer_class=CustomTokenBlacklistSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Invalidar el token de acceso y añadirlo a la lista negra
        if response.status_code == 200:          
            # Eliminar las cookies de token y refresh
            response = JsonResponse({"message": "Logout successful"})
            response.delete_cookie('token')
            response.delete_cookie('refresh')
            
            
        else:
            return Response({"message": "Failed to blacklist the token"}, status=status.HTTP_400_BAD_REQUEST)

        return response