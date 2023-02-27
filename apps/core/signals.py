from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import RequisicaoSaidaProduto


@receiver(post_save, sender=RequisicaoSaidaProduto)
def enviar_msg(sender, instance, created, **kargs):
    # sender = Model que está sendo observando
    # instance = Instância do momento. Objeto em si
    # created = Boolean que retornar True caso algo esteja sendo criado
    # **kargs = Recebe dict com outros argumentos
    if created:
        produtos = instance.itens.all()
        for item in produtos:
            print(item)
            print(f"Requisição: {instance} com os produto(s) {item} criada co sucesso.")


@receiver(post_save, sender=RequisicaoSaidaProduto)
def my_callback(sender, **kwargs):
    print("Setting changed!")

    # importa determinados arquivos que são necessários serem carregados
    # antes do acesso a app.
    # def ready(self):
    #     post_save.connect(enviar_msg, sender=RequisicaoSaidaProduto)
