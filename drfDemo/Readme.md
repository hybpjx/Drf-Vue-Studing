# drf 序列化器

### **什么是序列化与反序列化**

```python
"""
序列化：对象转换为字符串用于传输
反序列化：字符串转换为对象用于使用
"""
```

### **drf序列化与反序列化**

```python
"""
序列化：Model类对象转换为字符串用于传输
反序列化：字符串转换为Model类对象用于使用
"""
```

创建models类

```python
from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    gender = models.BooleanField(default=1, verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    classNum = models.CharField(max_length=10, verbose_name="班级")
    description = models.CharField(max_length=32, verbose_name="个性签名")

    class Meta:
        db_table = "tb_student"
        verbose_name = "学生表"
        verbose_name_plural = "学生表"
```

## 正常显示页面

就是注册到 views 用类视图

然后巴拉巴拉一大堆 麻烦的要死

但用rest_framework则是

先在项目中新建有个serializers.py的文件

```python
from rest_framework import serializers
# 创建一个序列器类 方便后面视图调用

from students.models import Student

class StuApiModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        # 这里表明的是字段 
        # fields = ["id", "name"]
```

[然后再在views.py](http://然后再在views.py) 中设置

```python
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from students.models import Student
from .serializers import StuApiModelSerializers

class StuApiViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StuApiModelSerializers
```

 最后在url中注册

```python
from rest_framework.routers import DefaultRouter
from .views import StuApiViewSet

router = DefaultRouter() # 可处理路由的路由器

router.register(prefix="stu", viewset=StuApiViewSet, basename="stu")

# 路由列表
urlpatterns = [
              ] + router.urls
```

而序列化则是

serilizers.py

```python
from rest_framework import serializers

"""
serializers 是drf给开发者调用的序列化模块
里面声明了所有的可用序列化的基类
serializer 序列化基类 drf 所有的 许了话器类都必须继承于serializer
ModelSerializer 模型下序列化器类，是序列化基类的子类，在工作中，除了serializer基类意外 最常用的序列化器类基类

"""

class StuSersApiSerializer(serializers.Serializer):
    # 只读属性  在反序列化客户端 不会要求你提交此字段
    id = serializers.IntegerField(read_only=True)
    # 必填字段
    name = serializers.CharField(required=True)
    # 默认是男性 提交的时候
    gender = serializers.BooleanField(default=True)
    # 最大值 和最小值
    age = serializers.IntegerField(max_value=100,min_value=0,error_messages={
        "max_value":"必须小于100",
        "min_value":"必须大于0",
    })
    # 允许为空
    classNum = serializers.CharField(allow_null=True,allow_blank=True)
    description = serializers.CharField(allow_blank=True,allow_null=True)
```

views.py

```python
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
# Create your views here.
from .serializers import StuSersApiSerializer
from students.models import Student

class StuSeriApiView(View):
    def get2(self, request):
        stu = Student.objects.all()
        # 1. 序列化一个对象 得到序列化对象
        ser = StuSersApiSerializer(instance=stu, many=True)
        # 2. 调用序列化的对象的data 得到数据
        data = ser.data

        # 3. 响应数据
        return JsonResponse(data=data, safe=False, status=200)

    def get(self, request):
        # 1. 接受客户端发送来的信息
        # data = json.dumps(request.body)
        data = {
            "name": "xh",
            "gender": False,
            "age": -17,
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
```

urls.py

```python
from django.conf.urls import re_path
from django.urls import path
from .views import *

urlpatterns=[
    path("seri1/",StuSeriApiView.as_view())

]
```

## 数据校验的方法

### 多个字段进行验证

而在序列化器中 需要对多个字段进行验证 所以需要 用到validate

seralizers.py中

```python
 from rest_framework import serializers

"""
serializers 是drf给开发者调用的序列化模块
里面声明了所有的可用序列化的基类
serializer 序列化基类 drf 所有的 许了话器类都必须继承于serializer
ModelSerializer 模型下序列化器类，是序列化基类的子类，在工作中，除了serializer基类意外 最常用的序列化器类基类

"""

class StuSersApiSerializer(serializers.Serializer):
    # 只读属性  在反序列化客户端 不会要求你提交此字段
    id = serializers.IntegerField(read_only=True)
    # 必填字段
    name = serializers.CharField(required=True)
    # 默认是男性 提交的时候
    gender = serializers.BooleanField(default=True)
    # 最大值 和最小值
    age = serializers.IntegerField(max_value=100, min_value=0, error_messages={
        "max_value": "必须小于100",
        "min_value": "必须大于0",
    })
    # 允许为空
    classNum = serializers.CharField(allow_null=True, allow_blank=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)

    # validate 这个字段是对所有字段进行验证的
    def validate(self, attrs):
        """
        验证客户端的所有数据
        类所以于会员注册的密码和确认密码 就只能在validate的方法中校对
        validate是固定字段名
        而attr是实例化器实例化时的data数据选项
        """
        # 301 只能有女生 不能加入其他男生
        if attrs["classNum"] == "301" and attrs["gender"]:
            raise serializers.ValidationError(detail="301是女生班级 不可以进")
        return attrs
```

视图代码views.py

```python
def get(self, request):
        # 1. 接受客户端发送来的信息
        # data = json.dumps(request.body)
        data = {
            "name": "xh",
            "gender": False,
            "age": 17,
            "classNum": "301",
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
```

效果图

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/ca92684b-0d71-4572-9d51-58d97287c5c4/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/2eed476d-c8e6-4715-97be-5dbeb9b234d9/Untitled.png)

