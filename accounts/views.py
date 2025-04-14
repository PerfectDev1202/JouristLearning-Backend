# accounts/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, UserUpdateSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
