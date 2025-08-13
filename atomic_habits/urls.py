from django.urls import path
from atomic_habits.apps import AtomicHabitsConfig

from .views import HabitViewSet

app_name = AtomicHabitsConfig.name

urlpatterns = [
    path("create/", HabitViewSet.as_view({"post": "create"}), name="habit-create"),
    path("", HabitViewSet.as_view({"get": "list"}), name="habit-list"),
    path("<int:pk>/", HabitViewSet.as_view({"get": "retrieve"}), name="habit-list"),
    path("<int:pk>/update/", HabitViewSet.as_view({"put": "update", "patch": "update"}), name="habit-update"),
    path("<int:pk>/delete/", HabitViewSet.as_view({"delete": "destroy"}), name="habit-delete"),
]
