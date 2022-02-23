from rest_framework.viewsets import ModelViewSet
# Create your views here.
from students.models import Student
from .serializers import StuApiModelSerializers

class StuApiViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StuApiModelSerializers
