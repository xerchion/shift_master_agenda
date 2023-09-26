from django.contrib.auth.models import User
from rest_framework import serializers

# from loto.models import Player


class RankingSerializer(serializers.Serializer):
    name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    id = serializers.IntegerField()


class BetsSerializer(serializers.Serializer):
    nacional = serializers.IntegerField()
    primitiva = serializers.ListField(child=serializers.CharField())
    euromillones = serializers.ListField(child=serializers.CharField())


class TurnsSerializer(serializers.Serializer):
    last = serializers.CharField()
    current = serializers.CharField()
    next = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]  # Ajusta los campos según tus necesidades


class UserSerializaer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    firs_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validate_data):
        instance = User()
        instance.first_name = validate_data.get("first_name")
        instance.last_name = validate_data.get("last_name")
        instance.username = validate_data.get("username")
        instance.email = validate_data.get("email")
        instance.set_password(validate_data.get("password"))
        instance.save()
        return instance

    def validate_username(sef, data):
        users = User.objects.filter(username=data)
        if len(users) != 0:
            raise serializers.ValidationError("Est usuario ya existe")
        else:
            return data
