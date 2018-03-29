# coding=UTF-8
import datetime

from backend.models import CustomerService
from common.utils.utils_file import FileUploadUtil
from common.views import FileOPView
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import logging

from user.models import User

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
            obj = CustomerService.objects.all()
            return render(request, self.template_name, {
                'obj': obj
            })
        except Exception as e:
            logger.exception(e)
            raise Http404

    def post(self, request, *args, **kwargs):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'add_customer_service':
                    return self._add_customer_service(request)
                if action == 'get_customer_service':
                    return self._get_customer_service(request)
                if action == 'update_customer_service':
                    return self._update_customer_service(request)
                if action == 'delete_customer_service':
                    return self._delete_customer_service(request)
                if action == 'switch_customer_service':
                    return self._switch_customer_service(request)
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
            img_path = ''
            file_obj = request.FILES.get("cs_weixin_img")
            file_upload = FileUploadUtil(file_obj, "upload/", 100 * 1024 * 1024)
            flag = file_upload.upload_file(is_new_folder=True)
            if flag:
                # ret = {'status': 200, 'msg': '上传成功', 'file_info': file_upload.file_path}
                img_path = file_upload.file_path
            else:
                pass
                # ret = {'status': 500, 'msg': '上传失败', 'file_info': file_upload.file_path}
            cs = {
                'cs_phone': request.POST.get('cs_phone'),
                'cs_qq': request.POST.get('cs_qq'),
                'cs_weixin': img_path,
                'cs_join_time': datetime.datetime.now(),
                'cs_note': request.POST.get('cs_note')
            }
            CustomerService.objects.create(**cs)
            result = {
                'status': 0,
                'msg': '添加成功',
                'upload_msg': '图片上传成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _delete_customer_service(self, request):
        try:
            id = request.POST.get('id')
            CustomerService.objects.filter(id=id).delete()
            result = {
                'status': 0,
                'msg': '删除成功',
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _switch_customer_service(self, request):
        try:
            id = request.POST.get('id')
            cs = CustomerService.objects.filter(id=id)
            if cs.first().is_active:
                cs.update(is_active=False)
            else:
                cs.update(is_active=True)
            result = {
                'status': 0,
                'msg': '操作成功',
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
            obj = User.objects.all()
            return render(request, self.template_name, {
                'obj': obj
            })
        except Exception as e:
            logger.exception(e)
            raise Http404

    def post(self, request, *args, **kwargs):
        pass


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
