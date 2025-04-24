from rest_framework import serializers

from service.models import Collection, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["amount", "user", "collection"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class CollectionSerializer(serializers.ModelSerializer):
    participant_count = serializers.ReadOnlyField(label="Количество участников")
    current_amount = serializers.ReadOnlyField(label="Собрано")

    class Meta:
        model = Collection
        fields = "__all__"


class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["name", "cause", "description", "author"]
        read_only_fields = ["author"]

    def create(self, validated_data):
        author = self.context["request"].user
        validated_data["author"] = author
        return super().create(validated_data)
