# coding=UTF-8
import datetime

from backend.models import CustomerService
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import logging

logger = logging.getLogger('wxp.%s' % __name__)


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    """
    首页
    """
    template_name = 'backend/backend_index.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class BasicSettingsView(TemplateView):
    """
    基本设置
    """
    template_name = 'backend/basic_settings.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404

    def post(self, request, *args, **kwargs):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'add_customer_service':
                    result = self._add_customer_service(request)
                else:
                    result = {
                        'status': 0,
                        'msg': '请求action错误'
                    }
            else:
                result = {
                    'status': 0,
                    'msg': '请求错误'
                }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _add_customer_service(self, request):
        try:
            if request.POST.get('cs_weixin'):
                img_path = request.POST.get('cs_weixin').split('\\')[-1]
            cs = {
                'cs_phone': request.POST.get('cs_phone'),
                'cs_qq': request.POST.get('cs_qq'),
                'cs_weixin': img_path,
                'cs_note': request.POST.get('cs_note')
            }
            CustomerService.objects.create(**cs)
            result = {
                'status': 0,
                'msg': '添加成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class UserManageView(TemplateView):
    """
    用户管理
    """
    template_name = 'backend/user_manage.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class StaffManageView(TemplateView):
    """
    员工管理
    """
    template_name = 'backend/staff_manage.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class RoleManageView(TemplateView):
    """
    角色管理
    """
    template_name = 'backend/role_manage.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class MessageManageView(TemplateView):
    """
    消息管理
    """
    template_name = 'backend/message_manage.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class GoodsListView(TemplateView):
    """
    商品列表
    """
    template_name = 'backend/goods_list.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class EnterpriseListView(TemplateView):
    """
    企业列表
    """
    template_name = 'backend/enterprise_list.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class OrderListView(TemplateView):
    """
    订单列表
    """
    template_name = 'backend/order_list.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404


@method_decorator(login_required, name='dispatch')
class EshopDecorationView(TemplateView):
    """
    商城装修
    """
    template_name = 'backend/eshop_decoration.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Exception as e:
            logger.exception(e)
            raise Http404
