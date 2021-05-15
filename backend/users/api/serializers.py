from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserWriteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all(), message="Username already exists.")],
        label="username",
    )
    password = serializers.CharField(required=True, write_only=True, min_length=9, label="password")

    registration_token = serializers.CharField(label="registration_token", read_only=True)
    token = TokenObtainPairSerializer(read_only=True, label="token")

    class Meta:
        model = get_user_model()
        fields = ["username", "registration_token", "password", "token"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user

    def validate_registration_token(self, token):
        if token is None or token == "":
            raise serializers.ValidationError("registration token is required.")

        if token == "correct":
            return token

        raise serializers.ValidationError("Invalid registration token.")


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username"]


class UserListSerializer(serializers.Serializer):
    users = serializers.SerializerMethodField()

    def get_users(self, _instance):
        return [{"username": user.username} for user in self.instance]

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(label="old password", required=True, write_only=True)
    new_password = serializers.CharField(label="new password", min_length=9, required=True, write_only=True)
    new_password_confirmation = serializers.CharField(
        label="new password confirmation", min_length=9, required=True, write_only=True
    )

    def validate_old_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Failed to change password")
        else:
            return value

    def validate(self, data):
        validated = super().validate(data)

        if data["new_password"] != data["new_password_confirmation"]:
            raise serializers.ValidationError("New passwords do not match.")
        else:
            return validated

    def update(self, instance, validated_data):
        user = self.context["request"].user

        user.set_password(validated_data["new_password"])
        user.save()

        return user

    def create(self, validated_data):
        pass
