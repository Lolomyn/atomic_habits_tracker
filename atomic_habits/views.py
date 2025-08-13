from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer
from .paginators import HabitPaginator
from .permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для привычки"""

    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Возвращает только привычки текущего пользователя"""
        return Habit.objects.filter(user=self.request.user)


class PublicHabitViewSet(viewsets.ModelViewSet):
    serializer_class = PublicHabitSerializer
    queryset = Habit.objects.filter(is_public=True)
