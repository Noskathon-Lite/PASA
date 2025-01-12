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


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print(f"Logged in as: {user.username}")
            #print(f"ATTRIBUTES: {user.__dict__}") To get all attributes of an object.
            return Response({
                "msg": "Login successful",
                "username": user.username,
                "userType": "Prof" if (user.user_type == "prof") else "User"
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'msg': 'Invalid Username or password',
                'error': serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST
                )