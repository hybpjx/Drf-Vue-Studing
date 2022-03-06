from django.urls import path
from .views import *

urlpatterns = [
    path("studentView/",StudentView.as_view(),name="studentView"),
    path("student/",StudentApiView.as_view(),name="student")
]
