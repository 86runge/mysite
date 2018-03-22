# coding=UTF-8
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from django.views.generic import TemplateView

import logging

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
            username = request.POST['username']
            password = request.POST['password']
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


# @method_decorator(login_required, name='dispatch')
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
