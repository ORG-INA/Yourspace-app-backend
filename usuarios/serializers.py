from datetime import datetime
from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenRefreshSlidingSerializer, TokenVerifySerializer,TokenObtainPairSerializer, TokenRefreshSerializer, TokenBlacklistSerializer
from rest_framework_simplejwt.settings import api_settings, settings

from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token, RefreshToken, SlidingToken, UntypedToken, BlacklistedToken
from rest_framework.exceptions import ValidationError


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

class CombinedTokenSerializer(TokenRefreshSerializer):
    refresh = ""
    access = ""
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        refresh = self.context['request'].COOKIES.get('refresh')
        token = self.context['request'].COOKIES.get('token')

        if token:
            try:
                tokenVerified = self.verifying(token)
                exp_date = datetime.utcfromtimestamp(tokenVerified['exp'])
                time_diff = exp_date - datetime.utcnow()
                print("Tiempo restante del token: ", time_diff.total_seconds())

                if time_diff.total_seconds() < 300:
                    print("Token expirado")
                    tokenSlided = self.sliding(token)
                    if tokenSlided:
                        print("Token slided con éxito")
                        return tokenSlided
                else:
                    print("Token no expirado y verificado con éxito")
                    return {"access": token, "refresh": refresh}
            except Exception as e:
                print(f"Error durante la verificación del token: {e}")
                print("Token expirado y no verificado, intentado refrescar...")
                tokenRefreshed = self.refreshing(refresh)
                if tokenRefreshed:
                    return tokenRefreshed
        else:
            print("No hay token, intentando refrescar...")
            try:
                return self.refreshing(refresh)
            except Exception as e:
                print("No se pudo refrescar el token")
                print(e)

    def verifying(self, token) -> dict:
        print("Verificando token...")
        token = UntypedToken(token)
        
        if (api_settings.BLACKLIST_AFTER_ROTATION and "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise ValidationError("Token is blacklisted")
        
        return token.payload

    def refreshing(self, refresh_token) -> dict:
        print("Refrescando token...")
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
        print("Token refrescado con éxito")
        return data

    def sliding(self, token) -> SlidingToken:
        print("Sliding token...")
        token = SlidingToken(token)
        print("Token slided con éxito")
        token.check_exp(api_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

        token.set_exp()
        token.set_iat()

        return token




            