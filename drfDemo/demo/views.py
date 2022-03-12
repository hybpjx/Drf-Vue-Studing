from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
from demo.serializers import StudentModelSerializer
from students.models import Student


# api 基本视图类
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class StudentAPIInfoView(APIView):
    def get(self, request, pk):
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

    def put(self, request, pk):
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

    def delete(self, request, pk):
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

    def put(self, request, pk):
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

    def delete(self, request, pk):
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


from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class StudentInfoMixinsView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, pk):
        """
        获取一条数据
        """
        return self.retrieve(request, pk)

    def put(self, request, pk):
        """
        更新一条数据
        """
        return self.update(request, pk)

    def delete(self, request, pk):
        """
        删除一条数据
        """
        return self.destroy(request, pk)


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
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# class StudentView(ListAPIView, CreateAPIView):
class StudentView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


# class StudentInfoView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
class StudentInfoView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


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
from rest_framework.viewsets import ReadOnlyModelViewSet


class StudentReadonlyMixinViewSet(ReadOnlyModelViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


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

        # print(self.action)
        return Response({"msg":"用户活动历史记录"})