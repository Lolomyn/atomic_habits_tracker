from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("atomic_habits.urls", namespace="atomic_habits")),
    path("", include("users.urls", namespace="users")),
]
