from django.urls import path
from .views import *

urlpatterns = [
    path("students/",StudentAPIView.as_view()),
]
