from django.db import models


# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    gender = models.BooleanField(default=1, verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    classNum = models.CharField(max_length=10, verbose_name="班级")
    description = models.CharField(max_length=32, verbose_name="个性签名")

    class Meta:
        db_table = "tb_student"
        verbose_name = "学生表"
        verbose_name_plural = "学生表"
