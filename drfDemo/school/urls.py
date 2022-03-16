from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("students", StudentModelViewSet, basename="students")

urlpatterns = [
              ] + router.urls
