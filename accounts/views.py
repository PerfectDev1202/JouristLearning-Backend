# accounts/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, NotificationSettings
from .serializers import RegisterSerializer, UserSerializer, UserUpdateSerializer, NotificationSettingsSerializer   
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .utils import send_verification_email, send_forgot_password_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        me = {
            "id": serializer.data.get("id"),
            "email": serializer.data.get("email"),
            "full_name": serializer.data.get("full_name"),
            "is_verified": serializer.data.get("is_verified"),
            "is_premium": serializer.data.get("is_premium"),
            "avatar": serializer.data.get("avatar"),
            "country": serializer.data.get("country"),
            "city": serializer.data.get("city"),
            "primary_language": serializer.data.get("primary_language"),
            "foreign_language": serializer.data.get("foreign_language"),
            "ui_language": serializer.data.get("ui_language"),
            "role": serializer.data.get("role"),
            "date_joined": serializer.data.get("date_joined"),
            "last_login": serializer.data.get("last_login"),
        }
        return Response(me)

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class NotificationSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        settings, _ = NotificationSettings.objects.get_or_create(user=self.request.user)
        return settings

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get("current_password")
    new_password = request.data.get("new_password")

    if not current_password or not new_password:
        return Response({"detail": "Both current and new password are required."}, status=400)

    if not user.check_password(current_password):
        return Response({"detail": "Current password is incorrect."}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"detail": "Password changed successfully."}, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response({"detail": "Account deleted successfully."}, status=204)

@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"detail": "Email and password are required."}, status=400)

    user = authenticate(request, email=email, password=password)

    if user is None:
        return Response({"detail": "Invalid credentials."}, status=401)

    user.last_login = now()
    user.save(update_fields=['last_login'])

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=200)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)

        if not user:
            return Response({"error": "User not found."}, status=404)

        if user.is_verified:
            return Response({"error": "User already verified."}, status=400)

        send_verification_email(user)
        return Response({"message": "Verification email sent."})

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    email = request.data.get('email')
    token = request.data.get('token')

    try:
        user = User.objects.get(email=email)
        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            return Response({"message": "Email verified successfully."})
        else:
            return Response({"error": "Invalid or expired token."}, status=400)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)

        if not user:
            return Response({"error": "User not found."}, status=404)

        send_forgot_password_email(user)
        return Response({"message": "Forgot password email sent."})
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

@api_view(['POST']) 
@permission_classes([AllowAny])
def reset_password(request):
    token = request.data.get('token')
    password = request.data.get('password')

    if not token or not password:
        return Response({"detail": "Token and password are required."}, status=400)
    try:
        uidb64, token_str = token.split(":")
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"detail": "Invalid or expired token."}, status=400)

    if not default_token_generator.check_token(user, token_str):
        return Response({"detail": "Invalid or expired token."}, status=400)

    user.set_password(password)
    user.save()

    return Response({"detail": "Password has been reset successfully."}, status=200)
    