### 单字段进行验证

写在 `serializers.py` 中

validate_<字段名>

```python
class StuSersApiSerializer(serializers.Serializer):
    # 只读属性  在反序列化客户端 不会要求你提交此字段
    id = serializers.IntegerField(read_only=True)
    # 必填字段
    name = serializers.CharField(required=True)
    # 默认是男性 提交的时候
    gender = serializers.BooleanField(default=True)
    # 最大值 和最小值
    age = serializers.IntegerField(max_value=100, min_value=0, error_messages={
        "max_value": "必须小于100",
        "min_value": "必须大于0",
    })
    # 允许为空
    classNum = serializers.CharField(allow_null=True, allow_blank=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)

    # validate 这个字段是对所有字段进行验证的
    def validate(self, attrs):
        """
        验证客户端的所有数据
        类所以于会员注册的密码和确认密码 就只能在validate的方法中校对
        validate是固定字段名
        而attr是实例化器实例化时的data数据选项
        """
        # 301 只能有女生 不能加入其他男生
        if attrs["classNum"] == "301" and attrs["gender"]:
            raise serializers.ValidationError(detail="301是女生班级 不可以进")
        return attrs

    def validate_name(self, data):
        """
        验证单个字段
        方法名的格式必须v以validate_<字段名> 为名词 否则 序列化识别不到！
        validate 开头的方法 户自动被 is_valid调用
        """
        if data in ["python", "django"]:
            # 在序列化中 验证失败可以通过抛出异常 的方式 来告知 is valid
            raise serializers.ValidationError(detail="学生名不能是python 或者 django ", code="validate_name")
        # 验证完数据后 必须v返回数据 否则最终的验证结果中 就不会出现该数据
        return data
#！！！！！！！！！！！return data 一定要返回不然这个字段就是None
```

views.py

```python
def get(self, request):
        # 1. 接受客户端发送来的信息
        # data = json.dumps(request.body)
        data = {
            "name": "python",
            "gender": False,
            "age": 17,
            "classNum": "301",
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
```

效果图

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/537f42df-364f-4916-bbf5-acda64183d6a/Untitled.png)

### 外部验证函数

```python
def check_classnum(data):
    """外部验证函数"""
    if len(data) != 3:
        raise serializers.ValidationError(detail="格式不正确 必须v是三位数", code="check_classnum")

    # 验证完毕 必须返回 数据 不然 数据等于None  验证结果中没有该数据
    return data

class StuSersApiSerializer(serializers.Serializer):
    # 只读属性  在反序列化客户端 不会要求你提交此字段
    id = serializers.IntegerField(read_only=True)
    # 必填字段
    name = serializers.CharField(required=True)
    # 默认是男性 提交的时候
    gender = serializers.BooleanField(default=True)
    # 最大值 和最小值
    age = serializers.IntegerField(max_value=100, min_value=0, error_messages={
        "max_value": "必须小于100",
        "min_value": "必须大于0",
    })
    # 允许为空 单独指定一个方法 validators 是外部函数验证选项 嵌套列表 列表的字段是函数 不能是字符串
    classNum = serializers.CharField(validators=[check_classnum])
    description = serializers.CharField(allow_blank=True, allow_null=True)
```

效果如下

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/422864df-40c2-4f74-b1a1-b64a0488acaa/Untitled.png)

## 反序列化 增加和更新操作

### 增加

seralizers.py

```python
		
class StuSeriApiView(View):
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
        serializer.save() # 会根据实例化徐猎奇的时候 是否传入 instance属性来自动调用create方法

        # # 3. 响应数据
        return JsonResponse(serializer.data, status=201)
```

serializers.py

```python
class StuSersApiSerializer(serializers.Serializer):
    # 只读属性  在反序列化客户端 不会要求你提交此字段
    id = serializers.IntegerField(read_only=True)
    # 必填字段
    name = serializers.CharField(required=True)
    # 默认是男性 提交的时候
    gender = serializers.BooleanField(default=True)
    # 最大值 和最小值
    age = serializers.IntegerField(max_value=100, min_value=0, error_messages={
        "max_value": "必须小于100",
        "min_value": "必须大于0",
    })
    # 允许为空 单独指定一个方法 validators 是外部函数验证选项 嵌套列表 列表的字段是函数 不能是字符串
    classNum = serializers.CharField(validators=[check_classnum])
    description = serializers.CharField(allow_blank=True, allow_null=True)
.................
.................

    def create(self, validated_data):
        """
        添加数据
        添加数据操作 就自动实现了从字典变成模型对象的过程
        方法名固定为 create
        固定参数 为： validated_data 就是验证成功后的结果
        """
        student = Student.objects.create(**validated_data)
        return student
```

