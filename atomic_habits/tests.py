from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from atomic_habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тестирование CRUD операций объекта Привычка."""

    def setUp(self) -> None:
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
            tg_chat_id=367881716
        )

        self.habit = Habit.objects.create(
            user=1,
            time_to_start='12:00:00',
            action='test',
            is_pleasant_habit=False,
            periodicity=1,
            duration=1,
            is_public=False
        )

    def test_create_habit(self):
        """Тестирование создания объекта Привычка."""
        data = {

        }
