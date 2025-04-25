from rest_framework import viewsets, permissions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from service.models import Collection, Payment
from api.serializers import (
    CollectionSerializer,
    PaymentSerializer,
    CollectionCreateSerializer,
    PaymentCreateSerializer,
)

CACHE_LIFETIME = 60 * 5  # 5 minutes


class CollectionViewSet(viewsets.ModelViewSet):
    """Сборы."""

    queryset = Collection.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["author", "cause"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CollectionCreateSerializer
        return CollectionSerializer

    @method_decorator(cache_page(CACHE_LIFETIME, cache="api"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_LIFETIME, cache="api"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    """Донаты."""

    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["collection", "user"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PaymentCreateSerializer
        return PaymentSerializer

    @method_decorator(cache_page(CACHE_LIFETIME, cache="api"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_LIFETIME, cache="api"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
