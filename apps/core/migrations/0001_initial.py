# Generated by Django 4.1.6 on 2023-02-20 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Estoque",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("produto_nome", models.CharField(max_length=50)),
                ("produto_codigo", models.CharField(max_length=20)),
                ("quantidade", models.IntegerField()),
                ("estoque_minimo", models.IntegerField()),
                ("estoque_maximo", models.IntegerField()),
            ],
            options={
                "verbose_name": "estoque",
                "verbose_name_plural": "estoques",
            },
        ),
        migrations.CreateModel(
            name="Produto",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nome_produto", models.CharField(max_length=50)),
                ("codigo_produto", models.CharField(max_length=20)),
                ("estoque_minimo", models.IntegerField()),
                ("estoque_maximo", models.IntegerField()),
            ],
            options={
                "verbose_name": "produto",
                "verbose_name_plural": "produtos",
            },
        ),
        migrations.CreateModel(
            name="RequisicaoSaidaProduto",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("descricao_saida", models.CharField(max_length=50)),
                (
                    "status_requisicao",
                    models.CharField(
                        choices=[
                            ("aguardando_compra", "Aguardando Compra"),
                            ("negada", "Negada"),
                            ("aguardando_liberacao", "Aguardando Liberação"),
                            ("liberada", "Liberada"),
                            ("cancelada", "Cancelada"),
                        ],
                        max_length=25,
                    ),
                ),
            ],
            options={
                "verbose_name": "Requisicao Saida",
                "verbose_name_plural": "Requisicoes Saida",
            },
        ),
        migrations.CreateModel(
            name="ItemSaidaProduto",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("quantidade", models.IntegerField()),
                (
                    "compra",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itens",
                        to="core.requisicaosaidaproduto",
                    ),
                ),
                (
                    "produto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="produtos",
                        to="core.produto",
                    ),
                ),
            ],
            options={
                "verbose_name": "Item Saida",
                "verbose_name_plural": "Item Saida",
            },
        ),
        migrations.CreateModel(
            name="EntradaProduto",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("descricao_entrada", models.CharField(max_length=50)),
                ("quantidade", models.IntegerField()),
                (
                    "produto",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.produto",
                    ),
                ),
            ],
            options={
                "verbose_name": "Entrada Produto",
                "verbose_name_plural": "Entrada Produto",
            },
        ),
    ]
