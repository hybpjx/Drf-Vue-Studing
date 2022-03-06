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
