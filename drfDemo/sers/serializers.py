from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from students.models import Student

"""
serializers 是drf给开发者调用的序列化模块
里面声明了所有的可用序列化的基类
serializer 序列化基类 drf 所有的 许了话器类都必须继承于serializer
ModelSerializer 模型下序列化器类，是序列化基类的子类，在工作中，除了serializer基类意外 最常用的序列化器类基类

"""


def check_classnum(data):
    """外部验证函数"""
    if len(data) != 3:
        raise serializers.ValidationError(detail="格式不正确 必须v是三位数", code="check_classnum")

    # 验证完毕 必须返回 数据 不然 数据等于None  验证结果中没有该数据
    return data


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
    # 允许为空 单独指定一个方法 validators 是外部函数验证选项 嵌套列表 列表的字段是函数 不能是字符串
    classNum = serializers.CharField(validators=[check_classnum])
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
        # 输入密码 和确认密码

        return attrs

    def validate_name(self, data):
        """
        验证单个字段
        方法名的格式必须v以validate_<字段名> 为名词 否则 序列化识别不到！
        validate 开头的方法 户自动被 is_valid调用
        """
        if data in ["python", "django"]:
            # 在序列化中 验证失败可以通过抛出异常 的方式 来告知 is valid
            raise serializers.ValidationError(detail="学生名不能是python 或者 django ", code="validate_name")
        # 验证完数据后 必须v返回数据 否则最终的验证结果中 就不会出现该数据
        return data

    def create(self, validated_data):
        """
        添加数据
        添加数据操作 就自动实现了从字典变成模型对象的过程
        方法名固定为 create
        固定参数 为： validated_data 就是验证成功后的结果
        """
        student = Student.objects.create(**validated_data)
        return student

    def update(self, instance, validated_data):
        """
        更新数据操作
        更新数据操作 就自动实现了从字典变成模型对象的过程
        方法名固定为：update
        固定参数 instance 实现序列化对象时，必须v传入的模型对象
        固定参数 validated_data 就是严惩成功后的结果
        """

        # # todo: 太麻烦 直接用 for 循环 kv 写入
        # instance.name = validated_data["name"]
        # instance.age = validated_data["age"]
        # instance.gender = validated_data["gender"]
        # instance.classNum = validated_data["classNum"]
        # instance.description = validated_data["description"]
        # # 调用模型对象的save方法 和views视图中的serializers.save 不是一个方法
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()  # 调用模型对象中的save方法 和 视图中的serializers的save 不是一个方法

        return instance


class StudentModelSerializer(serializers.ModelSerializer):
    # 1. 转换的字段声明
    # 字段名 =  选项类型(选项=选项值)

    # 可以手动添加   自定义字段
    # nickname = serializers.CharField(read_only=True, default="abc")
    nickname = serializers.CharField(required=False,allow_null=True,allow_blank=True)

    # 2. 如果当前序列化继承的是 modelserializer 则需要声明调用的模型类型

    class Meta:
        model = Student
        # 这里表明的是字段
        fields = ["id", "name", "age", "gender", "nickname"]
        # fields ="__all__" # 字符串只能是这个 代表所有字段
        # 表示的是只读字段 表示设置的字段 只会在序列化阶段显示
        read_only_fields=["id","nickname"]

        extra_kwargs = {
            #     选填 字段额外生命
            #     字段名：{
            #     "选项名":"选项值"
            #     }
            "age": {
                "min_value": 5,
                "max_value": 20,
                "error_messages": {
                    "min_value": "年龄最小不能小于5",
                    "max_value": "年龄最大不能大于20",
                },
            }
        }
    # 不用手动写 create 也能自动入库
    # # 3. 验证代码的对象方法
    # def create(self, validated_data):
    #     # 密码加密
    #     validated_data["password"] = make_password(validated_data["password"])
    #     super().create(validated_data)
    #     pass

    # 4. 模型操作的方法

