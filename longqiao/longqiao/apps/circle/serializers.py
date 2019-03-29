from rest_framework import serializers
from .models import WorldImages,WorldCircle
from users.serializers import UserSerializer

import re




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
    Cuser = UserSerializer()
    # worldimages_set = serializers.PrimaryKeyRelatedField(read_only=True,many=True)  # 新增
    worldimages_set = serializers.SlugRelatedField(read_only=True, slug_field='ImagesUrl', many=True)  # 新增

    # worldimages_set = ConfessionImagesSerializer()

    class Meta:
        model = WorldCircle
        fields = ('id', 'content',  'create_time', 'worldimages_set', 'Cuser','comment_count','up_count')

        extra_kwargs = {

            'id': {'read_only': True}
        }


class CreateWorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldCircle
        fields = ('content',  'Cuser')



    # def create(self, validated_data):
    #     """
    #     创建表白墙
    #     """
    #     print(validated_data)
    #
    #     wall = super().create(validated_data)
    #
    #     return wall

# class CreateConfessionWallSerializer(serializers.Serializer):
#     id = serializers.IntegerField(label='ID',read_only=True)
#     content = serializers.CharField(label='表白内容',max_length=255)
#     is_anonymity = serializers.BooleanField(required=False,label='是否匿名')
#
#     images =serializers.ImageField(required=False)
#
#     # # confessionimages_set = serializers.PrimaryKeyRelatedField(many=True)  # 新增
#     # confessionimages_set = serializers.SlugRelatedField(
#     #     many=True,
#     #     read_only=False,
#     #     slug_field='images'
#     # )
#     # class Meta:
#     #
#     #     model = ConfessionWall
#     def validate_images(self, value):
#         if value:
#
#             return value
#
#     def create(self, validated_data):
#         """
#         创建表白墙
#         """
#
#         wall = super().create(validated_data)
#
#
#         return wall

# # 创建表白墙评论　序列化器
# class CreateWallCommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WallComment
#         fields = ('wall', 'author_id', 'content','parent_id')
#
#         extra_kwargs = {
#             'parent_id': {'required': False,},
#         }
#
#     def validate_content(self, value):
#         """评论内容，不能为空"""
#         if not value.strip():
#             raise serializers.ValidationError('评论不能为空')
#
#
#         return value