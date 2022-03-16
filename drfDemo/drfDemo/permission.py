from rest_framework.permissions import BasePermission


class IsXiaoMingPermission(BasePermission):

    # def has_permission(self, request, view):
    #     """
    #     自定义选项
    #     返回结果为True 则表示允许访问视图类
    #     request:本次客户端提交的请求对象
    #     views: 本次客户端访问的视图类
    #     """
    #     # 写在自己要实现的代码过程,返回值为True,则表示通行
    #     # user = request.query_params.get("user")
    #     # return user == "xiaoming"
    #     return bool(request.user and request.user.username == "xiaoming")

    def has_object_permission(self, request, view, obj):
        """
        模型权限,写了视图权限(has_permission)方法 一般就 不需要写这个方法了
        返回结果为True 则表示允许访问
        request:本次客户端提交的请求对象
        views: 本次客户端访问的视图类
        obj:本次权限判断的模型对象
        """
        from school.models import Student
        if isinstance(obj, Student):
            # 限制只有小明才能操作的Student模型表
            user = request.query_params.get("user")
            return user == "xiaoming"
        else:
            # 操作其他模型 直接放行
            return True