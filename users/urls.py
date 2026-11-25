from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserCreateAPIView, UserProfileAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile-detail'),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
]
