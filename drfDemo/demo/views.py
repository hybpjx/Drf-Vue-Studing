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


class StudentInfoView(APIView):
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

"""
使用drf 内置的模型扩展类[混入类] 结合GenericAPIView 实现通用视图的简写操作
"""