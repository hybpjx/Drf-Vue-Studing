from rest_framework.viewsets import ModelViewSet
# Create your views here.
from students.models import Student
from .serializers import StuApiModelSerializers
# 创建一个序列器类 方便后面视图调用

class StuApiViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StuApiModelSerializers
