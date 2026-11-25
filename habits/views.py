from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Habit
from .serializers import HabitSerializer
from users.permissions import IsOwnerOrReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Возвращает привычки текущего пользователя.
        Для экшена 'public' — возвращает публичные привычки всех пользователей.
        """
        user = self.request.user

        # Если это запрос к /habits/public/ — отдаем только публичные
        if self.action == 'public':
            return Habit.objects.filter(is_public=True)

        # Во всех остальных случаях (список, детали, редактирование) — только свои
        return Habit.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        При создании привычки автоматически назначаем владельца.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def public(self, request):
        """
        Кастомный эндпоинт: GET /habits/public/
        Возвращает список публичных привычек (с пагинацией).
        """
        public_habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(public_habits)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)
