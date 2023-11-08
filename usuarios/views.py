from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes

from . models import User
from . serializers import RegisterUserSerializer, MyTokenObtainPairSerializer


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
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        print("request", request)
        response = super().post(request, *args, **kwargs)
        # Si la autenticación es exitosa, establece la cookie
        if response.status_code == 200:
            token = response.data.get('access', None)
            response.set_cookie('token', str(token), httponly=True, samesite='Strict', secure=True, path='/', expires=3600)

        return response