from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Habit
from .paginators import HabitPaginator
from .permissions import IsOwner
from .serializers import HabitSerializer, PublicHabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для привычки."""

    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Задает права, при которых только владелец привычки может ее редактировать."""
        if self.action in ["update", "retrieve", "destroy"]:
            self.permission_classes = [IsOwner]

        return super().get_permissions()

    def get_queryset(self):
        """Возвращает только привычки текущего пользователя."""
        return Habit.objects.filter(user=self.request.user)


class PublicHabitViewSet(viewsets.ModelViewSet):
    """ViewSet для публичной привычки."""

    serializer_class = PublicHabitSerializer
    queryset = Habit.objects.filter(is_public=True)
