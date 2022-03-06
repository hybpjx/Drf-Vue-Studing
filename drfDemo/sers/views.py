import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
# Create your views here.
from .serializers import StuSersApiSerializer, StudentModelSerializer
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
        serializer = StuSersApiSerializer(data=data)
        # 1.2 调用序列化器 进行数据验证
        ret = serializer.is_valid()
        print(f"{ret}")
        # 获取结果后 进行操作
        if ret:
            return JsonResponse(dict(serializer.validated_data))
        else:
            return JsonResponse(dict(serializer.errors))
        # 2. 操作数据库
        # 3. 响应数据

    def get4(self, request):
        # 1. 接受客户端发送来的信息
        # data = json.dumps(request.body)
        data = {
            "name": "pyth1on",
            "gender": False,
            "age": 17,
            "classNum": "3011",
            "description": "这家伙很懒 什么都没有留下",
        }

        # 1.1 实例化序列化器 获取序列化对象
        serializer = StuSersApiSerializer(data=data)
        # 1.2 调用序列化器 进行数据验证
        serializer.is_valid(raise_exception=True)

        print(data)
        # 2. 操作数据库
        # 3. 响应数据

        return JsonResponse({})

    # 创建 添加
    def get5(self, request):
        # 1. 接受客户端发送来的信息
        # data = json.dumps(request.body)
        data = {
            "name": "pyth1on",
            "gender": False,
            "age": 17,
            "classNum": "311",
            "description": "这家伙很懒 什么都没有留下",
        }

        # 1.1 实例化序列化器 获取序列化对象
        serializer = StuSersApiSerializer(data=data)
        # 1.2 调用序列化器 进行数据验证
        serializer.is_valid(raise_exception=True)
        """
        # # 2. 操作数据库
        # student = Student.objects.create(**serializer.data)
        # # print("student:",student) # 是一个 object 对象
        # serializer = StuSersApiSerializer(instance=student)
        # # print("serializer:",serializer) # 是 serializer
        """

        # 2. 获取验证以后的结果 操作数据
        serializer.save()  # 会根据实例化徐猎奇的时候 是否传入 instance属性来自动调用create方法

        # # 3. 响应数据
        return JsonResponse(serializer.data, status=201)

    # 更新操作
    def get(self, request):
        # 根据客户端访问的url 获得pk值
        #  sers/student/2 path("/student/?<pk>\d+/")
        pk = 3

        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return JsonResponse({"error": "该学生不存在"}, status=400)

        # 2. 接受客户端提供的数据
        data = {
            "name": "xiaohong",
            "age": 18,
            "gender": False,
            "classNum": "301",
            "description": "这家伙很懒 什么都没有留下"
        }

        # 3. 修改操作中的实例化序列器对象
        serializer = StuSersApiSerializer(instance=student, data=data)
        # 4.验证数据
        serializer.is_valid(raise_exception=True)

        # 5. 入库
        serializer.save() # 可以在save 中 传递一些不需要验证的数据到模型里面

        # 6. 返回结果
        return JsonResponse(serializer.data, status=201)


class StudentView(View):
    def get1(self, request):
        # 1. 序列化一个对象 得到序列化对象
        student = Student.objects.first()
        #
        student.nickname="小学生"

        serializer = StudentModelSerializer(student)
        # 2. 调用序列化的对象的data 得到数据
        data = serializer.data
        # 3. 相应数据
        return JsonResponse(data=data, safe=False, status=200,json_dumps_params={"ensure_ascii":False})

    def get2(self, request):
        stu = Student.objects.all()
        # 1. 序列化一个对象 得到序列化对象
        ser = StudentModelSerializer(instance=stu, many=True)
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
            "age": 117,
            "classNum": "301",
            "description": "hello",
        }

        # 1.1 实例化序列化器 获取序列化对象
        serializer = StudentModelSerializer(data=data)
        # 1.2 调用序列化器 进行数据验证
        ret = serializer.is_valid()
        print(f"{ret}")
        # 获取结果后 进行操作
        if ret:
            return JsonResponse(dict(serializer.validated_data))
        else:
            return JsonResponse(dict(serializer.errors))
        # 2. 操作数据库
        # 3. 响应数据

    def get4(self, request):
        # 1. 接受客户端发送来的信息
        # data = json.dumps(request.body)
        data = {
            "name": "pyth1on",
            "gender": False,
            "age": 117,
            "classNum": "3011",
            "description": "这家伙很懒 什么都没有留下",
        }

        # 1.1 实例化序列化器 获取序列化对象
        serializer = StudentModelSerializer(data=data)
        # 1.2 调用序列化器 进行数据验证
        serializer.is_valid(raise_exception=True)

        print(data)
        # 2. 操作数据库
        # 3. 响应数据

        return JsonResponse({})

    # 创建 添加
    def get(self, request):
        # 1. 接受客户端发送来的信息
        # data = json.dumps(request.body)
        data = {
            "name": "pyth1on",
            "gender": False,
            "age": 17,
            "classNum": "311",
            "description": "这家伙很懒 什么都没有留下",
        }

        # 1.1 实例化序列化器 获取序列化对象
        serializer = StudentModelSerializer(data=data)
        # 1.2 调用序列化器 进行数据验证
        serializer.is_valid(raise_exception=True)
        """
        # # 2. 操作数据库
        # student = Student.objects.create(**serializer.data)
        # # print("student:",student) # 是一个 object 对象
        # serializer = StuSersApiSerializer(instance=student)
        # # print("serializer:",serializer) # 是 serializer
        """

        # 2. 获取验证以后的结果 操作数据
        serializer.save()  # 会根据实例化徐猎奇的时候 是否传入 instance属性来自动调用create方法

        # # 3. 响应数据
        return JsonResponse(serializer.data, status=201)

    # 更新操作
    def get6(self, request):
        # 根据客户端访问的url 获得pk值
        #  sers/student/2 path("/student/?<pk>\d+/")
        pk = 3

        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return JsonResponse({"error": "该学生不存在"}, status=400)

        # 2. 接受客户端提供的数据
        data = {
            "name": "xiaohong",
            "age": 18,
            "gender": False,
            "classNum": "301",
            "description": "这家伙很懒 什么都没有留下"
        }

        # 3. 修改操作中的实例化序列器对象
        serializer = StudentModelSerializer(instance=student, data=data)
        # 4.验证数据
        serializer.is_valid(raise_exception=True)

        # 5. 入库
        serializer.save() # 可以在save 中 传递一些不需要验证的数据到模型里面

        # 6. 返回结果
        return JsonResponse(serializer.data, status=201)
