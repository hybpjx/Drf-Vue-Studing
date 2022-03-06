from students.models import Student
from rest_framework import serializers


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs = {
            #     选填 字段额外生命
            #     字段名：{
            #     "选项名":"选项值"
            #     }
            "age": {
                "min_value": 5,
                "max_value": 20,
                "error_messages": {
                    "min_value": "年龄最小不能小于5",
                    "max_value": "年龄最大不能大于20",
                },
            }
        }