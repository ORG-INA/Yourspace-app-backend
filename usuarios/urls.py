from django.urls import include, path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', views.CustomTokenVerifyView.as_view(), name='token_verify'),
    path('token/verifyAndRefresh/', views.CustomTokenVerifyAndRefreshView.as_view(), name='token_verify_and_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
# He aqui