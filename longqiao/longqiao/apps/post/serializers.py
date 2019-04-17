from rest_framework import serializers

from .models import Post, Category


# from users.serializers import UserSerializer


class PostListSerializer(serializers.ModelSerializer):
    """
    贴吧展示
    """

    owner = serializers.StringRelatedField(label='昵称')


    class Meta:
        model = Post
        fields = ('owner','title', 'desc', 'category', 'created_time', 'comment_count', 'up_count')


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

        fields = ('title', 'content', 'category', 'owner', 'created_time')

        extra_kwargs = {

        }

    def validate_title(self, value):
        """
        验证标题
        """
        if len(value.strip()) == 0:
            raise serializers.ValidationError('标题不能为空')
        return value

    def validate_content(self, value):
        """
        验证内容
        """
        if len(value.strip()) == 0:
            raise serializers.ValidationError('内容不能为空')
        return value

    def create(self, validated_data):

        desc = validated_data['content']

        post = super().create(validated_data)

        post.desc = desc[:36] + "..."
        post.save()



        return post


from drf_haystack.serializers import HaystackSerializer

from . search_indexes import Postindex

class POSTIndexSerializer(HaystackSerializer):
    """
    POST索引结果数据序列化器
    """
    object = PostListSerializer(read_only=True)

    class Meta:
        index_classes = [Postindex]
        fields = ('text',object)