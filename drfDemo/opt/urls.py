from django.urls import path
from .views import *

urlpatterns = [
    path("example/", Example.as_view()),
    path("home/", HomeVPIView.as_view()),
    path("homeinfo/", HomeInfoAPIView.as_view()),
    path("studentinfo/<int:pk>", StudentInfoApiView.as_view()),

    # 限流
    path("demo1/", Demo1ApiView.as_view()),
    path("demo2/", Demo2ApiView.as_view()),
    path("demo3/", Demo3ApiView.as_view()),

]
