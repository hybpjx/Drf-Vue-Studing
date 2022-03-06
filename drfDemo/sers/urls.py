from django.conf.urls import re_path
from django.urls import path
from .views import *

urlpatterns=[
    path("seri1/",StuSeriApiView.as_view()),
    path("seri2/",StudentView.as_view())

]