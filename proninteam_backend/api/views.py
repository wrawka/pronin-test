from rest_framework import viewsets, permissions

from service.models import Collection, Payment
from api.serializers import (
    CollectionSerializer,
    PaymentSerializer,
    CollectionCreateSerializer,
    PaymentCreateSerializer,
)


class CollectionViewSet(viewsets.ModelViewSet):
    """Сборы."""

    queryset = Collection.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CollectionCreateSerializer
        return CollectionSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Донаты."""

    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PaymentCreateSerializer
        return PaymentSerializer
