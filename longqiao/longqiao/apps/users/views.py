
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from django.shortcuts import HttpResponse,redirect,render
from rest_framework import status
from rest_framework.response import Response
from . import constants
from .oauth import Spider


from  . import serializers
# class ImageCodeView(APIView):
#     """
#     图片验证码
#
#     """
#
#     def get(self,request):
#         try:
#             image = Spider(constants.OAUTH_URL)
#             data = image.get_code()
#         except Exception:
#             return Response({"message": "获取验证码异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#         else:
#             return Response(data=data,content_type='image/jpg')

# # url(r'^users/$', views.UserView.as_view()),
# class UserView(CreateAPIView):
#     """
#     用户验证
#     传入参数：
#         StudentID, password, code
#     """
#     serializer_class = serializers.CreateUserSerializer


    # def get(self,request):
    #     image = Spider(constants.OAUTH_URL)
    #     image.get_code(), content_type = 'image/jpg'
    #     return render(request, 'login.html')

from .models import User

class Yz(APIView):
    def get(self,request):
        return render(request, 'login.html')

# url(r'^users/$', views.UserView.as_view()),
class UserView(APIView):
    """
    用户验证
    传入参数：
        StudentID, password, code
    """

    s = Spider(constants.OAUTH_URL)
    def get(self,request):

        try:
            # image = Spider(constants.OAUTH_URL)
            data = self.s.get_code()
        except Exception:
            return Response({"message": "获取验证码异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            # 这里不能是　Response,因为它会对原始数据进行处理
            return HttpResponse(data, content_type='image/jpg')




    def post(self,request):

        StudentID = request.POST.get('StudentID','')
        password = request.POST.get('password','')
        code = request.POST.get('code','')

        # 如果用户要求的字段没有填写完整,则不让进行下一段验证
        if not all([StudentID, password, code]):
            return Response({"message": "数据不完整"}, status=status.HTTP_400_BAD_REQUEST)

        try:
        # 判断
            flag = self.s.login(StudentID, password, code)
        except:
            return Response({"message": "链接超时"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        else:
            if flag == 55555:
                return Response({"message": "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)

            if flag == 66666:
                return Response({"message": "服务器异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            if flag:
                try:
                    StudentID, name, gender, enrollmentDate, birthday, department, sclass, classes = self.s.get_info()
                    print("aaaaaaaaaaaaaaaaaa")


                    user = User.objects.create_user(
                        StudentID=StudentID,
                        password=password,
                        username=name,
                        gender=gender,
                        enrollmentDate = enrollmentDate,
                        birthday = birthday,
                        department = department,
                        sclass = sclass,
                        classes = classes,
                        is_active=True
                    )

                    return Response({"message": "ok"})
                except:
                    return Response({"message": "获取个人信息和创建异常"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            else:
                return Response({"message": "学号或密码错误"},status=status.HTTP_400_BAD_REQUEST)