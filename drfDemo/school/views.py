from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializers import StudentModelSerializers


class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializers


