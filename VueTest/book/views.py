from django.shortcuts import render
from django.views import View
# Create your views here.
from django.http.response import JsonResponse  # 导入能处理Json响应的模块


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class BookView(View):
    def get(self, request):
        books_list = [
            {"id": 1, "title": "VUE详解", "price": 100},
            {"id": 2, "title": "K8s详解", "price": 200},
            {"id": 3, "title": "Echarts详解", "price": 300}
        ]
        return JsonResponse(books_list, safe=False)  # 实际项目中一般json数据来自数据库
