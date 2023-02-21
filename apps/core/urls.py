from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.core.views import index, ProdutoViewSet, EntradaProdutoViewSet, RequisicaoSaidaProdutoViewSet

app_name = 'core'

router = DefaultRouter()

router.register(r'produtos', ProdutoViewSet, 'produtos')
router.register(r'entrada-produto', EntradaProdutoViewSet, 'entrada-produto')
router.register(r'requisicao-saida-produto', RequisicaoSaidaProdutoViewSet, 'requisicao-saida-produto')


urlpatterns = [
    path('', include(router.urls)),
    path('core/', index, name='home')
]
