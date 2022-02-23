from rest_framework import serializers
# 创建一个序列器类 方便后面视图调用

from students.models import Student


class StuApiModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        fields = ["id", "name"]
