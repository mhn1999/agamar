from rest_framework.views import APIView
from .serializer import CustomUserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
from rest_framework import status
from rest_framework.generics import GenericAPIView


class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data},status=status.HTTP_201_CREATED)


class LogoutView(GenericAPIView):
    def post(self, request, *args):
        pass

'''
class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = CustomUser.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        return Response({"message": "You successfully logged in"}, status=status.HTTP_200_OK)
'''

