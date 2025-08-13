from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("habits/", include("atomic_habits.urls", namespace="atomic_habits")),
]
