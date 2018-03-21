# coding=UTF-8
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import render, redirect

from django.views.generic import TemplateView

import logging

from user.form import UserRegisterForm, UserLoginForm
from user.models import User

logger = logging.getLogger('wxp.%s' % __name__)


class IndexView(TemplateView):
    """
    首页
    """
    template_name = 'eshop/eshop_index.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
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
            userform = UserLoginForm(request.POST)
            if userform.is_valid():
                username = userform.cleaned_data['username']
                password = userform.cleaned_data['password']
                user = authenticate(request=request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('eshop:index')
            else:
                return render(request, self.template_name, {
                    'show_error': True
                })
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
            userform = UserRegisterForm(request.POST)
            if userform.is_valid():
                username = userform.cleaned_data['username']
                password = userform.cleaned_data['password']
                verify_code = userform.cleaned_data['verify_code']
                nick = userform.cleaned_data['nick']
                phone = userform.cleaned_data['phone']
                email = userform.cleaned_data['email']
                User.objects.create(
                    username=username,
                    password=password,
                    verify_code=verify_code,
                    nick=nick,
                    phone=phone,
                    email=email
                )
                return redirect('eshop:index')
            else:
                return render(request, self.template_name, {
                    'show_error': True
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

# class ResetPwdView(View):
#     '''重设密码'''
#
#     def get(self, request):
#         pass
#
#     def post(self, request):
#
#         if 'action' in request.POST:
#             action = request.POST.get('action')
#
#             if action == 'reset_pwd':
#                 result = self._handle_reset_pwd(request)
#             else:
#                 result = {
#                     'status': 0,
#                     'msg': '请求action错误'
#                 }
#         else:
#             result = {
#                 'status': 0,
#                 'msg': '请求错误'
#             }
#         return result
#
#     def _handle_reset_pwd(self, request):
#         try:
#             new_pwd = request.POST.get('confirm_pwd')
#             if new_pwd:
#                 new_pwd = make_password(new_pwd)
#             user = request.user
#             User.objects.filter(username=user).update(password=new_pwd)
#             result = {
#                 'status': 1,
#                 'msg': '修改成功'
#             }
#         except Exception as e:
#             logger.error("SerialOperate post raise exception %s" % e)
#             result = {
#                 'status': 0,
#                 'msg': '网络错误, 请刷新重试'
#             }
#         return JsonResponse(result)