### 更新

views.py

```python
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
            "name": "xiaohon111g",
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
        return JsonResponse(serializer.data, status=200)
```

serializers.py

```python
def update(self, instance, validated_data):
    """
    更新数据操作
    更新数据操作 就自动实现了从字典变成模型对象的过程
    方法名固定为：update
    固定参数 instance 实现序列化对象时，必须v传入的模型对象
    固定参数 validated_data 就是严惩成功后的结果
    """

    # # todo: 太麻烦 直接用 for 循环 kv 写入
    # instance.name = validated_data["name"]
    # instance.age = validated_data["age"]
    # instance.gender = validated_data["gender"]
    # instance.classNum = validated_data["classNum"]
    # instance.description = validated_data["description"]
    # # 调用模型对象的save方法 和views视图中的serializers.save 不是一个方法
    for k, v in validated_data.items():
        setattr(instance, k, v)
    instance.save() # 调用模型对象中的save方法 和 视图中的serializers的save 不是一个方法

    return instance
```

### 附加说明

1. 在序列化操作进行save()保存时 可以额外传递数据 这些数据可以在create 和update的validdated_date参数 获取到
    
    ```python
    # request.user 是Django中 记录当前用户的模型对象
    serializer.save(owner=request.user) # 可以在save中 传递一些不需要的验证的数据到模型里面
    ```
    
2. 默认序列化器 必须传递 所有的require的字段 否则会抛出验证异常，但是完美可以使用partial参数来允许部分字段更新
    
    ```python
    #  更新`name` 不需要验证 其他的字段 可以设置 partial=True
    serializer = StudentApiSerializer(student,data={"name":"xiaoming"},partial=True)
    ```
    
     
    

### 模型序列化器 的操作和使用

models.py

```python
from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    gender = models.BooleanField(default=1, verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    classNum = models.CharField(max_length=10, verbose_name="班级")
    description = models.CharField(max_length=32, verbose_name="个性签名")

    class Meta:
        db_table = "tb_student"
        verbose_name = "学生表"
        verbose_name_plural = "学生表"
```

serializers.py

```python
class StudentModelSerializer(serializers.ModelSerializer):
    # 1. 转换的字段声明
    # 字段名 =  选项类型(选项=选项值)

    # 可以手动探究啊自定义字段
    nickname=serializers.CharField(read_only=True)

    # 2. 如果当前序列化继承的是 modelserializer 则需要声明调用的模型类型

    class Meta:
        model = Student
        # 这里表明的是字段
        fields = ["id", "name","nickname"]
        # fields ="__all__" # 字符串只能是这个 代表所有字段
        # 表示的是只读字段 表示设置的字段 只会在序列化阶段显示
        # read_only_fields=[]

        extract_kwargs = {
            #     选填 字段额外生命
            #     字段名：{
            #     "选项名":"选项值"
            #     }
        }

    # 3. 验证代码的对象方法

    # 4. 模型操作的方法
```

views.py

```python
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
```

# drf 中视图调用的http请求和响应处理类

drf除了在数据序列化部分简写代码以外 还在视图中提供了简写操作 ，所以在django原有的django views，views.views类基础上

drf 封装了多个做了出来提供给我们使用。

Django DRF framwork提供视图的主要作用：

- 数据序列化的执行（检验，保存，转换数据）
- 控制数据库查询的执行
- 调用请求类和响应类，这两个了也是由drf 帮我们再次扩展了一些功能类）

views.py

```python
from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response  # drf的response 是django HttpResponse对象的子类
from rest_framework import status  # 保存了 所有http响应状态对应的代码

# Create your views here.
class StudentView(View):
    def get(self, request):
        print(fr"request={request}")  # wsgi httpresonse 在视图中传递的变量是wsgi
        return HttpResponse("ok")

class StudentApiView(APIView):
    def get(self, request):
        print(f"request={request}")  # 和 上面的request 没有关系

        # 自定义响应头
        return Response({"msg": "ok"}, status=status.HTTP_201_CREATED, headers={"company": "i want to money"})

    def post(self, request):
        """
        添加数据/获取请求体数据
        """
        print(f"request.data={request.data}")  # 接受的数据 已经被Parser解析器转换成字典数据了
        print(request.data.get("name"))

        """
        获取查询参数/ 查询字符串
        """
        # query_params 和原生Django 的request.get 相同 只是更换了名字
        print(f"request.query_params={request.query_params}")

        return Response({"msg": "ok"})

    def put(self, request):
        """
        更新数据
        """
        print(f"request={request}")  # 和 上面的request 没有关系
        return Response({"msg": "ok"})

    def patch(self, request):
        """
        更新数据[部分]
        """
        print(f"request={request}")  # 和 上面的request 没有关系
        return Response({"msg": "ok"})

    def delete(self, request):
        """
        删除数据
        """
        print(f"request={request}")  # 和 上面的request 没有关系
        return Response({"msg": "ok"})
```

