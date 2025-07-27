from django.contrib import admin

from atomic_habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "place",
        "time_to_start",
        "action",
        "action_description",
        "is_pleasant_habit",
        "related_habit",
        "periodicity",
        "award",
        "duration",
        "is_public",
    )
    list_filter = ("action", "periodicity", "is_public")
    search_fields = ("action",)
