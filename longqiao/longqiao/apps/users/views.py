import random
import json

from rest_framework.generics import RetrieveAPIView, UpdateAPIView, GenericAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin

from rest_framework.views import APIView
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection

from .serializers import UserSerializer, SiteUserSerializer
from . import constants
from .oauth import Spider
from .models import User, FriendShip
from . import serializers
from .utils import make_token
from .utils import howLongDays
from world.models import WorldCircle
from world.serializers import WorldSerializer, MyWorldSerializer

from fdfs_client.client import Fdfs_client

client = Fdfs_client(constants.FDFS)


class Yz(APIView):
    def get(self, request):
        return render(request, 'login.html')


# url(r'^users/$', views.UserView.as_view()),
class UserView(APIView):
    """
    用户验证
    传入参数：
        StudentID, password, code
    """

    s = Spider(constants.OAUTH_URL)  # 类属性,生成　Spider实例对象

    def get(self, request):

        try:
            data = self.s.get_code()  # 调用验证码
        except Exception:
            return Response({"message": "获取验证码异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            # 这里不能是　Response,因为它会对原始数据进行处理
            return HttpResponse(data, content_type='image/jpg')  # 返回验证码

    def post(self, request):

        print("有人请求了")
        print(request.body)
        # b'name=20160741112&pwd=lch121922028&captcha=16gh'
        StudentID = request.data.get('name', '')
        password = request.data.get('pwd', '')
        code = request.data.get('captcha', '')
        print(StudentID, password, code)
        # 如果用户要求的字段没有填写完整,则不让进行下一段验证
        if not all([StudentID, password, code]):
            return Response({"message": "数据不完整"}, status=status.HTTP_400_BAD_REQUEST)

        # 如果用户已经验证过,则不必再去请求教务系统,直接登陆成功
        try:
            user = authenticate(username=StudentID, password=password)

            if user is not None:
                print(user)

                # 调用　手动签发JWT的函数
                user = make_token(user)

                data = {
                    "id": user.pk,
                    "StudentID": user.StudentID,
                    "username": user.username,
                    "nickname": user.nickname,
                    "department": user.department,
                    "sclass": user.sclass,
                    "classes": user.classes,
                    "avatar": user.avatar,
                    "token": user.token,
                    "is_site": user.is_site
                }

                return Response({"message": "ok", 'data': data}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            pass  # 用户还没有验证

        print("aaaaaa")
        try:
            # 判断
            flag = self.s.login(StudentID, password, code)
        except ConnectionError:
            return Response({"message": "链接超时"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        else:
            if flag == constants.CODE_ERROR:
                return Response({"message": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)

            if flag == constants.SERVICE_ERROR:
                return Response({"message": "服务器异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            if flag:
                try:

                    StudentID, name, gender, enrollmentDate, birthday, department, sclass, classes = self.s.get_info()

                    nickname = '陇桥{0}{1}'.format("小仙女" if gender == "女" else "小魔鬼", random.randint(0, 99999))

                    # 创建用户
                    user = User.objects.create_user(
                        StudentID=StudentID,
                        password=password,
                        username=name,
                        gender=gender,
                        nickname=nickname,
                        enrollmentDate=enrollmentDate,
                        birthday=birthday,
                        realBirthday=birthday[4:],
                        department=department,
                        sclass=sclass,
                        classes=classes,
                    )

                    # 补充生成记录登录状态的token
                    # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    # payload = jwt_payload_handler(user)
                    # token = jwt_encode_handler(payload)
                    # user.token = token
                    #

                    user = make_token(user)

                    data = {
                        "id": user.pk,
                        "StudentID": StudentID,
                        "username": user.username,
                        "nickname": nickname,
                        "department": department,
                        "sclass": sclass,
                        "classes": classes,
                        "avatar": user.avatar,
                        "token": user.token,
                        "is_site": user.is_site  # 是否有权限开通首页
                    }
                    redis_conn = get_redis_connection('courses')

                    if not redis_conn.get(sclass):  # 如果缓存没有该课程，就去请求课程

                        print("我去请求课程了")
                        self.s.get__lessons()  #

                    return Response({"message": "ok", 'results': data}, status=status.HTTP_200_OK)
                except:
                    return Response({"message": "获取个人信息和创建异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            else:
                return Response({"message": "学号或密码错误"}, status=status.HTTP_400_BAD_REQUEST)


# url(r'^user/$', views.UserDetailView.as_view()), # 用户个人信息
class UserDetailView(RetrieveAPIView):
    """
    用户详情
    """
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# url(r'^user/$', views.UserDetailView.as_view()), # 用户主页
class User1DetailView(ListAPIView):
    """
    用户详情
    """

    permission_classes = [IsAuthenticated]

    serializer_class = WorldSerializer

    def get_queryset(self):
        return WorldCircle.objects.filter(Cuser=self.kwargs["pk"])

    # def get_serializer_context(self):
    #     world = WorldCircle.objects.filter(Cuser=self.kwargs["pk"])
    #     self.kwargs['format']= WorldSerializer(world,many=True)

    #
    # def get(self, request, pk):
    #
    #
    #     return self.retrieve(request)

    # def get(self, request, pk):
    #     return self.retrieve(request)
    # def get_object(self):
    #     return User.objects.get(pk=self.request.data['pk'])


# class UserUpdatelView(APIView):
#     # serializer_class = serializers.UserUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user
#
#     def post(self,request):
#
#         user = serializers.UserUpdateSerializer(data=request.data)
#         if user.is_valid():
#             user.save()
#             return Response({'message':'ok','user':user},status=status.HTTP_200_OK)
#         else:
#             return Response({'message':'error'},status=status.HTTP_400_BAD_REQUEST)

# url(r'^info/$', views.UserUpdatelView.as_view()), # 修改用户个人信息
class UserUpdatelView(UpdateAPIView):
    """
    修改个人信息
    """
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# url(r'^longtime/$', views.UserHowLongView.as_view()), # 获取用户在校多少天
class UserHowLongView(APIView):
    """
    获取用户在校多少天
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)

        longDays = howLongDays(request.user.enrollmentDate)

        return Response({'message': 'ok', 'longDays': longDays}, status=status.HTTP_200_OK)


# url(r'^lessons/$', views.LessonsView.as_view()), # 获取课程
class LessonsView(APIView):
    """
    获取课程
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sclass = request.user.sclass

        """获取课程表"""
        redis_conn = get_redis_connection('courses')

        lesson = redis_conn.get(sclass)
        if lesson:  # 如果缓存有该课程

            print("用到缓存了")
            return Response({'message': 'ok', 'lesson': lesson}, status=status.HTTP_200_OK)

        else:
            return Response({'message': '获取课程失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


#     url(r'^relessons/$', views.RefreshLessonsView.as_view()), # 获取课程
class RefreshLessonsView(APIView):
    """
    刷新课程
    """

    permission_classes = [IsAuthenticated]

    s = Spider(constants.OAUTH_URL)  # 类属性,生成　Spider实例对象

    def get(self, request):

        try:
            data = self.s.get_code()  # 调用验证码
        except Exception:
            return Response({"message": "获取验证码异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            # 这里不能是　Response,因为它会对原始数据进行处理
            return HttpResponse(data, content_type='image/jpg')  # 返回验证码

    def post(self, request):

        StudentID = request.data.get('StudentID', '')
        password = request.data.get('password', '')
        code = request.data.get('code', '')

        # 如果用户要求的字段没有填写完整,则不让进行下一段验证
        if not all([StudentID, password, code]):
            return Response({"message": "数据不完整"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 判断
            flag = self.s.login(StudentID, password, code)
        except ConnectionError:
            return Response({"message": "链接超时"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        else:
            if flag == constants.CODE_ERROR:
                return Response({"message": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)

            if flag == constants.SERVICE_ERROR:
                return Response({"message": "服务器异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            if flag:

                print("我去请求课程了")
                self.s.get__lessons()

                sclass = request.user.sclass

                """获取课程表"""
                redis_conn = get_redis_connection('courses')

                lesson = redis_conn.get(sclass)
                if lesson:  # 如果缓存有该课程

                    print("用到新的缓存了")
                    return Response({'message': 'ok', 'lesson': lesson}, status=status.HTTP_200_OK)

                return Response({"message": "ok", })


# url(r'^avatar/$', views.AvatarView.as_view()), # 修改头像
class AvatarView(APIView):
    permission_classes = [IsAuthenticated]

    """
    修改头像
    """

    def post(self, request):
        user = request.user
        avatar = request.data.get("avatar")
        if avatar:
            try:
                ret = client.upload_by_buffer(avatar.read(), file_ext_name=avatar.name.split(".")[-1])
                if ret["Status"] == "Upload successed.":
                    url = constants.StorageIP + ret["Remote file_id"]

                    User.objects.filter(pk=user).update(avatar=url)

                    return Response({'message': "ok", 'avatar': url})

            except:
                return Response({'message': "上传失败"})

        else:
            return Response({'message': "error"}, status=status.HTTP_400_BAD_REQUEST)


class PicView(APIView):
    permission_classes = [IsAuthenticated]

    """
    修改主页背景或头像
    """

    def post(self, request):
        type = request.data.get("type")
        user = request.user

        pic = request.data.get("pic")

        if pic:
            try:
                ret = client.upload_by_buffer(pic.read(), file_ext_name=pic.name.split(".")[-1])
                if ret["Status"] == "Upload successed.":
                    url = constants.StorageIP + ret["Remote file_id"]
                    if type == 'avatar':
                        u = user.avatar = url

                    elif type == 'avatar':
                        u = user.site_pic = url

                    u.save()
                    return Response({'message': "ok", 'pic': url})

            except:
                return Response({'message': "上传失败"})

        else:
            return Response({'message': "error"}, status=status.HTTP_400_BAD_REQUEST)


class UnFollowView(APIView):
    """
    取消关注
    """

    def post(self, request):
        print("***************")
        to_user = request.data.get('to_user')

        user = request.user

        try:
            to_use = User.objects.get(pk=to_user)
            FriendShip.unfollow(user, to_use)


        except:
            return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class FollowView(APIView):
    """
    关注
    """

    def post(self, request):
        to_user = request.data.get('to_user')

        user = request.user

        print(user, to_user)

        try:
            to_use = User.objects.get(pk=to_user)
            FriendShip.follow(user, to_use)


        except:
            return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'ok'}, status=status.HTTP_200_OK)


class FollowerView(APIView):
    """
    关注的人
    """

    def get(self, request):
        user_list = get_follower(request)
        return Response({"message": "ok", 'data': user_list.data}, status=status.HTTP_200_OK)


def get_follower(request, u=None):
    if u:
        user = u
    else:
        user = request.user

    followed_list = FriendShip.user_followed(user)
    user_list = UserSerializer(followed_list, context={'request': request}, many=True)

    print(user_list.data)
    return user_list


class FollowedView(APIView):
    """
    关注我的人
    """

    def get(self, request):
        user_list = get_followed(request)

        print(user_list.data)

        return Response({"message": "ok", 'data': user_list.data}, status=status.HTTP_200_OK)


def get_followed(request, u=None):
    if u:
        user = u
    else:
        user = request.user

    followed_list = FriendShip.user_follower(user)
    user_list = UserSerializer(followed_list, context={'request': request}, many=True)
    # for user in followed_list:
    #     user_list.append({'user_id': user.pk, 'user': user.nickname, 'avatar': user.avatar})

    return user_list


class MySiteView(ListAPIView):
    """我的主页"""

    # permission_classes = [IsAuthenticated]

    serializer_class = MyWorldSerializer

    def get_queryset(self):
        return WorldCircle.objects.filter(Cuser=self.kwargs["pk"]).select_related("Cuser")

    def get(self, request, *args, **kwargs):
        world = super(ListAPIView, self).list(request, *args, **kwargs)
        user = User.objects.get(pk=self.kwargs["pk"])
        # TODO context={'request': request}　必须加
        user_info = SiteUserSerializer(user, context={'request': request})

        fd = get_followed(request, u=user).data  # 关注我的人
        fd_count = len(fd)
        fr = get_follower(request, u=user).data  # 我关注的人
        fr_count = len(fr)

        # print(fd.data)
        # print(fr.data)
        # print(world.data)
        # print(user_info.data)
        return Response({"world": world.data, "userinfo": user_info.data,
                         "fd_count": fd_count, "fd": fd,
                         "fr_count": fr_count, "fr": fr})
