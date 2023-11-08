from django.utils.deprecation import MiddlewareMixin


class CustomHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('token')
        if token:
            print("Se ha encontrado el token en la cookie y modificado el encabezado Authorization")
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'