from django.db import models
from django.db.models import F
from django.contrib.auth.models import User


# PRODUTO
class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=50)
    codigo_produto = models.CharField(max_length=20)
    preco_entrada = models.FloatField(null=False)
    estoque_minimo = models.IntegerField()
    estoque_maximo = models.IntegerField()

    class Meta:
        verbose_name = "produto"
        verbose_name_plural = "produtos"

    def __str__(self) -> str:
        return f"{self.nome_produto}"


class EntradaProduto(models.Model):
    id = models.AutoField(primary_key=True)
    descricao_entrada = models.CharField(max_length=50)
    produto = models.ForeignKey(
        Produto, null=True, on_delete=models.PROTECT, related_name="produto"
    )
    quantidade = models.IntegerField()

    class Meta:
        verbose_name = "Entrada Produto"
        verbose_name_plural = "Entrada Produto"

    def __str__(self) -> str:
        return self.descricao_entrada


# ESTOQUE
class Estoque(models.Model):
    id = models.AutoField(primary_key=True)
    produto_nome = models.CharField(max_length=50)
    produto_codigo = models.CharField(max_length=20)
    quantidade = quantidade = models.IntegerField()
    estoque_minimo = models.IntegerField()
    estoque_maximo = models.IntegerField()

    class Meta:
        verbose_name = "estoque"
        verbose_name_plural = "estoques"

    def __str__(self) -> str:
        return f"{self.produto_nome} - {self.produto_codigo} - {self.quantidade}"


# SAIDA PRODUTO
class RequisicaoSaidaProduto(models.Model):
    # class StatusRequisicao(models.IntegerChoices):
    #     aguardando_liberacao, 'Aguardando Liberação'),
    #     aguardando_compra, 'Aguardando Compra'),
    #     liberada, 'Liberada'),
    #     negada 'Negada'),
    #     cancelada, 'Cancelada'),
    # }

    __STATUS_REQUISICAO = {
        ("aguardando_liberacao", "Aguardando Liberação"),
        ("aguardando_compra", "Aguardando Compra"),
        ("liberada", "Liberada"),
        ("negada", "Negada"),
        ("cancelada", "Cancelada"),
    }

    id = models.AutoField(primary_key=True)
    descricao_saida = models.CharField(max_length=50)
    status_requisicao = models.CharField(
        max_length=25,
        choices=__STATUS_REQUISICAO,
        null=False,
        default="aguardando_liberacao",
    )
    usuario = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="requisicoes"
    )

    class Meta:
        verbose_name = "Requisicao Saida"
        verbose_name_plural = "Requisicoes Saida"
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.descricao_saida

    @property  # Campo calculado direto na classe sem armazenamento no banco
    def resumo_total(self):
        queryset = self.itens.all().aggregate(
            resumo_total=models.Sum(F("quantidade") * F("produto__preco_entrada"))
        )
        return queryset["resumo_total"]


class ItemSaidaProduto(models.Model):
    id = models.AutoField(primary_key=True)
    compra = models.ForeignKey(
        RequisicaoSaidaProduto, on_delete=models.CASCADE, related_name="itens"
    )
    produto = models.ForeignKey(
        Produto, on_delete=models.PROTECT, related_name="produtos"
    )
    quantidade = models.IntegerField()

    class Meta:
        verbose_name = "Item Saida"
        verbose_name_plural = "Item Saida"

    def __str__(self) -> str:
        return f"{self.compra} - {self.produto} - {self.quantidade}"


# class RequisicaoSaidaProdutoItemSaidaProduto(models.Model):
#     id = models.AutoField(primary_key=True)
#     requisicao_saida_produto_id = models.ForeignKey(RequisicaoSaidaProduto, on_delete=models.CASCADE)
#     itens_entrada_produto_id = models.ForeignKey(
#         ItemSaidaProduto, on_delete=models.CASCADE, related_name='item_saida_produto')


# class StatusRequisição(models.Model):

#     # class StatusRequisicao(models.IntegerChoices):
#     #     aguardando = 1, 'Aguardando Liberação'
#     #     atendida = 2, 'Atendida'
#     #     negada = 3, 'Negada'
#     #     cancelada = 4, 'Cancelada'
#     #     aguardando_compra = 5, 'Aguardando Compra'

#     __STATUS_REQUISICAO = {
#         ('aguardando_liberacao', 'Aguardando Liberação'),
#         ('aguardando_compra', 'Aguardando Compra'),
#         ('liberada', 'Liberada'),
#         ('negada', 'Negada'),
#         ('cancelada', 'Cancelada'),
#     }

#     id = models.AutoField(primary_key=True)
#     status_requisicao = models.CharField(max_length=25, choices=__STATUS_REQUISICAO, null=False)
#     # status_requisicao = models.IntegerField(choices=StatusRequisicao.choices, null=False, )