## 基本视图类APIView和通用视图类GenericAPIView的声明和使用

### APIView基本视图类

```python
from rest_framework.views import APIView
```

APIView 是 REST framework 提供的 所有视图类的积累 继承自Django 的View 弗雷

`APIView` 和 `View`不同之处在于

- 传入的视图方法是REST framework的Request 对象，而不是Django 的HttpRequest对象：
- 视图方法可以返回REST framework的Response对象，视图会为响应数据设置符合的前端期望要求的格式。
- 任意APIException一场都会被捕获到，并且处理成合格格式的响应信息返回给客户端：
    - Django 的View 所有一场全部以HTML格式显示
    - DRF中的APIView 的子类会自动根据 客户端中的accept进行的错误格式进行转换
- 重新生命应该新的as_view方法并在 dispatch()进行 路由分发前 会对请求的客户端进行身份验证，权限检查，流量控制。

APIView新增加了类属性

> **authentication_classes**  列表或者元组 身份认证类
> 

> **permission_classes**  列表或者元组 权限检查类
> 

> **throttle_classes**  列表或者元组 流量控制类
> 

在APIView 中仍以常规的类视图定义方法来实现get(),post 或者请求其他方式的方法

序列化器serializer.py 

```python
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
```

views.py 

```python
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
from demo.serializers import StudentModelSerializer
from students.models import Student

class StudentAPIView(APIView):
    """
    GET /demo/students/ 获取所有学生信息
    POST /demo/students/ 添加一个学生信息

    GET /demo/students/<pk> 获取一个学生信息
    PUT /demo/students/<pk> 更新一个学生信息
    DELETE /demo/students/<pk> 删除一个学生信息
    """

    def get(self, request):
        """
        获取所有学生信息
        """
        # 1. 从数据库中读取学生信息列表
        student_list = Student.objects.all()
        # 2. 实例化序列化器, 获取序列化对象
        serializer = StudentModelSerializer(instance=student_list, many=True)
        # 3. 转换 数据并且返回给客户端
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        添加一条数据
        """
        # 1.获取客户端 提交的数据
        # request.data # 获取客户端提交的数据
        # 2.实例化序列化器,获取序列化器对象
        serializer = StudentModelSerializer(data=request.data)
        # 3. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回新增的模型数据给客户端
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def put(self, request):
        pass

    def delete(self, request):
        pass

class StudentInfoView(APIView):
    def get(self,request,pk):
        """
        获取一条数据
        """
        # 1. 使用pk 作为条件获取模型对象
        try:
            student=Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 2. 序列化
        serializer= StudentModelSerializer(instance=student)
        # 3. 返回结果
        return Response(serializer.data)

    def put(self,request,pk):
        """
        更新数据
        """
        # 1. 使用pk 获取要更新的数据
        try:
            student=Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 获取客户端提交的数据
        serializer= StudentModelSerializer(instance=student,data=request.data)

        # 3. 反序列化[验证数据和数据保存]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回结果
        return Response(serializer.data)

    def delete(self,request,pk):
        """
        删除数据
        """
        # 1. 使用pk 获取要删除的数据并删除
        try:
            student=Student.objects.get(pk=pk).delete()
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 结果
        return Response(status.HTTP_204_NO_CONTENT)
```

路由 urls.py

```python
from django.urls import path
from .views import *

urlpatterns = [
    path("students/", StudentAPIView.as_view()),
    path("students/<int:pk>", StudentInfoView.as_view()),
]
```

### GenericAPIView(通用视图类)

通用视图类的主要作用就是把视图中的独特的代码 抽离出来 使得代码更加通用 方便把代码进行简写

GenericAPIView 继承于 APIView

主要增加了操作序列化和操作数据库的方法 作用是为下面mixin扩展类的执行提供方法支持 通常在使用时，可以搭配应该或者多个Mixin扩展类

views.py

```python
"""GenericApIView通用视图类"""
from rest_framework.generics import GenericAPIView

class StudentGenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        """获取所有数据"""
        # 1. 从数据库获取学生列表信息
        queryset = self.get_queryset()  # Generic APIView提供的get_queryset(
        # 2. 序列化
        serializer = self.get_serializer(instance=queryset, many=True)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def post(self, request):
        """添加一个数据"""
        # 1. 获取客户端 提交的数据 实现序列化器,获取序列化兑现
        serializer = self.get_serializer(data=request.data)
        # 2. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3. 返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StudentInfoGenericApiView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    def get(self, request, pk):
        """获取一个数据"""
        # 1.使用pk 作为条件获取数据
        instance = self.get_object()
        # instance = self.queryset().get(pk=3)
        # 2.序列化
        serializer = self.get_serializer(instance=instance)
        # 3. 返回结果

        return Response(serializer.data)

    def put(self,request,pk):
        """更新一条数据"""

        # 1.使用pk 作为条件获取数据
        instance = self.get_object()

        # 2. 获取客户端提交的数据
        serializer = self.get_serializer(instance=instance,data=request.data)

        # 3. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回结果
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def delete(self,request,pk):
        """
        删除数据
        """
        # 1. 使用pk 获取要删除的数据并删除
        try:
            student = self.get_object().delete()
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 结果
        return Response(status.HTTP_204_NO_CONTENT)
```

