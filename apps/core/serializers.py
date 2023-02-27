from apps.core.models import (
    Produto,
    EntradaProduto,
    RequisicaoSaidaProduto,
    ItemSaidaProduto,
)
from rest_framework import serializers

# from drf_writable_nested import WritableNestedModelSerializer


class ProdutoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"
        depth = 1


class ProdutoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"


class EntradaProdutoReadSerializer(serializers.ModelSerializer):
    produto = serializers.CharField(source="produto.nome_produto")

    class Meta:
        model = EntradaProduto
        fields = "__all__"
        depth = 1


class EntradaProdutoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaProduto
        fields = "__all__"


# Serializers Saida
class ItemSaidaProdutoReadSerializer(serializers.ModelSerializer):
    produto = serializers.CharField(source="produto.nome_produto")
    quantidade = serializers.IntegerField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = ItemSaidaProduto
        fields = (
            "produto",
            "quantidade",
            "total",
        )

    def get_total(self, instance):
        return instance.quantidade * instance.produto.preco_entrada


class RequisicaoSaidaProdutoReadSerializer(serializers.ModelSerializer):
    status_requisicao = serializers.SerializerMethodField()
    descricao_saida = serializers.CharField()
    usuario = serializers.CharField(source="usuario.email")

    # produto = serializers.CharField(many= ,read_only=True, view_name='core:produtos-detail')

    itens = ItemSaidaProdutoReadSerializer(
        many=True
    )  # está associando pelo related_name: itens

    class Meta:
        model = RequisicaoSaidaProduto
        fields = (
            "id",
            "usuario",
            "descricao_saida",
            "status_requisicao",
            "itens",
            "resumo_total",
        )
        depth = 1

    def get_status_requisicao(self, instance):
        return instance.get_status_requisicao_display()


# CRIAÇÃO REQUISICAO SAIDA PRODUTO
class ItemSaidaProdutoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSaidaProduto
        fields = (
            "produto",
            "quantidade",
        )

    def validate(self, data):
        for i in data:
            if data["quantidade"] > data["produto"].estoque_maximo:
                raise serializers.ValidationError(
                    {
                        "msg": f"Quantidade solicitada para o produto {data['produto'].nome_produto} \
                            não disponível em estoque."
                    }
                )
        return data


# class RequisicaoSaidaProdutoWriteSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
class RequisicaoSaidaProdutoWriteSerializer(serializers.ModelSerializer):
    itens = ItemSaidaProdutoWriteSerializer(
        many=True
    )  # está associando pelo related_name: itens

    # Caso no request não venha o usuario, será usado o usuário autenticado
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = RequisicaoSaidaProduto
        fields = (
            "id",
            "descricao_saida",
            "usuario",
            "itens",
        )

    # OBS: Lib "drf_writable_nested" tem como proposta não precisar o método create e update

    def create(self, validated_data):
        itens = validated_data.pop("itens")

        compra = RequisicaoSaidaProduto.objects.create(**validated_data)
        for item in itens:
            ItemSaidaProduto.objects.create(compra=compra, **item)
        return compra

    def update(self, instance, validated_data):
        itens = validated_data.pop("itens")
        instance.descricao_saida = validated_data.get(
            "descricao_saida", instance.descricao_saida
        )

        if itens:
            instance.itens.all().delete()
            for item in itens:
                ItemSaidaProduto.objects.create(compra=instance, **item)
            instance.save()
        return instance
