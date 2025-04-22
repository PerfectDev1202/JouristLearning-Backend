from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, MeView, UpdateProfileView, resend_verification, verify_email, forgot_password, reset_password, jwt_login, change_password, delete_account, NotificationSettingsView

urlpatterns = [
    path('login/', jwt_login, name='jwt_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),
    path('update/', UpdateProfileView.as_view(), name='update-profile'),
    path('resend-verification/', resend_verification, name='resend-verification'),
    path('verify-email/', verify_email, name='verify-email'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('reset-password/', reset_password, name='reset-password'),
    path('change-password/', change_password, name='change-password'),
    path('delete-me/', delete_account, name='delete-account'),
    path('notification-settings/', NotificationSettingsView.as_view(), name='notification-settings'),
]
