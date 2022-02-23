
from django.contrib import admin
from django.urls import path

from students.views import StudentView

urlpatterns = [
    path("student/",StudentView.as_view())
]
