from abc import ABC

from rest_framework import serializers
from .models import CustomUser
from django.utils.text import gettext_lazy
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'name', 'phone_number', 'address',
                  'is_private_person', 'is_book_store']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class RefreshTokenSerializer(serializers.Serializer, ABC):
    pass
