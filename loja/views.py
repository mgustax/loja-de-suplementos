import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
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
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            
            if not username or not password:
                return JsonResponse({'error': 'Username e password são obrigatórios'}, status=400)
                
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Usuário já existe'}, status=400)
                
            user = User.objects.create_user(username=username, email=email, password=password)
            Cliente.objects.create(usuario=user)
            return JsonResponse({'message': 'Usuário criado com sucesso'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
            
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
<<<<<<< HEAD
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
=======
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login realizado com sucesso'})
            else:
                return JsonResponse({'error': 'Credenciais inválidas'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
            
    return JsonResponse({'error': 'Método não permitido'}, status=405)
>>>>>>> main

@csrf_exempt
def logout_view(request):
    if request.method in ['POST', 'GET']:
        logout(request)
        return JsonResponse({'message': 'Logout realizado com sucesso'})
    return JsonResponse({'error': 'Método não permitido'}, status=405)

# --- VIEW DE LÓGICA DO CARRINHO ---

@csrf_exempt
def quantidade_view(request):
    """View focada estritamente na lógica do carrinho"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Não autenticado'}, status=401)
        
    cliente = getattr(request.user, 'cliente', None)
    if not cliente:
        return JsonResponse({'error': 'Apenas clientes podem ter carrinho'}, status=403)

    pedido, created = Pedido.objects.get_or_create(cliente=cliente, status='PENDENTE')
    
    if request.method == 'GET':
        itens = ItemPedido.objects.filter(pedido=pedido)
        itens_data = [
            {
                'id': item.id,
                'produto_id': item.produto.id,
                'produto_nome': item.produto.nome,
                'quantidade': item.quantidade,
                'preco_unitario': str(item.preco),
                'subtotal': str(item.preco * item.quantidade)
            } for item in itens
        ]
        return JsonResponse({'pedido_id': pedido.id, 'itens': itens_data})
        
<<<<<<< HEAD
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
=======
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')
            quantidade = int(data.get('quantidade', 1))
            
            produto = get_object_or_404(Produto, id=produto_id)
            
            item, item_created = ItemPedido.objects.get_or_create(
                pedido=pedido, 
                produto=produto,
                defaults={'preco': produto.preco, 'quantidade': quantidade}
            )
            
            if not item_created:
                if quantidade <= 0:
                    item.delete()
                    return JsonResponse({'message': 'Item removido do carrinho'})
                else:
                    item.quantidade = quantidade
                    item.save()
                    
            return JsonResponse({
                'message': 'Carrinho atualizado', 
                'produto': produto.nome, 
                'quantidade_atual': item.quantidade if quantidade > 0 else 0
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Quantidade inválida'}, status=400)
            
    return JsonResponse({'error': 'Método não permitido'}, status=405)
>>>>>>> main
