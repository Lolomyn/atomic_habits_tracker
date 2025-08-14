from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель привычки"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор привычки",
    )

    place = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Место выполнения привычки",
        help_text="Укажите место выполнения привычки",
    )

    time_to_start = models.TimeField(
        verbose_name="Время выполнения привычки",
        help_text="Укажите время выполнения привычки",
    )

    action = models.CharField(
        max_length=120, verbose_name="Действие", help_text="Укажите действие, которое представляет из себя привычка"
    )

    action_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание действия",
        help_text="Укажите подробнее о действии, которое представляет из себя привычка",
    )

    is_pleasant_habit = models.BooleanField(verbose_name="Приятная привычка")

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="related_habits",
        verbose_name="Связанная привычка",
        help_text="Укажите привычку, связанную с полезной привычкой",
    )

    PERIODICITY_CHOICES = [
        (1, "1 день"),
        (2, "2 дня"),
        (3, "3 дня"),
        (4, "4 дня"),
        (5, "5 дней"),
        (6, "6 дней"),
    ]

    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        verbose_name="Периодичность в днях",
        help_text="Укажите периодичность выполнения привычки в днях",
    )

    award = models.TextField(
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
    )

    duration = models.IntegerField(
        verbose_name="Время выполнения привычки",
        help_text="Укажите время выполнения привычки",
    )

    is_public = models.BooleanField(verbose_name="Опубликовать")

    def __str__(self):
        """Строковое представление модели."""
        return f"{self.action} / Периодичность (дней): {self.periodicity}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["action"]
