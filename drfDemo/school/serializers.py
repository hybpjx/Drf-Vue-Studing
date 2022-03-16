from rest_framework import serializers

from school.models import *


# #  老师模型 序类化器类
# class TeacherModelSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Teacher
#         fields = "__all__"


#  成绩模型 序类化器类
class CourseModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        # 这样返回会有一个花括号 如何去除呢
        fields = ["name"]
        # fields = ("id", "name", "teacher")


#  成绩模型 序类化器类
class AchievementModelSerializers(serializers.ModelSerializer):
    # course=CourseModelSerializers()

    # 去除花括号 !! 一定要加引号
    course_name = serializers.CharField(source="course.name")
    teacher_name = serializers.CharField(source="course.teacher.name")

    class Meta:
        model = Achievement
        fields = ["id", "course_name", "score", "create_time", "teacher_name"]
        # fields = ("id", "course","score", "create_time")


#  成绩模型 序类化器类
class AchievementModelSerializers2(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = "__all__"
        """
        制定关联深度
        # 1.成绩模型->课程                   1
        # 2.从老师模型->课程->成绩            2
        # 3.从老师模型->课程->成绩->学生       3
        """
        depth=3


#  学生模型 序类化器类
class StudentModelSerializers(serializers.ModelSerializer):
    # s_achievement 就是 models 里指明的外键字段 ,不可以自定义 不能h指明序列化器
    # s_achievement = AchievementModelSerializers2(many=True)

    class Meta:
        model = Student
        fields = ("id", "name", "achievement")
        # fields = ("id", "name", "s_achievement")
