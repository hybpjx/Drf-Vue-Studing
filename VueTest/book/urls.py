from django.urls import path
from .views import *

urlpatterns = [
    path("index/",IndexView.as_view(),name="index"),
    path("book/",BookView.as_view(),name="book")
]
