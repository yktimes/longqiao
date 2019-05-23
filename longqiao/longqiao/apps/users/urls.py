from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/', views.UserView.as_view()), # 创建用户

    url(r'^user/$', views.UserDetailView.as_view()), # 用户个人信息
    # 个人主页
    url(r'^mysite/(?P<pk>\d+)/$', views.MySiteView.as_view(), name='my-detail'), # 用户超链接



    url(r'^info/$', views.UserUpdatelView.as_view()), # 修改用户个人信息

    url(r'^longtime/$', views.UserHowLongView.as_view()), # 获取用户在校多长时间

    url(r'^lessons/$', views.LessonsView.as_view()), # 获取课程

    url(r'^relessons/$', views.RefreshLessonsView.as_view()), # 获取课程

    url(r'^avatar/$', views.AvatarView.as_view()), # 修改头像
    # url(r'image_codes/$',views.ImageCodeView.as_view()),
    url(r'yz/$',views.Yz.as_view()),


    url(r'follower/$',views.FollowerView.as_view()), # 我关注的人
    url(r'followed/$',views.FollowedView.as_view()), # 关注我的人

    url(r'unfollow/$',views.UnFollowView.as_view()), # 取消关注
    url(r'follow/$',views.FollowView.as_view()), # 关注


    # url(r'^authorizations/$', obtain_jwt_token),


]
