from rest_framework import serializers

"""
serializers 是drf给开发者调用的序列化模块
里面声明了所有的可用序列化的基类
serializer 序列化基类 drf 所有的 许了话器类都必须继承于serializer
ModelSerializer 模型下序列化器类，是序列化基类的子类，在工作中，除了serializer基类意外 最常用的序列化器类基类

"""


class StuSersApiSerializer(serializers.Serializer):
    # 只读属性  在反序列化客户端 不会要求你提交此字段
    id = serializers.IntegerField(read_only=True)
    # 必填字段
    name = serializers.CharField(required=True)
    # 默认是男性 提交的时候
    gender = serializers.BooleanField(default=True)
    # 最大值 和最小值
    age = serializers.IntegerField(max_value=100, min_value=0, error_messages={
        "max_value": "必须小于100",
        "min_value": "必须大于0",
    })
    # 允许为空
    classNum = serializers.CharField(allow_null=True, allow_blank=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)

    # validate 这个字段是对所有字段进行验证的
    def validate(self, attrs):
        """
        验证客户端的所有数据
        类所以于会员注册的密码和确认密码 就只能在validate的方法中校对
        validate是固定字段名
        而attr是实例化器实例化时的data数据选项
        """
        # 301 只能有女生 不能加入其他男生
        if attrs["classNum"] == "301" and attrs["gender"]:
            raise serializers.ValidationError(detail="301是女生班级 不可以进")
        return attrs
