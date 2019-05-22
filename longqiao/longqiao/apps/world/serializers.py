from rest_framework import serializers
from .models import ConfessionImages
from .models import ConfessionWall
from .models import WallComment

from .models import WorldImages
from .models import WorldCircle
from .models import Site
from .models import SiteImages

from users.serializers import UserSerializer

import re



class SiteImagesSerializer(serializers.ModelSerializer):
    """
    首页照片序列化器
    """

    # img_conn = ConfessionWallSerializer()

    class Meta:
        model = SiteImages
        fields = ('ImagesUrl', 'img_conn')



class SiteSerializer(serializers.ModelSerializer):
    """
    首页展示序列化器　　详情和列表
    """

    url = serializers.HyperlinkedIdentityField(view_name='site-detail')

    Cuser = UserSerializer()

    siteimages_set = serializers.SlugRelatedField(read_only=True, slug_field='ImagesUrl', many=True)  # 新增

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Site
        fields = (
        'url', 'id', 'content', 'tag', 'create_time', 'Cuser', 'siteimages_set', 'comment_count',
        'up_count')

        extra_kwargs = {

            'id': {'read_only': True}
        }

class CreateSiteSerializer(serializers.ModelSerializer):
    """创建首页序列化器"""

    class Meta:
        model = Site
        fields = ('content', 'Cuser','is_top','tag')

        extra_kwargs = {

            'is_top': {'read_only': False},
            'tag': {'read_only': False}
        }






class ConfessionImagesSerializer(serializers.ModelSerializer):
    """
    表白墙照片序列化器
    """

    # img_conn = ConfessionWallSerializer()

    class Meta:
        model = ConfessionImages
        fields = ('ImagesUrl', 'img_conn')


class ConfessionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfessionWall

    # def create(self, validated_data):
    #     """
    #     创建表白墙照片
    #     """
    #     print(validated_data)
    #
    #     img = super().create(validated_data)
    #
    #     return img


class ConfessionWallSerializer(serializers.ModelSerializer):
    """
    表白墙展示序列化器　　详情和列表
    """

    url = serializers.HyperlinkedIdentityField(view_name='walls-detail')

    Cuser = UserSerializer()
    # confessionimages_set = serializers.PrimaryKeyRelatedField(read_only=True,many=True)  # 新增
    # confessionimages_set = serializers.PrimaryKeyRelatedField(read_only=True)
    confessionimages_set = serializers.SlugRelatedField(read_only=True, slug_field='ImagesUrl', many=True)  # 新增
    # confessionimages_set = serializers.IntegerField()
    # confessionimages_set = ConfessionImagesSerializer()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ConfessionWall
        fields = (
        'url', 'id', 'content', 'is_anonymity', 'create_time', 'Cuser', 'confessionimages_set', 'comment_count',
        'up_count')

        extra_kwargs = {
            'is_anonymity': {'required': False},
            'id': {'read_only': True}
        }


class ImagesSerializer(serializers.ModelSerializer):
    """
    表白墙照片序列化器
    """

    # img_conn = ConfessionWallSerializer()

    class Meta:
        model = ConfessionImages
        fields = ('ImagesUrl', 'img_conn')


class CreateConfessionWallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfessionWall
        fields = ('content', 'is_anonymity', 'Cuser')

        extra_kwargs = {
            'is_anonymity': {'required': False, },

        }

    # def create(self, validated_data):
    #     """
    #     创建表白墙
    #     """
    #     print(validated_data)
    #
    #     wall = super().create(validated_data)
    #
    #     return wall



# 创建表白墙评论　序列化器
class CreateWallCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WallComment
        fields = ('wall', 'author_id', 'content', 'parent_id')

        extra_kwargs = {
            'parent_id': {'required': False, },
        }

    def validate_content(self, value):
        """评论内容，不能为空"""
        if not value.strip():
            raise serializers.ValidationError('评论不能为空')

        return value


class WorldImagesSerializer(serializers.ModelSerializer):
    """
    世界圈照片序列化器
    """

    # img_conn = ConfessionWallSerializer()

    class Meta:
        model = WorldImages
        fields = ('ImagesUrl', 'img_conn')

    # def create(self, validated_data):
    #     """
    #     创建表白墙照片
    #     """
    #     print(validated_data)
    #
    #     img = super().create(validated_data)
    #
    #     return img


class WorldSerializer(serializers.ModelSerializer):
    """
    世界圈展示序列化器


    """
    url = serializers.HyperlinkedIdentityField(view_name='world-detail')

    Cuser = UserSerializer()
    # worldimages_set = serializers.PrimaryKeyRelatedField(read_only=True,many=True)  # 新增
    worldimages_set = serializers.SlugRelatedField(read_only=True, slug_field='ImagesUrl', many=True)  # 新增

    # worldimages_set = ConfessionImagesSerializer()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = WorldCircle
        fields = ('url', 'id', 'content', 'create_time', 'worldimages_set', 'Cuser', 'comment_count', 'up_count')

        extra_kwargs = {

            'id': {'read_only': True}
        }


class CreateWorldSerializer(serializers.ModelSerializer):
    """创建动态序列化器"""

    class Meta:
        model = WorldCircle
        fields = ('content', 'Cuser')
