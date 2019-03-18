
from rest_framework.generics import RetrieveAPIView,UpdateAPIView
from rest_framework.views import APIView
from django.shortcuts import HttpResponse,redirect,render
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from . import constants
from .oauth import Spider
from .models import User
from . import serializers

import random


class Yz(APIView):
    def get(self,request):
        return render(request, 'login.html')



def make_token(user):
    """
    生成　token
    :param user: user对象
    :return: 增加了token的user对象
    """
    # 补充生成记录登录状态的token
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    user.token = token
    user.save()


    print('user',user)
    return user

# url(r'^users/$', views.UserView.as_view()),
class UserView(APIView):
    """
    用户验证
    传入参数：
        StudentID, password, code
    """

    s = Spider(constants.OAUTH_URL) # 类属性,生成　Spider实例对象

    def get(self,request):

        try:
            data = self.s.get_code() #　调用验证码
        except Exception:
            return Response({"message": "获取验证码异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            # 这里不能是　Response,因为它会对原始数据进行处理
            return HttpResponse(data, content_type='image/jpg') # 返回验证码




    def post(self,request):

        StudentID = request.POST.get('StudentID','')
        password = request.POST.get('password','')
        code = request.POST.get('code','')

        # 如果用户要求的字段没有填写完整,则不让进行下一段验证
        if not all([StudentID, password, code]):
            return Response({"message": "数据不完整"}, status=status.HTTP_400_BAD_REQUEST)


        # 如果用户已经验证过,则不必再去请求教务系统,直接登陆成功
        try:
            user = User.objects.get(StudentID=StudentID)
            if user.check_password(password):

                # 补充生成记录登录状态的token
                # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                # payload = jwt_payload_handler(user)
                # token = jwt_encode_handler(payload)
                # user.token = token


                # 调用　手动签发JWT的函数
                user = make_token(user)


                return Response({"message": "已经验证过的身份",'token':user.token,'学号':user.StudentID}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass # 用户还没有验证



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

                    nickname = '陇桥%05d' % (random.randint(0, 99999))



                    # 创建用户
                    user = User.objects.create_user(
                        StudentID=StudentID,
                        password=password,
                        username=name,
                        gender=gender,
                        nickname=nickname,
                        enrollmentDate = enrollmentDate,
                        birthday = birthday,
                        department = department,
                        sclass = sclass,
                        classes = classes,
                        is_active=True
                    )

                    # 补充生成记录登录状态的token
                    # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    # payload = jwt_payload_handler(user)
                    # token = jwt_encode_handler(payload)
                    # user.token = token
                    #
                    # user.save()

                    user = make_token(user)

                    return Response({"message": "ok",'token':user.token})
                except:
                    return Response({"message": "获取个人信息和创建异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            else:
                return Response({"message": "学号或密码错误"},status=status.HTTP_400_BAD_REQUEST)


# url(r'^user/$', views.UserDetailView.as_view()), # 用户个人信息
class UserDetailView(RetrieveAPIView):
    """
    用户详情
    """
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

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

