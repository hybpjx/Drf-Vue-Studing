from rest_framework.viewsets import ModelViewSet
# Create your views here.
from students.models import Student
from .serializers import StuApiModelSerializers


class StuApiViewSet(ModelViewSet):
    """
    展示所有学生信息
    """
    queryset = Student.objects.all()
    serializer_class = StuApiModelSerializers
