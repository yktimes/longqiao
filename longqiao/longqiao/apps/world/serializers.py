from rest_framework import serializers
from .models import ConfessionImages,ConfessionWall
from users.serializers import UserSerializer
import re



# class ConfessionWallSerializer(serializers.Serializer):
#
#     id = serializers.IntegerField(label='ID',read_only=True)
#     content = serializers.CharField(label='表白内容',max_length=255)
#     is_anonymity = serializers.BooleanField(required=False,label='是否匿名')
#     confessionimages_set = serializers.PrimaryKeyRelatedField(read_only=True,many=True)  # 新增

class ConfessionImagesSerializer(serializers.ModelSerializer):
    """
    创建表白墙序列化器
    """


    # img_conn = ConfessionWallSerializer()

    class Meta:
        model = ConfessionImages
        fields = ('images')

class ConfessionWallSerializer(serializers.ModelSerializer):
    """
    创建表白墙序列化器
    """
    Cuser = UserSerializer()
    confessionimages_set = serializers.PrimaryKeyRelatedField(read_only=True,many=True)  # 新增
    # confessionimages_set = serializers.SlugRelatedField(read_only=True,slug_field='images',many=True)  # 新增
    # confessionimages_set = ConfessionImagesSerializer()
    class Meta:
        model = ConfessionWall
        fields = ('id','content','is_anonymity','create_time','confessionimages_set','Cuser')

        extra_kwargs = {
            'is_anonymity': {'required': False},
             'id':{'read_only':True}
        }

        #
    # def validate(self, data):
    #
    #     return data
    #
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

