from django.contrib import admin

from django.contrib import admin

from .models import (
    Categoria,
    Produto,
    Cliente,
    Pedido,
    ItemPedido
)

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(ItemPedido)