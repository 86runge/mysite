# coding = UTF-8
from django.urls import path
from .views import IndexView, LoginView, LogoutView, RegisterView, ForgetPasswordView

app_name = 'eshop'

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    # 登录注册模块
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password'),
]
