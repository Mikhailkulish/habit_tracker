from django.urls import path

from users.views import UserCreateAPIView, UserProfileAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile-detail'),
]
