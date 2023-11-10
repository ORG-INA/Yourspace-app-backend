from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenBlacklistSerializer
from rest_framework_simplejwt.settings import api_settings

from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from . models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "last_name", "id"]

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "last_name", "password"]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)

        token['email'] = user.email
        token['name'] = user.name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff  
        
        return token

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = ""
    access = ""
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh_token = self.context['request'].COOKIES.get('refresh')
        if refresh_token is None:
            raise serializers.ValidationError('No se ha encontrado el refresh token en la cookie')
        refresh = self.token_class(refresh_token)
        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app is not installed, `blacklist` method will not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data
    
class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    refresh = ""

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        refresh = self.token_class(self.context['request'].COOKIES.get('refresh'))
        try:
            refresh.blacklist()
        except AttributeError:
            pass
        return {}
