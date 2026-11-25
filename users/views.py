from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsOwnerOrReadOnly
from users.serializers import (
    UserProfilePublicSerializer,
    UserProfileSerializer,
    UserSerializer,
)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(is_active=True)


class UserProfileAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserProfileSerializer
        if self.get_object() == self.request.user:
            return UserProfileSerializer
        return UserProfilePublicSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(User, pk=pk) if pk else self.request.user
        self.check_object_permissions(self.request, obj)
        return obj
