# coding=UTF-8
from django.http import Http404
from django.shortcuts import render

from django.views.generic import TemplateView

import logging

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


class LogoutView(TemplateView):
    """
    登录页面
    """


class RegisterView(TemplateView):
    """
    登录页面
    """
    template_name = 'eshop/eshop_register.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404
