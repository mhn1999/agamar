from re import U
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializer import CustomUserSerializer, UserInfoSerializer, UserUpdateInfoSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
from rest_framework import permissions, status, generics
from rest_framework.generics import GenericAPIView
from .serializer import RefreshTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['GET'])
def userList(request):
	user = CustomUser.objects.all().order_by('-id')
	serializer = CustomUserSerializer(user, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def userDetail(request, pk):
	user = CustomUser.objects.get(id=pk)
	serializer = CustomUserSerializer(user, many=False)
	return Response(serializer.data)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data},status=status.HTTP_201_CREATED)


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserInfoView(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request, *args):
        user = request.user
        serializer = UserInfoSerializer(user, many=False)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)


class UserUpdateInfoView(APIView):
    permissions = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def patch(self, request):
        user = request.user
        serializer = UserUpdateInfoSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_205_RESET_CONTENT)


class ChangePasswordView(generics.UpdateAPIView):
    permissions = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(user, request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_205_RESET_CONTENT)

'''
class UpdateImageView(APIView):
    permissions = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user
        file = request.data.get('file')
        serializer = UpdateImageSerializer(user, data={'file': file})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_205_RESET_CONTENT)

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

