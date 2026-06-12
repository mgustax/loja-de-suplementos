import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect

from .models import Cliente, Produto, Pedido, ItemPedido


# --- VIEWS DE NAVEGAÇÃO ---

def home_view(request):
    return render(request, 'loja/home.html')


def produtos_view(request):
    produtos = Produto.objects.all()
    return render(request, 'loja/produtos.html', {
        'produtos': produtos })


def detalhe_view(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'loja/detalhe.html', {'produto': produto})


# --- AUTENTICAÇÃO ---

@csrf_exempt
def cadastro_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            if not username or not password:
                return JsonResponse(
                    {'error': 'Username e password são obrigatórios'},
                    status=400
                )

            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {'error': 'Usuário já existe'},
                    status=400
                )

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            Cliente.objects.create(usuario=user)

            return JsonResponse(
                {'message': 'Usuário criado com sucesso'},
                status=201
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'JSON inválido'},
                status=400
            )

    return JsonResponse(
        {'error': 'Método não permitido'},
        status=405
    )


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'loja/login.html',
            {'error': 'Credenciais inválidas'}
        )

    return render(request, 'loja/login.html')


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('home')


# --- CARRINHO ---

@csrf_exempt
def quantidade_view(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Não autenticado'},
            status=401
        )

    cliente = getattr(request.user, 'cliente', None)

    if not cliente:
        return JsonResponse(
            {'error': 'Apenas clientes podem ter carrinho'},
            status=403
        )

    pedido, created = Pedido.objects.get_or_create(
        cliente=cliente,
        status='PENDENTE'
    )

    itens = ItemPedido.objects.filter(pedido=pedido)

    return render(
        request,
        'loja/carrinho.html',
        {
            'pedido': pedido,
            'itens': itens
        }
    )


def adicionar_ao_carrinho(request):

    if request.method == 'POST':

        produto_id = request.POST.get('produto_id')

        if produto_id:
            produto = get_object_or_404(
                Produto,
                id=produto_id
            )

            if request.user.is_authenticated:

                cliente = getattr(
                    request.user,
                    'cliente',
                    None
                )

                if cliente:

                    pedido, _ = Pedido.objects.get_or_create(
                        cliente=cliente,
                        status='PENDENTE'
                    )

                    item, created = ItemPedido.objects.get_or_create(
                        pedido=pedido,
                        produto=produto,
                        defaults={
                            'preco': produto.preco,
                            'quantidade': 1
                        }
                    )

                    if not created:
                        item.quantidade += 1
                        item.save()

        return redirect('carrinho')

    return redirect('produtos')
