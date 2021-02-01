from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    # 借助于jwt完成登录请求
    path("login/", obtain_jwt_token),

    path("captcha/", views.CaptchaAPIView.as_view()),
    path("users/", views.UserAPIView.as_view()),
    # 获取短信验证码 并催乳redis
    path("message/", views.MessageAPIView.as_view()),
    # 校验手机号是否可登录
    path("phone/", views.MessageRegisterAPIView.as_view()),
    # 为可登录手机号签发token
    path('login2/',views.MessageLoginAPIView.as_view())
]
