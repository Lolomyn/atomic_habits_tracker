from celery import shared_task
from django.utils import timezone

from atomic_habits.models import Habit

from .services import send_telegram_message


@shared_task
def send_message_about_habit():
    habit_time = timezone.now().time().replace(microsecond=0)

    for habit in Habit.objects.all():
        if habit.time_to_start == habit_time and habit.is_due_today():

            if habit.user.tg_chat_id:
                send_telegram_message(
                    habit.user.tg_chat_id,
                    f"Привет, {habit.user.username}! Пора приступать к привычке [{habit.action}]!",
                )

            habit.last_completed = timezone.now().date()
            habit.save()
