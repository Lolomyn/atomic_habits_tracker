from rest_framework import serializers, viewsets

from .models import Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для привычки"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
