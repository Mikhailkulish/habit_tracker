from django.core.exceptions import ValidationError


def validate_duration(value):
    """Время выполнения должно быть не больше 120 секунд."""
    if value > 120:
        raise ValidationError('Время выполнения не должно превышать 120 секунд.')


def validate_periodicity(value):
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""
    if value < 1 or value > 7:
        raise ValidationError('Периодичность должна быть от 1 до 7 дней.')
