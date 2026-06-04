from django.contrib import admin

from .models import (
    Categoria,
    Produto,
    Cliente,
    Pedido,
    ItemPedido
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nome'
    )

    search_fields = (
        'nome',
    )


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nome',
        'categoria',
        'preco',
        'estoque',
        'ativo'
    )

    search_fields = (
        'nome',
    )

    list_filter = (
        'categoria',
        'ativo'
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'usuario',
        'telefone'
    )

    search_fields = (
        'usuario__username',
    )


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'cliente',
        'status',
        'total',
        'criado_em'
    )

    list_filter = (
        'status',
    )


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'pedido',
        'produto',
        'quantidade',
        'preco'
    )