url.py

```python
from django.urls import path
from .views import *

urlpatterns = [
    # GenericAPIView
    path("students2/",StudentGenericAPIView.as_view()),
    path("students2/<int:pk>", StudentInfoGenericApiView.as_view()),
]
```

## 基于Mixin模型扩展类+GenericView 通用类

views.py

```python
"""
使用drf 内置的模型扩展类[混入类] 结合GenericAPIView 实现通用视图的简写操作
from rest_framework.mixins import ListModelMixin  获取多条数据 返回结果
from rest_framework.mixins import CreateModelMixin 添加一条数据 返回结果
from rest_framework.mixins import RetrieveModelMixin 获取一条数据 返回结果
from rest_framework.mixins import UpdateModelMixin 更新一条数据 返回结果
from rest_framework.mixins import DestroyModelMixin 删除一条数据 返回结果
"""

from rest_framework.mixins import ListModelMixin, CreateModelMixin

class StudentMixinsView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        "获取所有数据"
        return self.list(request)

    def post(self, request):
        "添加一条数据"
        return self.create(request)

from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin

class StudentInfoMixinsView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self,request,pk):
        """
        获取一条数据
        """
        return self.retrieve(request,pk)

    def put(self,request,pk):
        """
        更新一条数据
        """
        return self.update(request,pk)

    def delete(self,request,pk):
        """
        删除一条数据
        """
        return self.destroy(request,pk)
```

urls.py

```python
# GenericAPIView+Mixin
    path("students3/",StudentMixinsView.as_view()),
    path("students3/<int:pk>",StudentInfoMixinsView.as_view()),
```

## 视图子类

views.py

```python
"""
视图子类是通用试图类,和模型扩展类的子类
上面的接口代码 还可以继续更加的精简drf 在使用genericAPIView和mixins合并后 还提供了视图子类
视图子类 提供了各种视图方法 调用mixins操作

ListAPIView = GenericAPIView + ListModelMixin # 获取多条数据的视图方法
CreateAPIView = GenericAPIView + CreateModelMixin # 添加一条数据的视图方法
RetrieveAPIView = GenericAPIView + RetrieveModelMixin # 获取一条数据的视图方法
UpdateAPIView = GenericAPIView+UpdateModelMixin # 更新一条数据的视图方法
DestroyAPIView = GenericAPIView + DestroyModelMixin # 删除一条数据的视图方法
组合视图子类
ListCreateAPIView = ListAPIView+CreateAPIView
RetrieveUpdateAPIView  = RetrieveAPIView+UpdateAPIView
RetrieveDestroyAPIView = RetrieveAPIView+DestroyAPIView
RetrieveUpdateDestroyAPIView=RetrieveAPIView+UpdateAPIView
"""
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

# class StudentView(ListAPIView, CreateAPIView):
class StudentView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

# class StudentInfoView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
class StudentInfoView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
```

url.py

```python
# ListAPIView+CreateAPIView+...
    path("students4/",StudentView.as_view()),
    path("students4/<int:pk>",StudentInfoMixinsView.as_view()),
```

## 基于视图集和路由集实现API接口

### 视图集ViewSet

view.py

```python
"""
在上面的接口实现 过程中 也存在代码重复的情况,如果我们合并成一个接口类,则需要考虑两个问题
1. 路由的合并问题
2. get方法重复的问题

drf提供了视图集来解决这个问题

"""

"""
ViewSet -> APIView的代码重复问题 基本视图集
"""
from rest_framework.viewsets import ViewSet

class StudentViewSet(ViewSet):
    def get_list(self, request):
        """获取所有数据"""
        # 1. 从数据库获取学生列表信息
        student_list = Student.objects.all()
        # 2. 序列化
        serializer = StudentModelSerializer(instance=student_list, many=True)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def post(self, request):
        """
        添加一条数据
        """
        # 1.获取客户端 提交的数据
        # request.data # 获取客户端提交的数据
        # 2.实例化序列化器,获取序列化器对象
        serializer = StudentModelSerializer(data=request.data)
        # 3. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_student_info(self, request, pk):
        """
        获取一条数据
        """
        # 1. 使用pk 作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 2. 序列化
        serializer = StudentModelSerializer(instance=student)
        # 3. 返回结果
        return Response(serializer.data)

    def update_student_info(self, request, pk):
        """
                更新数据
                """
        # 1. 使用pk 获取要更新的数据
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 获取客户端提交的数据
        serializer = StudentModelSerializer(instance=student, data=request.data)

        # 3. 反序列化[验证数据和数据保存]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回结果
        return Response(serializer.data)

    def delete_student_info(self, request, pk):
        """
              删除数据
              """
        # 1. 使用pk 获取要删除的数据并删除
        try:
            student = Student.objects.get(pk=pk).delete()
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 结果
        return Response(status.HTTP_204_NO_CONTENT)
```

