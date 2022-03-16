from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model


class CustomAuthentication(BaseAuthentication):
    """
     自定义认证类
    """

    def authenticate(self, request):
        """
        认证方法
        # request 本次客户端发来的http请求
        """
        user = request.query_params.get("user")
        # pwd = request.query_params.get("pwd")
        # if user != "zic" or pwd != "admin*123":
        #     return None

        # get_user_model 获取系统中用户表对应的用户模型类
        user = get_user_model().objects.filter(username=user).first()
        # 按照格式返回
        return (user, None)


