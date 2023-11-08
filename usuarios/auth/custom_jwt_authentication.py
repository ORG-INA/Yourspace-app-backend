from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def get_raw_token(self, request):
        return super().get_raw_token(request)
        # Obtén el token desde las cookies
        token = request.COOKIES.get('token')
        print("CustomJWTAuthentication - Token desde las cookies: ", token)
        return token
