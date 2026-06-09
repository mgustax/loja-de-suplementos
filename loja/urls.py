from django.urls import path
from . import views


urlpatterns = [
<<<<<<< HEAD
    # Mapeando para as views corretas que organizamos
    path('', views.home_view, name='home'),             # Vamos precisar criar a home_view simples
    path('produtos/', views.produtos_view, name='produtos'), 
    path('carrinho/', views.quantidade_view, name='carrinho'), 
    
    # Rotas de detalhe e quantidade (Lógica do backend)
    path('produto/<int:produto_id>/', views.detalhe_view, name='detalhe'),
    path('quantidade/', views.quantidade_view, name='quantidade'), 
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    
    # ... suas outras rotas ...
    path('adicionar-ao-carrinho/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),

]
=======
    path('api/cadastro/', views.cadastro_view, name='api_cadastro'),
    path('api/login/', views.login_view, name='api_login'),
    path('api/logout/', views.logout_view, name='api_logout'),
    path('api/carrinho/', views.quantidade_view, name='api_carrinho'),
]
>>>>>>> main
