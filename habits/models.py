from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from .validators import validate_duration, validate_periodicity


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Создатель привычки',
        related_name='habits',
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место',
        help_text='Место, в котором необходимо выполнять привычку',
    )
    time = models.TimeField(
        verbose_name='Время',
        help_text='Время, когда необходимо выполнять привычку',
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Действие',
        help_text='Действие, которое представляет собой привычка',
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки',
        help_text='Приятная привычка — это вознаграждение, а не полезное действие',
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        help_text='Привычка, которая связана с другой привычкой',
        related_name='related_to',
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        validators=[validate_periodicity],
        verbose_name='Периодичность',
        help_text='Периодичность выполнения привычки для напоминания в днях',
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Вознаграждение',
        help_text='Чем пользователь должен себя вознаградить после выполнения',
    )
    duration = models.PositiveSmallIntegerField(
        validators=[validate_duration],
        verbose_name='Время на выполнение',
        help_text='Время, которое предположительно потратит пользователь на выполнение привычки (в секундах)',
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности',
        help_text='Привычки можно публиковать в общий доступ',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action} в {self.time} в {self.place}'

    def clean(self):
        super().clean()

        # 1. Нельзя одновременно указать связанную привычку и вознаграждение
        if self.related_habit and self.reward:
            raise ValidationError(
                'Нельзя одновременно указать связанную привычку и вознаграждение.'
            )

        # 2. У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                'У приятной привычки не может быть вознаграждения или связанной привычки.'
            )

        # 3. В связанные привычки могут попадать только приятные привычки
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                'Связанная привычка должна быть приятной (is_pleasant=True).'
            )
