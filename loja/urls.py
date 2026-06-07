from django.urls import path
from . import views

urlpatterns = [
    path('api/cadastro/', views.cadastro_view, name='api_cadastro'),
    path('api/login/', views.login_view, name='api_login'),
    path('api/logout/', views.logout_view, name='api_logout'),
    path('api/carrinho/', views.quantidade_view, name='api_carrinho'),
]
