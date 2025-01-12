from rest_framework import serializers
from .models import User, Prof
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'fullname']
    def create(self, validated_data):
        print("User Serializer")
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname']
        )
        return user


class ProfRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Prof
        fields = ['username', 'email', 'password', 'fullname']
    def create(self, validated_data):
        print("Prof Serializer")
        prof = Prof.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname'],
            user_type = 'prof'
        )
        return prof
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        print("Login serializer")
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        data['user'] = user
        return data


class UserAnswerSubmitSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    answers = serializers.ListField(
        child=serializers.CharField(),
        min_length=10,
        max_length=10,
        help_text="A list of 10 answers."
    )


class ProfAnswerSubmitSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    answers = serializers.ListField(
        child=serializers.CharField(),
        min_length=10,
        max_length=10,
        help_text="A list of 10 answers."
    )