路由

urls.py

```python
from django.urls import path
from .views import *

urlpatterns = [
    # APIView
    path("students/", StudentAPIView.as_view()),
    path("students/<int:pk>", StudentAPIInfoView.as_view()),

    # GenericAPIView
    path("students2/", StudentGenericAPIView.as_view()),
    path("students2/<int:pk>", StudentInfoGenericApiView.as_view()),

    # GenericAPIView+Mixin
    path("students3/", StudentMixinsView.as_view()),
    path("students3/<int:pk>", StudentInfoMixinsView.as_view()),

    # ListAPIView+CreateAPIView+...
    path("students4/", StudentView.as_view()),
    path("students4/<int:pk>", StudentInfoMixinsView.as_view()),

    # 视图集 ViewSet
    path("students5/", StudentViewSet.as_view(
        {
            "get": "get_list",  # 视图类方法 可以是原来的http请求 也可以是自己自定义的方法名
            "post": "post",
        }
    )),
    path("students5/<int:pk>", StudentViewSet.as_view(
        {
            "get": "get_student_info",
            "put": "update_student_info",
            "delete": "delete_student_info",
        }
    )),

]
```

### 通用视图集GenericViewSet

views.py

```python
"""
GenericViewSet APIView的代码重复问题 通用视图集 同时使得代码更加通用
"""
from rest_framework.viewsets import GenericViewSet

class StudentGenericViewSet(GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def list(self, request):
        """获取所有数据"""
        # 1. 从数据库获取学生列表信息
        queryset = self.get_queryset()  # Generic APIView提供的get_queryset(
        # 2. 序列化
        serializer = self.get_serializer(instance=queryset, many=True)
        # 3. 转换数据并返回给客户端
        return Response(serializer.data)

    def create(self, request):
        """添加一个数据"""
        # 1. 获取客户端 提交的数据 实现序列化器,获取序列化兑现
        serializer = self.get_serializer(data=request.data)
        # 2. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3. 返回新增的模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        """获取一个数据"""
        # 1.使用pk 作为条件获取数据
        instance = self.get_object()
        # instance = self.queryset().get(pk=3)
        # 2.序列化
        serializer = self.get_serializer(instance=instance)
        # 3. 返回结果

        return Response(serializer.data)

    def update(self, request, pk):
        """更新一条数据"""

        # 1.使用pk 作为条件获取数据
        instance = self.get_object()

        # 2. 获取客户端提交的数据
        serializer = self.get_serializer(instance=instance, data=request.data)

        # 3. 反序列化[验证数据,保存数据到数据库]
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4. 返回结果
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """
                删除数据
                """
        # 1. 使用pk 获取要删除的数据并删除
        try:
            student = self.get_object().delete()
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2. 结果
        return Response(status.HTTP_204_NO_CONTENT)
```

urls.py

```python
from django.urls import path
from .views import *

urlpatterns = [
    # APIView
    path("students/", StudentAPIView.as_view()),
    path("students/<int:pk>", StudentAPIInfoView.as_view()),

    # GenericAPIView
    path("students2/", StudentGenericAPIView.as_view()),
    path("students2/<int:pk>", StudentInfoGenericApiView.as_view()),

    # GenericAPIView+Mixin
    path("students3/", StudentMixinsView.as_view()),
    path("students3/<int:pk>", StudentInfoMixinsView.as_view()),

    # ListAPIView+CreateAPIView+...
    path("students4/", StudentView.as_view()),
    path("students4/<int:pk>", StudentInfoMixinsView.as_view()),

    # 视图集 ViewSet
    path("students5/", StudentViewSet.as_view(
        {
            "get": "get_list",  # 视图类方法 可以是原来的http请求 也可以是自己自定义的方法名
            "post": "post",
        }
    )),
    path("students5/<int:pk>", StudentViewSet.as_view(
        {
            "get": "get_student_info",
            "put": "update_student_info",
            "delete": "delete_student_info",
        }
    )),

    # 通用视图集 GenericViewSet
    path("students6/", StudentGenericViewSet.as_view(
        {
            "get": "list",  # 视图类方法 可以是原来的http请求 也可以是自己自定义的方法名
            "post": "create",
        }
    )),
    path("students6/<int:pk>", StudentGenericViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }
    )),
]
```

### 通用视图集+mixin混合类

views.py

```python
"""
GenericViewSet 通用视图集+mixin混合类
"""

# 继承的五个类 刚好有 五个方法 list  create update retrieve destroy
class StudentGenericMixinViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin,
                                 DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

"""
上面的接口类继承的父类太多了
我们可以用一些合并的视图父类让其继承

ReadOnlyModelViewSet = mixins.RetrieveModelMixin + mixins.listModelMixin+GenericView

获取多条数据
获取一条数据
"""
# modelViewSet 实现了五合一
from rest_framework.viewsets import  ReadOnlyModelViewSet

class StudentReadonlyMixinViewSet(ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

from rest_framework.viewsets import ModelViewSet
class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
```

