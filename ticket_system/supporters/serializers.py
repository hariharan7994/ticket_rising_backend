from rest_framework import serializers
from django.contrib.auth import authenticate
from superadmin.models import User, Supporter, Designation

# -------- Supporter Serializer -------- #
class SupporterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Supporter
        fields = ["username", "email", "phone_number", "designation"]


# -------- Supporter Register Serializer (SuperAdmin creates supporter) -------- #
class SupporterRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Supporter
        fields = ["username", "email", "password", "phone_number", "designation"]

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # Create User first
        user = User.objects.create_user(
            username=username, email=email, password=password, is_supporter=True
        )

        # Create Supporter profile
        supporter = Supporter.objects.create(user=user, **validated_data)
        return supporter


# -------- Supporter Login Serializer -------- #
class SupporterLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_supporter:
            raise serializers.ValidationError("User is not a supporter")
        data["user"] = user
        return data

#=====================get supporters=====================#
class SupporterDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Supporter
        fields = ["id", "username", "email", "phone_number", "designation"]




class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ["id", "name"]