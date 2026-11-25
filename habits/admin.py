from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    # Поля, которые отображаются в общем списке привычек
    list_display = (
        'action',
        'user',
        'time',
        'place',
        'periodicity',
        'is_pleasant',
        'is_public',
    )

    # Фильтры справа (позволяют быстро находить приятные, публичные и т.д.)
    list_filter = (
        'is_pleasant',
        'is_public',
        'periodicity',
    )

    # Поиск по действию, месту и email пользователя
    search_fields = (
        'action',
        'place',
        'user__email',
    )

    # Поля, которые доступны только для чтения (создаются автоматически)
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    # Группировка полей при редактировании (чтобы не было "каши")
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Настройки привычки', {
            'fields': ('duration', 'periodicity', 'is_pleasant', 'is_public')
        }),
        ('Связи и вознаграждения', {
            'fields': ('related_habit', 'reward'),
            'description': 'Заполните только одно из полей: либо связанную привычку, либо вознаграждение.'
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Секция будет свернута по умолчанию
        }),
    )

    # Сортировка по умолчанию (сначала новые)
    ordering = ('-created_at',)

    # Количество элементов на странице
    list_per_page = 20