urls.py

```python
from django.urls import path
from .views import *

urlpatterns = [
    # APIView
    path("students/", StudentAPIView.as_view()),
    path("students/<int:pk>", StudentAPIInfoView.as_view()),

    # GenericAPIView
    path("students2/", StudentGenericAPIView.as_view()),
    path("students2/<int:pk>", StudentInfoGenericApiView.as_view()),

    # GenericAPIView+Mixin
    path("students3/", StudentMixinsView.as_view()),
    path("students3/<int:pk>", StudentInfoMixinsView.as_view()),

    # ListAPIView+CreateAPIView+...
    path("students4/", StudentView.as_view()),
    path("students4/<int:pk>", StudentInfoMixinsView.as_view()),

    # 视图集 ViewSet
    path("students5/", StudentViewSet.as_view(
        {
            "get": "get_list",  # 视图类方法 可以是原来的http请求 也可以是自己自定义的方法名
            "post": "post",
        }
    )),
    path("students5/<int:pk>", StudentViewSet.as_view(
        {
            "get": "get_student_info",
            "put": "update_student_info",
            "delete": "delete_student_info",
        }
    )),

    # 通用视图集 GenericViewSet
    path("students6/", StudentGenericViewSet.as_view(
        {
            "get": "list",  # 视图类方法 可以是原来的http请求 也可以是自己自定义的方法名
            "post": "create",
        }
    )),
    path("students6/<int:pk>", StudentGenericViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }
    )),

    # 通用视图集 GenericViewSet+mixin 混合类
    path("students6/", StudentReadonlyMixinViewSet.as_view(
        {
            "get": "list",  # 视图类方法 可以是原来的http请求 也可以是自己自定义的方法名
            "post": "create",
        }
    )),
    path("students6/<int:pk>", StudentGenericViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }
    )),

    # 通用视图集 ReadonlyViewSet
    path("students7/", StudentReadonlyMixinViewSet.as_view(
        {
            "get": "list",  # 视图类方法 可以是原来的http请求 也可以是自己自定义的方法名
            "post": "create",
        }
    )),
    path("students7/<int:pk>", StudentReadonlyMixinViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }
    )),
]
```

# 路由Routers

无形之中 我们的路由就增加了  所以需要简化代码

urls.py

```python
# 自动生成路由信息(和视图集一起使用)
from rest_framework.routers import SimpleRouter, DefaultRouter

# 1. 实例化一个路由器
router = DefaultRouter()
# router = SimpleRouter() # 会缺失API主界面
# 2. 给路由注册去注册视图集
router.register("students9", StudentModelViewSet, basename="students9")
router.register("students10", StudentModelViewSet, basename="students10")
print(router.urls)
# 3. 把生成的路由列表和原路由进行拼接
urlpatterns += router.urls
```

用action 封装 路由

```python
class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    # http://127.0.0.1:8000/demo/students9/student111/login/
    @action(methods=["get"],detail=False,url_path="student111/login")
    def login(self, request):
        """
        登陆视图
        """
        return Response({"msg": "ok"})

    # http://127.0.0.1:8000/demo/students9/1/login/log/
    @action(methods=["get"],detail=True,url_path="login/log")
    def login_log(self,request,pk):
        # 视图集类中比普通视图类多一个属性 action
        # 可以通过self.method 获取本次客户端的http请求
        # 可以通过self.action获取本次客户端请求的视图方法名[ViewSet提供的]

        print(self.action)
        return Response({"msg":"用户活动历史记录"})
```

# 序列化嵌套

新建 app school

新建models.py

```sql
from django.db import models
from django.utils import timezone as datetime

# Create your models here.

"""
学生      sch_student     1
成绩      sch_achievement n   n
课程      sch_course          1   n
老师      sch_teacher             1
"""

# 学生
class Student(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    age = models.SmallIntegerField(verbose_name="年龄")
    sex = models.BooleanField(default=False, verbose_name="性别")

    class Meta:
        db_table = "sch_student"

    # 自定义模型
    # 属性方法 可以直接当属性使用
    @property
    def achievement(self):
        """成绩列表"""
        # print(self.s_achievement.all())
        return self.s_achievement.values("student__name", "course__name", "score")

    def __str__(self):
        return self.name

# 课程
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="课程名称")
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, related_name="course", db_constraint=False)

    class Meta:
        db_table = "sch_course"

    def __str__(self):
        return self.name

# 教师
class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    sex = models.BooleanField(default=False, verbose_name="性别")

    class Meta:
        db_table = "sch_teacher"

    def __str__(self):
        return self.name

# 成绩
class Achievement(models.Model):
    score = models.DecimalField(default=0, max_digits=4, decimal_places=1, verbose_name="成绩")
    student = models.ForeignKey("Student", on_delete=models.DO_NOTHING, related_name="s_achievement",
                                db_constraint=False)
    course = models.ForeignKey("Course", on_delete=models.DO_NOTHING, related_name="c_achievement", db_constraint=False)
    create_time = models.DateTimeField(auto_created=datetime.now(), verbose_name="创建时间")

    class Meta:
        db_table = "sch_achievement"

    def __str__(self):
        return str(self.score)
```

