from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Cliente, Produto, Pedido, ItemPedido
from django.shortcuts import redirect

# --- VIEWS DE NAVEGAÇÃO (Front-End) ---

def home_view(request):
    """Renderiza a página inicial (Home)"""
    return render(request, 'loja/home.html')

def produtos_view(request):
    """Renderiza a vitrine de produtos"""
    produtos = Produto.objects.filter(ativo=True)
    return render(request, 'loja/produtos.html', {'produtos': produtos})

def detalhe_view(request, produto_id):
    """Renderiza a página de detalhes de um produto específico"""
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'loja/detalhe.html', {'produto': produto})

# --- VIEWS DE AUTENTICAÇÃO ---

@csrf_exempt
def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'loja/cadastro.html', {'error': 'Usuário já existe'})
            
        user = User.objects.create_user(username=username, email=email, password=password)
        Cliente.objects.create(usuario=user)
        return redirect('login')
        
    return render(request, 'loja/cadastro.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirecionamento correto para a Home
            return redirect('home') 
        else:
            return render(request, 'loja/login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'loja/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- VIEW DE LÓGICA DO CARRINHO ---

@csrf_exempt
def quantidade_view(request):
    """View focada estritamente na lógica do carrinho"""
    if not request.user.is_authenticated:
        return redirect('login')
        
    cliente = getattr(request.user, 'cliente', None)
    if not cliente:
        return render(request, 'loja/carrinho.html', {'error': 'Apenas clientes podem ter carrinho'})

    pedido, created = Pedido.objects.get_or_create(cliente=cliente, status='PENDENTE')
    
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        quantidade = int(request.POST.get('quantidade', 1))
        
        produto = get_object_or_404(Produto, id=produto_id)
        
        item, item_created = ItemPedido.objects.get_or_create(
            pedido=pedido, 
            produto=produto,
            defaults={'preco': produto.preco, 'quantidade': quantidade}
        )
        
        if not item_created:
            if quantidade <= 0:
                item.delete()
            else:
                item.quantidade = quantidade
                item.save()
                
        return redirect('carrinho')
        
    itens = ItemPedido.objects.filter(pedido=pedido)
    return render(request, 'loja/carrinho.html', {'pedido': pedido, 'itens': itens})


def adicionar_ao_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        # AQUI VOCÊ COLOCA A LÓGICA DE SALVAR NA SESSÃO OU BANCO
        # Exemplo básico: print(f"Produto {produto_id} adicionado!")
        return redirect('carrinho') # Ou a página que você desejar
    return redirect('produtos')