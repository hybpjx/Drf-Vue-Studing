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
    path("students7/", StudentReadonlyMixinViewSet.as_view(
        {
            "get": "list",  # 视图类方法 可以是原来的http请求 也可以是自己自定义的方法名
            "post": "create",
        }
    )),
    path("students7/<int:pk>", StudentGenericViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }
    )),

    # 通用视图集 ReadonlyViewSet
    path("students8/", StudentReadonlyMixinViewSet.as_view(
        {
            "get": "list",  # 视图类方法 可以是原来的http请求 也可以是自己自定义的方法名
            "post": "create",
        }
    )),
    path("students8/<int:pk>", StudentReadonlyMixinViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }
    )),

    # path("students9/login",StudentModelViewSet.as_view({
    #     "get":"login"
    # }))
]

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
