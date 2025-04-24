from rest_framework import serializers

from service.models import Collection, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["amount", "user", "collection", "is_hidden"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class PaymentPreviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.get_full_name", label="Донатер")
    visible_amount = serializers.SerializerMethodField(label="Сумма")

    class Meta:
        model = Payment
        fields = ["id", "user", "visible_amount", "date"]
        read_only_fields = ["id", "user", "visible_amount", "date"]

    def get_visible_amount(self, obj):
        if obj.is_hidden:
            return "Скрыто"
        return obj.amount


class CollectionSerializer(serializers.ModelSerializer):
    participant_count = serializers.ReadOnlyField(label="Количество участников")
    current_amount = serializers.ReadOnlyField(label="Собрано")
    payments = PaymentPreviewSerializer(many=True, read_only=True)

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
