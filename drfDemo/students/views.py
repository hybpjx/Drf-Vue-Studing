from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
# Create your views here.
from students.models import Student


class StudentView(View):
    def get(self,request):
        stu = Student.objects.values()

        return JsonResponse(data=list(stu),safe=False)