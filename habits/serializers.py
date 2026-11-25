from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        # 1. Исключить одновременный выбор связанной привычки и вознаграждения
        if data.get('related_habit') and data.get('reward'):
            raise serializers.ValidationError(
                'Нельзя одновременно указать связанную привычку и вознаграждение.'
            )

        # 2. Время выполнения не больше 120 секунд
        if data.get('duration') and data['duration'] > 120:
            raise serializers.ValidationError(
                'Время выполнения не должно превышать 120 секунд.'
            )

        # 3. В связанные привычки могут попадать только приятные привычки
        related_habit = data.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                'Связанная привычка должна иметь признак приятной (is_pleasant=True).'
            )

        # 4. У приятной привычки не может быть вознаграждения или связанной привычки
        if data.get('is_pleasant'):
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть вознаграждения или связанной привычки.'
                )

        # 5. Нельзя выполнять привычку реже, чем 1 раз в 7 дней
        periodicity = data.get('periodicity')
        if periodicity and (periodicity < 1 or periodicity > 7):
            raise serializers.ValidationError(
                'Периодичность должна быть от 1 до 7 дней.'
            )

        return data
