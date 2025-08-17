from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки"""

    def validate(self, data):
        award = data.get("award")
        related_habit = data.get("related_habit")
        duration = data.get("duration")
        is_pleasant_habit = data.get("is_pleasant_habit")

        if is_pleasant_habit:
            if award:
                raise serializers.ValidationError(
                    {
                        "award": ["У приятной привычки не может быть вознаграждения"],
                    }
                )
            if related_habit:
                raise serializers.ValidationError(
                    {
                        "related_habit": ["У приятной привычки не может быть связанной привычки"],
                    }
                )

        if related_habit:
            if not related_habit.is_pleasant_habit:
                raise serializers.ValidationError(
                    {
                        "related_habit": [
                            "В связанные привычки могут попадать только привычки с признаком приятной привычки"
                        ],
                    }
                )

        if award and related_habit:
            raise serializers.ValidationError(
                {
                    "award": ["Нельзя указывать одновременно с связанной привычкой"],
                    "related_habit": ["Нельзя указывать одновременно с вознаграждением"],
                }
            )

        if duration > 120:
            raise serializers.ValidationError(
                {
                    "duration": ["Время выполнения должно быть не больше 120 секунд"],
                }
            )

        return data

    class Meta:
        model = Habit
        exclude = ['user']


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор публичной привычки"""

    class Meta:
        model = Habit
        exclude = ["id", "is_public"]
