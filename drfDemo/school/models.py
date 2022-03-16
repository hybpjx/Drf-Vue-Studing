from django.db import models
from django.utils import timezone as datetime

# Create your models here.

"""
学生      sch_student     1
成绩      sch_achievement n   n
课程      sch_course          1   n
老师      sch_teacher             1
"""


# 学生
class Student(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    age = models.SmallIntegerField(verbose_name="年龄")
    sex = models.BooleanField(default=False, verbose_name="性别")

    class Meta:
        db_table = "sch_student"

    # 自定义模型
    # 属性方法 可以直接当属性使用
    @property
    def achievement(self):
        """成绩列表"""
        # print(self.s_achievement.all())
        return self.s_achievement.values("student__name", "course__name", "score")

    def __str__(self):
        return self.name


# 课程
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="课程名称")
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, related_name="course", db_constraint=False)

    class Meta:
        db_table = "sch_course"

    def __str__(self):
        return self.name


# 教师
class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    sex = models.BooleanField(default=False, verbose_name="性别")

    class Meta:
        db_table = "sch_teacher"

    def __str__(self):
        return self.name


# 成绩
class Achievement(models.Model):
    score = models.DecimalField(default=0, max_digits=4, decimal_places=1, verbose_name="成绩")
    student = models.ForeignKey("Student", on_delete=models.DO_NOTHING, related_name="s_achievement",
                                db_constraint=False)
    course = models.ForeignKey("Course", on_delete=models.DO_NOTHING, related_name="c_achievement", db_constraint=False)
    create_time = models.DateTimeField(auto_created=datetime.now(), verbose_name="创建时间")

    class Meta:
        db_table = "sch_achievement"

    def __str__(self):
        return str(self.score)
