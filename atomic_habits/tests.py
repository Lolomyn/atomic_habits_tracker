from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from atomic_habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тестирование CRUD операций объекта Привычка."""

    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.com", username="test", password="test", tg_chat_id=367881716)

        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            time_to_start="12:00:00",
            action="test",
            is_pleasant_habit=False,
            periodicity=2,
            duration=1,
            is_public=False,
        )

        self.public_habit = Habit.objects.create(
            user=self.user,
            time_to_start="12:00:00",
            action="Скушать яблоко",
            is_pleasant_habit=True,
            periodicity=1,
            duration=1,
            is_public=True,
        )

    def test_create_habit(self):
        """Тестирование создания объекта Привычка."""
        data = {
            "user": 1,
            "time_to_start": "07:00:00",
            "action": "Почистить зубы",
            "is_pleasant_habit": False,
            "periodicity": 1,
            "duration": 1,
            "is_public": True,
        }

        response = self.client.post("/habits/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

    def test_str_method(self):
        """Тестирование строкового представления модели."""
        self.assertEqual(str(self.habit), "test / Периодичность (дней): 2")

    def test_create_habit_no_auth(self):
        """Тестирование создания объекта Привычка без авторизации."""
        self.client.logout()

        data = {
            "user": 1,
            "time_to_start": "07:00:00",
            "action": "Почистить зубы",
            "is_pleasant_habit": False,
            "periodicity": 1,
            "duration": 1,
            "is_public": True,
        }

        response = self.client.post("/habits/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_list_habits(self):
        """Тестирование просмотра объекта Привычка."""
        response = self.client.get("/habits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results", response.data)), 2)
        self.assertEqual(response.data.get("results", response.data)[0]["action"], "test")

    def test_list_habits_no_auth(self):
        """Тестирование просмотра объекта Привычка без авторизации."""
        self.client.logout()

        response = self.client.get("/habits/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_public_habits(self):
        """Тестирование просмотра объекта Публичная привычка."""
        response = self.client.get("/public_habits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["action"], "Скушать яблоко")

    def test_list_public_habits_no_auth(self):
        """Тестирование просмотра объекта Публичная привычка без авторизации."""
        self.client.logout()

        response = self.client.get("/public_habits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["action"], "Скушать яблоко")

    def test_update_habit(self):
        """Тестирование обновления объекта Привычка."""
        update_data = {
            "user": self.habit.user.id,
            "action": "test update",
            "duration": self.habit.duration,
            "time_to_start": self.habit.time_to_start,
            "is_pleasant_habit": self.habit.is_pleasant_habit,
            "is_public": self.habit.is_public,
        }

        response = self.client.patch(
            reverse("atomic_habits:habit-update", kwargs={"pk": self.habit.pk}),
            data=update_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "test update")

    def test_delete_habit(self):
        """Тестирование удаления объекта Привычка."""
        response = self.client.delete(
            reverse("atomic_habits:habit-delete", kwargs={"pk": self.habit.id}),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_validator_pleasant_habit__award(self):
        """Тестирование валидации поля is_pleasant_habit при создании объекта Привычка."""
        data = {
            "user": self.habit.user.id,
            "time_to_start": "07:00:00",
            "action": "Почистить зубы",
            "is_pleasant_habit": True,
            "award": "award",
            "periodicity": 1,
            "duration": 1,
            "is_public": True,
        }

        response = self.client.post("/habits/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["award"][0], "У приятной привычки не может быть вознаграждения")

    def test_validator_pleasant_habit__related_habit(self):
        """Тестирование валидации поля is_pleasant_habit при создании объекта Привычка."""
        data = {
            "user": self.habit.user.id,
            "time_to_start": "07:00:00",
            "action": "Почистить зубы",
            "is_pleasant_habit": True,
            "related_habit": self.habit.id,
            "periodicity": 1,
            "duration": 1,
            "is_public": True,
        }

        response = self.client.post("/habits/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["related_habit"][0], "У приятной привычки не может быть связанной привычки")

    def test_validator_related_habit(self):
        """Тестирование валидации поля related_habit при создании объекта Привычка."""
        data = {
            "user": self.habit.user.id,
            "time_to_start": "07:00:00",
            "action": "Почистить зубы",
            "is_pleasant_habit": False,
            "related_habit": self.habit.id,
            "periodicity": 1,
            "duration": 1,
            "is_public": True,
        }

        response = self.client.post("/habits/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["related_habit"][0],
            "В связанные привычки могут попадать только привычки с признаком приятной привычки",
        )

    def test_validator_related_habit__award(self):
        """Тестирование валидации полей related_habit и award при создании объекта Привычка."""
        data = {
            "user": self.habit.user.id,
            "time_to_start": "07:00:00",
            "action": "Почистить зубы",
            "is_pleasant_habit": False,
            "award": "award",
            "related_habit": self.public_habit.id,
            "periodicity": 1,
            "duration": 1,
            "is_public": True,
        }

        response = self.client.post("/habits/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["award"][0], "Нельзя указывать одновременно с связанной привычкой")
        self.assertEqual(response.data["related_habit"][0], "Нельзя указывать одновременно с вознаграждением")

    def test_validator_duration(self):
        """Тестирование валидации поля duration при создании объекта Привычка."""
        data = {
            "user": self.habit.user.id,
            "time_to_start": "07:00:00",
            "action": "Почистить зубы",
            "is_pleasant_habit": True,
            "periodicity": 1,
            "duration": 121,
            "is_public": True,
        }

        response = self.client.post("/habits/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["duration"][0], "Время выполнения должно быть не больше 120 секунд")

    def test_is_due_today_no_lat_completed(self):
        """Тестирование, когда привычка еще ни разу не выполнялась"""
        self.habit.last_completed = None
        self.assertTrue(self.habit.is_due_today())

    def test_is_due_today(self):
        """Тестирование, когда привычку нужно выполнить сегодня"""
        self.habit.last_completed = timezone.now().date() - timedelta(days=2)
        self.assertTrue(self.habit.is_due_today())

    def test_is_due_today_not_today(self):
        """Тестирование, когда привычку не нужно выполнять сегодня"""
        self.habit.last_completed = timezone.now().date() - timedelta(days=1)
        self.assertFalse(self.habit.is_due_today())

    def test_is_due_today_time_periodicity(self):
        """Тестирование, когда время сравнивается с периодичностью"""
        self.habit.last_completed = timezone.now().date() - timedelta(days=self.habit.periodicity)
        self.assertTrue(self.habit.is_due_today())


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.com", username="test", password="test", tg_chat_id=367881716)

    def test_user_create(self):
        data = {
            "email": "test_email@yandex.ru",
            "username": "test_username",
            "password": "test_pswd",
        }

        response = self.client.post("/register/", data=data)
        self.assertEqual(response.data.get("username"), "test_username")
