from rest_framework import viewsets

from .models import Habit
from .serializers import HabitSerializer
from .paginators import PageNumberPagination


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = PageNumberPagination
