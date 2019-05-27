from rest_framework import serializers

from .models import Post, Category, PostImages

from users.serializers import UserSerializer

from drf_haystack.serializers import HaystackSerializer

from .search_indexes import Postindex


class PostListSerializer(serializers.ModelSerializer):
    """
    贴吧展示
    """
    url = serializers.HyperlinkedIdentityField(view_name='post-detail')
    # owner = serializers.StringRelatedField(label='昵称')
    Cuser = UserSerializer()
    postimages_set = serializers.SlugRelatedField(read_only=True, slug_field='ImagesUrl', many=True)  # 新增

    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = (
        'url', 'Cuser', "postimages_set", 'title', 'desc', 'category', 'created_time', 'comment_count', 'up_count')

        extra_kwargs = {

            'id': {'read_only': True}
        }


class ImagesSerializer(serializers.ModelSerializer):
    """
    贴吧照片序列化器
    """

    # img_conn = ConfessionWallSerializer()

    class Meta:
        model = PostImages
        fields = ('ImagesUrl', 'img_conn')


class PostDetailSerializer(serializers.ModelSerializer):
    """
    帖子详情展示
    """
    Cuser = UserSerializer()
    postimages_set = serializers.SlugRelatedField(read_only=True, slug_field='ImagesUrl', many=True)  # 新增

    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = (
            'Cuser', "postimages_set", 'title', 'content', 'category', 'created_time', 'comment_count', 'up_count')

        extra_kwargs = {

            'id': {'read_only': True}
        }


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

        fields = ('title', 'content', 'category', 'Cuser', 'created_time')

        extra_kwargs = {
            "created_time": {'required': False},
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

        if len(desc)>50:

            post.desc = desc[:50] + " ..."
        else:
            post.desc = desc
        post.save()

        return post


class POSTIndexSerializer(HaystackSerializer):
    """
    POST索引结果数据序列化器
    """
    object = PostListSerializer(read_only=True)

    class Meta:
        index_classes = [Postindex]
        fields = ('text', object)
