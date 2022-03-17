from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 2 # 每页多少条
    page_size_query_param = 'page_size' # 查询 字符串代表每一页数据的变量名
    page_query_param = "page" # 查询 字符串代表页码数据的变量名
    max_page_size = 4