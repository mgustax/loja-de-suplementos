from django.urls import path
from . import views

urlpatterns = [
    # Páginas
    path('', views.home_view, name='home'),
    path('produtos/', views.produtos_view, name='produtos'),
    path('carrinho/', views.quantidade_view, name='carrinho'),

    # Produto
    path('produto/<int:produto_id>/', views.detalhe_view, name='detalhe'),
    path('quantidade/', views.quantidade_view, name='quantidade'),

    # Autenticação
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),

    # Carrinho
    path('adicionar-ao-carrinho/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),

    # APIs
    path('api/cadastro/', views.cadastro_view, name='api_cadastro'),
    path('api/login/', views.login_view, name='api_login'),
    path('api/logout/', views.logout_view, name='api_logout'),
    path('api/carrinho/', views.quantidade_view, name='api_carrinho'),
]