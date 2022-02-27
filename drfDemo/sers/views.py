import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
# Create your views here.
from .serializers import StuSersApiSerializer
from students.models import Student


class StuSeriApiView(View):
    def get1(self, request):
        # 1. 序列化一个对象 得到序列化对象
        ser = StuSersApiSerializer()
        # 2. 调用序列化的对象的data 得到数据
        data = ser.data

        # 3. 相应数据
        return JsonResponse(data=data, safe=False, status=200)

    def get2(self, request):
        stu = Student.objects.all()
        # 1. 序列化一个对象 得到序列化对象
        ser = StuSersApiSerializer(instance=stu, many=True)
        # 2. 调用序列化的对象的data 得到数据
        data = ser.data

        # 3. 响应数据
        return JsonResponse(data=data, safe=False, status=200)

    def get3(self, request):
        # 1. 接受客户端发送来的信息
        # data = json.dumps(request.body)
        data = {
            "name": "xh",
            "gender": True,
            "age": 17,
            "classNum": "301",
            "description": "hello",
        }

        # 1.1 实例化序列化器 获取序列化对象
        serializer=StuSersApiSerializer(data=data)
        # 1.2 调用序列化器 进行数据验证
        ret =serializer.is_valid()
        print(f"{ret}")
        # 获取结果后 进行操作
        if ret:
            return JsonResponse(dict(serializer.validated_data))
        else:
            return JsonResponse(dict(serializer.errors))
        # 2. 操作数据库
        # 3. 响应数据


    def get(self, request):
        # 1. 接受客户端发送来的信息
        # data = json.dumps(request.body)
        data = {
            "name": "xh",
            "gender": True,
            "age": 17,
            "classNum": "301",
            "description": "hello",
        }

        # 1.1 实例化序列化器 获取序列化对象
        serializer=StuSersApiSerializer(data=data)
        # 1.2 调用序列化器 进行数据验证
        serializer.is_valid(raise_exception=True)

        # 2. 操作数据库
        # 3. 响应数据
