from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from apps.core.models import Produto, EntradaProduto, RequisicaoSaidaProduto
from apps.core.serializers import (
    ProdutoReadSerializer,
    ProdutoWriteSerializer,
    EntradaProdutoReadSerializer,
    EntradaProdutoWriteSerializer,
    RequisicaoSaidaProdutoWriteSerializer,
    RequisicaoSaidaProdutoReadSerializer,
)
from apps.core.pagination import SmallResultsSetPagination


def index(request):
    return render(request, "index.html")


# DRF
class ProdutoViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]
    queryset = Produto.objects.all()

    def get_serializer_class(self):
        if self.action == ["create", "update", "partial_update", "destroy"]:
            return ProdutoWriteSerializer
        else:
            return ProdutoReadSerializer


class EntradaProdutoViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "patch", "delete", "head"]
    queryset = EntradaProduto.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return EntradaProdutoWriteSerializer
        else:
            return EntradaProdutoReadSerializer


class RequisicaoSaidaProdutoViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "patch", "delete", "head"]
    queryset = RequisicaoSaidaProduto.objects.all()
    pagination_class = SmallResultsSetPagination

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # "create()", "retrieve()", "update()", "partial_update()", "destroy()" and "list()" actions.
            return RequisicaoSaidaProdutoWriteSerializer
        else:
            return RequisicaoSaidaProdutoReadSerializer

    def get_queryset(self):
        usuario = self.request.user
        if usuario.groups.filter(name="Administradores"):
            return RequisicaoSaidaProduto.objects.all()
        return RequisicaoSaidaProduto.objects.filter(usuario=usuario)