迁移数据

`python manager.py migrations`

 `python manager.py migrate`

添加数据

```sql
insert into drf.sch_teacher(id,name,sex) VALUES(1,"李老师",0);
insert into drf.sch_teacher(id,name,sex) VALUES(2,"曹老师",1);
insert into drf.sch_teacher(id,name,sex) VALUES(3,"王老师",2);

insert into drf.sch_student(id,name,age,sex) VALUES(1,"小明",18,0);
insert into drf.sch_student(id,name,age,sex) VALUES(2,"小王",19,1);
insert into drf.sch_student(id,name,age,sex) VALUES(3,"小李",17,0);
insert into drf.sch_student(id,name,age,sex) VALUES(4,"小钱",18,0);
insert into drf.sch_student(id,name,age,sex) VALUES(5,"小白",16,1);
insert into drf.sch_student(id,name,age,sex) VALUES(6,"小黑",15,1);
insert into drf.sch_student(id,name,age,sex) VALUES(7,"小赵",14,0);
insert into drf.sch_student(id,name,age,sex) VALUES(8,"小梁",13,1);
insert into drf.sch_student(id,name,age,sex) VALUES(9,"小风",21,1);
insert into drf.sch_student(id,name,age,sex) VALUES(10,"小林",22,1);
insert into drf.sch_student(id,name,age,sex) VALUES(11,"小麦",20,0);
insert into drf.sch_student(id,name,age,sex) VALUES(12,"小丽",22,0);
insert into drf.sch_student(id,name,age,sex) VALUES(13,"小石",21,1);
insert into drf.sch_student(id,name,age,sex) VALUES(14,"小丹",18,0);

insert into drf.sch_course(id,name,teacher_id) VALUES(1,"Python入门",1);
insert into drf.sch_course(id,name,teacher_id) VALUES(2,"Python进阶",2);
insert into drf.sch_course(id,name,teacher_id) VALUES(3,"Python高级",3);
insert into drf.sch_course(id,name,teacher_id) VALUES(4,"Goland入门",4);
insert into drf.sch_course(id,name,teacher_id) VALUES(5,"Goland进阶",5);
insert into drf.sch_course(id,name,teacher_id) VALUES(6,"Goland高级",6);

insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",1,100.0,1,1);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",2,100.0,2,2);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",3,100.0,3,3);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",4,100.0,4,4);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",5,100.0,5,5);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",6,100.0,6,6);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",7,100.0,7,1);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",8,100.0,8,2);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",9,100.0,9,3);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",10,100.0,10,4);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",11,100.0,11,5);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",12,100.0,12,6);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",13,100.0,13,1);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",14,100.0,14,2);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",15,100.0,1,3);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",16,100.0,2,4);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",17,100.0,3,5);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",18,100.0,4,6);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",19,100.0,5,1);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",20,100.0,6,2);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",21,100.0,7,3);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",22,100.0,8,4);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",23,100.0,9,5);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",24,100.0,10,6);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",25,100.0,11,1);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",26,100.0,12,2);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",27,100.0,13,3);
insert into drf.sch_achievement(create_time,id,score,course_id,student_id) VALUES("2022-03-12 08:01:09",28,100.0,14,4);
```

seriaizer.py

```sql
from rest_framework import serializers

from school.models import *

# #  老师模型 序类化器类
# class TeacherModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Teacher
#         fields = "__all__"

#  成绩模型 序类化器类
class CourseModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        # 这样返回会有一个花括号 如何去除呢
        fields = ["name"]
        # fields = ("id", "name", "teacher")

#  成绩模型 序类化器类
class AchievementModelSerializers(serializers.ModelSerializer):
    # course=CourseModelSerializers()

    # 去除花括号 !! 一定要加引号
    course_name = serializers.CharField(source="course.name")
    teacher_name = serializers.CharField(source="course.teacher.name")

    class Meta:
        model = Achievement
        fields = ["id", "course_name", "score", "create_time", "teacher_name"]
        # fields = ("id", "course","score", "create_time")

#  成绩模型 序类化器类
class AchievementModelSerializers2(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = "__all__"
        """
        制定关联深度
        # 1.成绩模型->课程                   1
        # 2.从老师模型->课程->成绩            2
        # 3.从老师模型->课程->成绩->学生       3
        """
        depth=3

#  学生模型 序类化器类
class StudentModelSerializers(serializers.ModelSerializer):
    # s_achievement 就是 models 里指明的外键字段 ,不可以自定义 不能h指明序列化器
    # s_achievement = AchievementModelSerializers2(many=True)

    class Meta:
        model = Student
        fields = ("id", "name", "achievement")
        # fields = ("id", "name", "s_achievement")
```

views.py

```sql
from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializers import StudentModelSerializers

class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializers
```

urls.py

```sql
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("students", StudentModelViewSet, basename="students")

urlpatterns = [
              ] + router.urls
```

》