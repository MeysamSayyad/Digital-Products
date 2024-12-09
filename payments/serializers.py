from rest_framework import serializers
from .models import Gateway, Payment
from users.serializers import UserSerializer
from subscriptions.serializers import PackageSerializer


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ["title", "is_enable", "description", "avatar"]


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    package = PackageSerializer()
    gateway = GatewaySerializer()

    class Meta:
        model = Payment
        fields = [
            "user",
            "package",
            "gateway",
            "price",
            "status",
            "token",
            "phone_number",
            "consumed_code",
        ]
