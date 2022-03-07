from django.urls import path
from .views import *

urlpatterns = [
    # APIView
    path("students/", StudentAPIView.as_view()),
    path("students/<int:pk>", StudentInfoView.as_view()),

    # GenericAPIView
    path("students2/",StudentGenericAPIView.as_view()),
    path("students2/<int:pk>", StudentInfoGenericApiView.as_view()),
]
