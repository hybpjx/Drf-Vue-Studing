from django.http import JsonResponse
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from drfDemo.authentication import CustomAuthentication
from school.models import Student
from school.serializers import StudentModelSerializers


class Example(APIView):
    # 类属性
    authentication_classes = [CustomAuthentication, ]

    def get(self, request):
        # AnonymousUser 未登录用户
        print(request.user)
        # <class 'django.contrib.auth.models.AnonymousUser'>
        # print(type(request.user))

        if request.user.id:
            print("已通过验证")
        else:
            print("未通过验证")

        return Response({"msg": "ok"})


class HomeVPIView(APIView):
    def get(self, request):
        # AnonymousUser 未登录用户
        print(request.user)
        # <class 'django.contrib.auth.models.AnonymousUser'>
        # print(type(request.user))

        if request.user.id:
            print("已通过验证")
        else:
            print("未通过验证")

        return Response({"msg": "ok"})


from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from drfDemo.permission import IsXiaoMingPermission


class HomeInfoAPIView(APIView):
    # 自定义认证
    authentication_classes = [CustomAuthentication, ]

    # # 内置权限
    # permission_classes = [IsAuthenticated] # 表示当前视图类中的视图方法只能被已登录的 的站点会员访问
    # permission_classes = [IsAdminUser] # 表示当前视图类中的视图方法 只能被管理员访问
    # permission_classes = [IsAuthenticatedOrReadOnly] # 表示当前视图类中的视图方法 游客只能查看 不能修改

    # 自定义权限
    permission_classes = [IsXiaoMingPermission]

    def get(self, request):
        return Response({"msg": "ok"})

    def post(self, request):
        return Response({"msg": "ok"})


from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle


class StudentInfoApiView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializers
    # 自定义权限
    permission_classes = [IsAuthenticated]

    # 限流局部配置 这里需要配合在配置中的DEFAULT_THROTTLE_RATES来设置频率
    throttle_classes = [UserRateThrottle]


class Demo1ApiView(APIView):
    """
    限流
    """
    permission_classes = [IsAuthenticated]

    throttle_scope = 'member'

    def get(self, request):
        return Response({"msg": "ok"})


class Demo2ApiView(APIView):
    """
    限流
    """
    permission_classes = [IsAuthenticated]

    throttle_scope = 'vip'

    def get(self, request):
        return Response({"msg": "ok"})


class Demo3ApiView(APIView):
    """
    限流
    """
    permission_classes = [IsAuthenticated]

    throttle_scope = 'vvip'

    def get(self, request):
        return Response({"msg": "ok"})
