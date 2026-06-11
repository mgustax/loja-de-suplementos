from django.db import models
from django.contrib.auth.models import User

# =========================
# Categoria
# =========================

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# =========================
# Produto
# =========================

class Produto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    nome = models.CharField(max_length=200) 

    descricao = models.TextField()

    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    estoque = models.IntegerField()

    imagem = models.ImageField(
        upload_to='produtos/'
    )

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nome


# =========================
# Cliente
# =========================

class Cliente(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    endereco = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.usuario.username


# =========================
# Pedido
# =========================

class Pedido(models.Model):

    STATUS = (
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('ENVIADO', 'Enviado'),
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDENTE'
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Pedido #{self.id}'


# =========================
# Item do Pedido
# =========================

class ItemPedido(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )

    quantidade = models.IntegerField(default=1)

    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def __str__(self):
        return self.produto.nome