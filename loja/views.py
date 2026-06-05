from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Cliente, Produto, Pedido, ItemPedido

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
            return redirect('quantidade')
        else:
            return render(request, 'loja/login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'loja/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def quantidade_view(request):
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
                
        return redirect('quantidade')
        
    itens = ItemPedido.objects.filter(pedido=pedido)
    # Todos os produtos para podermos adicionar ao carrinho na tela
    produtos = Produto.objects.filter(ativo=True)
    return render(request, 'loja/carrinho.html', {'pedido': pedido, 'itens': itens, 'produtos': produtos})
