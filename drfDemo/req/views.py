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
