from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.db import DataError

def exceptions_custom(exc,context):
    """
    自定义异常
    exc: 本次发生的异常
    context： 本次发生的异常的上下文环境
            所谓的执行上下文就是python解释器在执行代码时保存在内存中的变量，函数，类，对象，模块等一切信息
    """

    response=exception_handler(exc,context)
    # 如果返回值不是None则继续
    if response:
        pass
    # 如果为None 则有些异常是drf无法定义的，需要手动处理
    else:
        if isinstance(exc,ZeroDivisionError):
            response= Response({"detail":"不能被0除"})
        if isinstance(exc,DataError):
            response= Response({"detail":"数据库存储异常"})
    return response