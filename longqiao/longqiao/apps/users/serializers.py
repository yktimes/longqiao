from rest_framework import serializers
from .models import User
import re


from . import constants
from .oauth import Spider

class UserSerializer(serializers.ModelSerializer):
    """
    创建用户序列化器
    """


    class Meta:
        model = User
        fields = ('id','StudentID', 'nickname','department')

    # def validate_mobile(self, value):
    #     """验证手机号"""
    #     if not re.match(r'^1[3-9]\d{9}$', value):
    #         raise serializers.ValidationError('手机号格式错误')
    #
    #     # 手机号是否重复
    #     count = User.objects.filter(mobile=value).count()
    #     if count > 0:
    #         raise serializers.ValidationError('手机号已存在')
    #
    #     return value
    #
    # def validate_allow(self, value):
    #     """检验用户是否同意协议"""
    #     if value != 'true':
    #         raise serializers.ValidationError('请同意用户协议')
    #     return value

    # def validate(self, data):
    #
    #     autho = Spider(constants.OAUTH_URL)
    #
    #     # 判断
    #     flag = autho.login(data['StudentID'],data['password'],data['code'])
    #
    #
    #     if flag==55555:
    #         raise serializers.ValidationError('短信验证码错误')
    #     if flag==66666:
    #         raise serializers.ValidationError('服务器错误')
    #     if flag:
    #         StudentID,name,gender,enrollmentDate,birthday,department,sclass,classes = autho.get_info()
    #         data.StudentID=StudentID
    #         data.name=name
    #         data.gender=gender
    #         data.enrollmentDate=enrollmentDate
    #         data.birthday = birthday
    #         data.department=department
    #         data.sclass=sclass
    #         data.classes=classes
    #
    #         return data
    #     else:
    #         raise serializers.ValidationError('学号或密码错误')
    #
    #
    #
    #
    #
    #
    # def create(self, validated_data):
    #     """
    #     创建用户
    #     """
    #     # 移除数据库模型类中不存在的属性
    #
    #     del validated_data['code']
    #
    #     user = super().create(validated_data)
    #
    #     # 调用django的认证系统加密密码
    #     user.set_password(validated_data['password'])
    #     user.save()
    #
    #     return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('id','StudentID', 'nickname','avatar','gender','department', 'email', 'sclass','mobile')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户修改信息序列化器
    """
    class Meta:
        model = User
        fields = ('nickname', 'email', 'mobile')

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')

        # 手机号是否重复
        count = User.objects.filter(mobile=value).count()
        if count > 0:
            raise serializers.ValidationError('手机号已存在')

        return value


    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #
    #     return user