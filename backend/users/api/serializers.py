from django.contrib.auth import get_user_model
from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]
