from django.contrib import admin

from apps.core.models import RequisicaoSaidaProduto, ItemSaidaProduto, Produto, Estoque, EntradaProduto


# PRODUTO
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_produto', 'codigo_produto', 'preco_entrada', 'estoque_minimo', 'estoque_maximo',)
    list_display_links = ('id', 'nome_produto',)


# ENTRADA
@admin.register(EntradaProduto)
class EntradaProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao_entrada', 'produto', 'quantidade',)
    list_display_links = ('id', 'descricao_entrada',)


# ESTOQUE
@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto_nome', 'produto_codigo', 'quantidade', 'estoque_minimo', 'estoque_maximo',)
    list_display_links = ('id', 'produto_nome',)


# SAIDA
class ItemSaidaProdutoInline(admin.TabularInline):
    model = ItemSaidaProduto
    extra = 0  # how many rows to show


@admin.register(RequisicaoSaidaProduto)
class RequisicaoSaidaProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descricao_saida', 'status_requisicao',)
    list_display_links = ('id', 'descricao_saida')
    inlines = (ItemSaidaProdutoInline,)

    # def itens(self, obj):
    #     return "\n".join([p.itens for p in obj.item.all()])


# @admin.register(ItemSaidaProduto)
# class ItemSaidaProdutoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'compra', 'produto', 'quantidade',)
#     list_display_links = ('id', 'compra', 'produto', 'quantidade',)
#     # inlines = (RequisicaoSaidaProdutoItemSaidaProdutoInline,)
