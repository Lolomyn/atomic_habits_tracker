from django.urls import path

from atomic_habits.apps import AtomicHabitsConfig

from .views import HabitViewSet, PublicHabitViewSet

app_name = AtomicHabitsConfig.name

urlpatterns = [
    path("habits/create/", HabitViewSet.as_view({"post": "create"}), name="habit-create"),
    path("habits/", HabitViewSet.as_view({"get": "list"}), name="habit-list"),
    path("habits/<int:pk>/", HabitViewSet.as_view({"get": "retrieve"}), name="habit-list"),
    path("habits/<int:pk>/update/", HabitViewSet.as_view({"put": "update", "patch": "update"}), name="habit-update"),
    path("habits/<int:pk>/delete/", HabitViewSet.as_view({"delete": "destroy"}), name="habit-delete"),
    # опубликованные привычки
    path("public_habits/", PublicHabitViewSet.as_view({"get": "list"}), name="public-habit-list"),
]
