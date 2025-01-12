from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, ProfRegistrationSerializer, LoginSerializer


class UserRegistrationAPIView(APIView):
    def post(self, request):
        print("WORKED")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"User Id is: {user.id}")
            print(f"The username is {user.username}")
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class ProfRegistrationAPIView(APIView):
    def post(self, request):
        print("WORKED")
        serializer = ProfRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            prof = serializer.save()
            print(f"Prof Id is: {prof.id}")
            print(f"The username is {prof.username}")
            return Response({"msg": "Prof registered successfully"}, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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