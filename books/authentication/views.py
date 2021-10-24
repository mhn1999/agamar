from rest_framework.views import APIView
from .serializer import CustomUserSerializer
from rest_framework.response import Response

class RegisterView(APIView):
    def post(self,request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data})


class LoginView(APIView):
    def post(self, request):
        pass