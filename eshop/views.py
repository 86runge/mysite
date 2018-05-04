# coding=UTF-8
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from django.views.generic import TemplateView

import logging

from goods.models import Goods
from user.models import User

logger = logging.getLogger('wxp.%s' % __name__)


# @method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    """
    首页
    """
    template_name = 'eshop/eshop_index.html'

    def get(self, request, *args, **kwargs):
        try:
            hot_good = Goods.objects.all().order_by('-online_time')[:5]
            return render(request, self.template_name, {
                'hot_good': hot_good
            })
        except Exception as e:
            logger.exception(e)
            raise Http404


class LoginView(TemplateView):
    """
    登录页面
    """
    template_name = 'eshop/eshop_login.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404

    def post(self, request, *args, **kwargs):
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                result = {
                    'status': 0,
                    'msg': '登陆成功'
                }
            else:
                result = {
                    'status': 1,
                    'msg': '用户名或密码不正确'
                }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404


class LogoutView(TemplateView):
    """
    登出页面
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('eshop:index')


class RegisterView(TemplateView):
    """
    注册页面
    """
    template_name = 'eshop/eshop_register.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404

    def post(self, request):
        try:
            user_data = {
                'username': request.POST['username'],
                'password': request.POST['password'],
                'verify_code': request.POST['verify_code'],
                'nick': request.POST['nick'],
                'phone': request.POST['phone'],
                'email': request.POST['email'],
                'date_joined': datetime.datetime.now()
            }
            User.objects.create_user(**user_data)
            return JsonResponse({
                'status': 1
            })
        except Exception as e:
            logger.exception(e)
            raise Http404


class ForgetPasswordView(TemplateView):
    """
    忘记密码
    """
    template_name = 'eshop/forget_password.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404

    def post(self, request):
        try:
            new_pwd = request.POST.get('password')
            if new_pwd:
                new_pwd = make_password(new_pwd)
            username = request.POST.get('username')
            User.objects.filter(username=username).update(password=new_pwd)
            result = {
                'status': 1,
                'msg': '修改成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class MemberCenter(TemplateView):
    """
    会员中心
    """
    template_name = 'eshop/member_center.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404
