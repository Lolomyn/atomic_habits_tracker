from rest_framework import viewsets

from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer
from .paginators import HabitPaginator


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator


class PublicHabitViewSet(viewsets.ModelViewSet):
    serializer_class = PublicHabitSerializer
    queryset = Habit.objects.filter(is_public=True)
