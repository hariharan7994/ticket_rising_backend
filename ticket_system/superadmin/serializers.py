from rest_framework import serializers
from django.contrib.auth import authenticate

class SuperAdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError({"non_field_errors": ["Both username and password are required"]})

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({"non_field_errors": ["Invalid username or password"]})

        if not user.is_superuser:
            raise serializers.ValidationError({"non_field_errors": ["You are not a super admin"]})

        data["user"] = user
        return data
