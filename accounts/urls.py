from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, MeView, UpdateProfileView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),
    path('update/', UpdateProfileView.as_view(), name='update-profile'),
]
