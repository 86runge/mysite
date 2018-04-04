# coding=UTF-8
import datetime
import logging

from backend.models import CustomerService, MessageManage, MESSAGE_GROUP
from common.utils.utils_file import FileUploadUtil
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import ProtectedError
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from user.models import User, Staff, Department, Role, Group, Permission

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
                # if action == 'get_customer_service':
                #     return self._get_customer_service(request)
                # if action == 'update_customer_service':
                #     return self._update_customer_service(request)
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
        try:
            if 'action' in request.POST:
                action = request.POST.get('action')
                # if action == 'add_user':
                #     return self._add_user(request)
                if action == 'get_user':
                    return self._get_user(request)
                if action == 'update_user':
                    return self._update_user(request)
                if action == 'delete_user':
                    return self._delete_user(request)
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

    def _get_user(self, request):
        try:
            id = request.POST.get('id')
            user = User.objects.filter(id=id)[0]
            user_result = {
                'username': user.username,
                'password': user.password,
                'nick': user.nick,
                'phone': user.phone,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
            }
            return JsonResponse(user_result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _update_user(self, request):
        try:
            id = request.POST.get('id')
            user = {
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'nick': request.POST.get('nick'),
                'phone': request.POST.get('phone'),
                'email': request.POST.get('email'),
                'is_staff': request.POST.get('is_staff') or True,
                'is_active': request.POST.get('is_active'),
                'date_joined': datetime.datetime.now()
            }
            User.objects.filter(id=id).update(**user)
            result = {
                'status': 0,
                'msg': '修改成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _delete_user(self, request):
        try:
            id = request.POST.get('id')
            User.objects.filter(id=id).delete()
            result = {
                'status': 0,
                'msg': '删除成功'
            }
            return JsonResponse(result)
        except ProtectedError:
            result = {
                'status': 1,
                'msg': '该用户正在被使用，无法删除'
            }
            return JsonResponse(result)
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
            obj = Staff.objects.all()
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
                if action == 'add_staff':
                    return self._add_staff(request)
                if action == 'get_staff':
                    return self._get_staff(request)
                if action == 'update_staff':
                    return self._update_staff(request)
                if action == 'delete_staff':
                    return self._delete_staff(request)
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

    def _add_staff(self, request):
        try:
            user = {
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'nick': request.POST.get('nick'),
                'phone': request.POST.get('phone'),
                'email': request.POST.get('email'),
                'is_active': request.POST.get('is_active'),
                'date_joined': datetime.datetime.now()
            }
            staff = {
                'department': request.POST.get('department'),
                'role': request.POST.get('role'),
                'superior': request.POST.get('superior')
            }
            _user = User.objects.create_user(**user)
            staff['user'] = _user
            Staff.objects.create(**staff)
            result = {
                'status': 0,
                'msg': '添加成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _get_staff(self, request):
        try:
            id = request.POST.get('id')
            staff = Staff.objects.filter(id=id)[0]
            user = User.objects.filter(id=staff.user_id)[0]
            staff_result = {
                'username': user.username,
                'password': user.password,
                'nick': user.nick,
                'phone': user.phone,
                'email': user.email,
                'is_active': user.is_active,
                'department': staff.department,
                'role': staff.role,
                'superior': staff.superior,
            }
            return JsonResponse(staff_result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _update_staff(self, request):
        try:
            user = {
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'nick': request.POST.get('nick'),
                'phone': request.POST.get('phone'),
                'email': request.POST.get('email'),
                'is_active': request.POST.get('is_active'),
                'date_joined': datetime.datetime.now()
            }
            staff = {
                'department': request.POST.get('department'),
                'role': request.POST.get('role'),
                'superior': request.POST.get('superior')
            }
            staff_id = request.POST.get('id')
            user_id = Staff.objects.filter(id=staff_id)[0].user_id
            Staff.objects.filter(id=staff_id).update(**staff)
            User.objects.filter(id=user_id).update(**user)
            result = {
                'status': 0,
                'msg': '修改成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _delete_staff(self, request):
        try:
            result = {
                'status': 0,
                'msg': '删除成功'
            }
            return JsonResponse(result)
        except ProtectedError:
            result = {
                'status': 1,
                'msg': '该员工正在被使用，无法删除'
            }
            return JsonResponse(result)
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
            content_type = ContentType.objects.all()
            permission = Permission.objects.all()
            group = Group.objects.all()
            role = Role.objects.all()
            department = Department.objects.all()
            return render(request, self.template_name, {
                'content_type': content_type,
                'permission': permission,
                'group': group,
                'role': role,
                'department': department,
            })
        except Exception as e:
            logger.exception(e)
            raise Http404

    def post(self, request, *args, **kwargs):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action')
                # 权限操作
                if action == 'add_permission':
                    return self._add_permission(request)
                if action == 'get_permission':
                    return self._get_permission(request)
                if action == 'update_permission':
                    return self._update_permission(request)
                if action == 'delete_permission':
                    return self._delete_permission(request)
                # 群组操作
                if action == 'add_group':
                    return self._add_group(request)
                if action == 'get_group':
                    return self._get_group(request)
                if action == 'update_group':
                    return self._update_group(request)
                if action == 'delete_group':
                    return self._delete_group(request)
                # 角色操作
                if action == 'add_role':
                    return self._add_role(request)
                if action == 'get_role':
                    return self._get_role(request)
                if action == 'update_role':
                    return self._update_role(request)
                if action == 'delete_role':
                    return self._delete_role(request)
                # 部门操作
                if action == 'add_department':
                    return self._add_department(request)
                if action == 'get_department':
                    return self._get_department(request)
                if action == 'update_department':
                    return self._update_department(request)
                if action == 'delete_department':
                    return self._delete_department(request)
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

    def _add_permission(self, request):
        try:
            permission = {
                'name': request.POST.get('name'),
                'content_type_id': request.POST.get('content_type'),
                'codename': request.POST.get('codename'),
            }
            Permission.objects.create(**permission)
            result = {
                'status': 0,
                'msg': '添加成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _get_permission(self, request):
        try:
            id = request.POST.get('id')
            permission = Permission.objects.filter(id=id)[0]
            content_type = ContentType.objects.filter(id=permission.content_type_id)[0]
            permission_result = {
                'name': permission.name,
                'content_type': content_type.id,
                'codename': permission.codename,
            }
            return JsonResponse(permission_result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _update_permission(self, request):
        try:
            id = request.POST.get('id')
            permission = {
                'name': request.POST.get('name'),
                'content_type_id': request.POST.get('content_type'),
                'codename': request.POST.get('codename'),
            }
            Permission.objects.filter(id=id).update(**permission)
            result = {
                'status': 0,
                'msg': '修改成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _delete_permission(self, request):
        try:
            id = request.POST.get('id')
            Permission.objects.filter(id=id).delete()
            result = {
                'status': 0,
                'msg': '删除成功'
            }
            return JsonResponse(result)
        except ProtectedError:
            result = {
                'status': 1,
                'msg': '该权限正在被使用，无法删除'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _add_group(self, request):
        try:
            group = {
                'name': request.POST.get('name'),
                'created': datetime.datetime.now(),
                'is_active': request.POST.get('is_active'),
                'notes': request.POST.get('notes')
            }
            Group.objects.create(**group)
            result = {
                'status': 0,
                'msg': '添加成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _get_group(self, request):
        try:
            id = request.POST.get('id')
            group = Group.objects.filter(id=id)[0]
            group_result = {
                'name': group.name,
                # 'permissions': group.permissions,
                'is_active': group.is_active,
                'notes': group.notes,
            }
            return JsonResponse(group_result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _update_group(self, request):
        try:
            id = request.POST.get('id')
            group = {
                'name': request.POST.get('name'),
                'created': datetime.datetime.now(),
                'is_active': request.POST.get('is_active'),
                'notes': request.POST.get('notes')
            }
            Group.objects.filter(id=id).update(**group)
            result = {
                'status': 0,
                'msg': '修改成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _delete_group(self, request):
        try:
            id = request.POST.get('id')
            Group.objects.filter(id=id).delete()
            result = {
                'status': 0,
                'msg': '删除成功'
            }
            return JsonResponse(result)
        except ProtectedError:
            result = {
                'status': 1,
                'msg': '该群组正在被使用，无法删除'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _add_role(self, request):
        try:
            role = {
                'name': request.POST.get('name'),
                # 'groups': request.POST.get('groups'),
                'created': datetime.datetime.now(),
                'is_active': request.POST.get('is_active'),
                'notes': request.POST.get('notes')
            }
            Role.objects.create(**role)
            result = {
                'status': 0,
                'msg': '添加成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _get_role(self, request):
        try:
            id = request.POST.get('id')
            role = Role.objects.filter(id=id)[0]
            role_result = {
                'name': role.name,
                # 'groups': role.groups,
                'is_active': role.is_active,
                'notes': role.notes,
            }
            return JsonResponse(role_result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _update_role(self, request):
        try:
            id = request.POST.get('id')
            role = {
                'name': request.POST.get('name'),
                'created': datetime.datetime.now(),
                'is_active': request.POST.get('is_active'),
                'notes': request.POST.get('notes')
            }
            Role.objects.filter(id=id).update(**role)
            result = {
                'status': 0,
                'msg': '修改成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _delete_role(self, request):
        try:
            id = request.POST.get('id')
            Role.objects.filter(id=id).delete()
            result = {
                'status': 0,
                'msg': '删除成功'
            }
            return JsonResponse(result)
        except ProtectedError:
            result = {
                'status': 1,
                'msg': '该角色正在被使用，无法删除'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _add_department(self, request):
        try:
            department = {
                'name': request.POST.get('name'),
                'created': datetime.datetime.now(),
                'is_active': request.POST.get('is_active'),
                'notes': request.POST.get('notes')
            }
            Department.objects.create(**department)
            result = {
                'status': 0,
                'msg': '添加成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _get_department(self, request):
        try:
            id = request.POST.get('id')
            department = Department.objects.filter(id=id)[0]
            department_result = {
                'name': department.name,
                'is_active': department.is_active,
                'notes': department.notes,
            }
            return JsonResponse(department_result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _update_department(self, request):
        try:
            id = request.POST.get('id')
            department = {
                'name': request.POST.get('name'),
                'created': datetime.datetime.now(),
                'is_active': request.POST.get('is_active'),
                'notes': request.POST.get('notes')
            }
            Department.objects.filter(id=id).update(**department)
            result = {
                'status': 0,
                'msg': '修改成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _delete_department(self, request):
        try:
            id = request.POST.get('id')
            Department.objects.filter(id=id).delete()
            result = {
                'status': 0,
                'msg': '删除成功'
            }
            return JsonResponse(result)
        except ProtectedError:
            result = {
                'status': 1,
                'msg': '该部门正在被使用，无法删除'
            }
            return JsonResponse(result)
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
            msg = MessageManage.objects.all()
            msg_group = {}
            msg_group['msg_choice'] = MESSAGE_GROUP
            return render(request, self.template_name, {
                'msg': msg,
                'msg_group': msg_group
            })
        except Exception as e:
            logger.exception(e)
            raise Http404

    def post(self, request, *args, **kwargs):
        try:
            if 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'add_message':
                    return self._add_message(request)
                if action == 'get_message':
                    return self._get_message(request)
                if action == 'update_message':
                    return self._update_message(request)
                if action == 'delete_message':
                    return self._delete_message(request)
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

    def _add_message(self, request):
        try:
            message = {
                'msg_group': request.POST.get('msg_group'),
                'msg_title': request.POST.get('msg_title'),
                'msg_note': request.POST.get('msg_note'),
                'msg_start': request.POST.get('msg_start'),
                'msg_end': request.POST.get('msg_end'),
                'msg_created': datetime.datetime.now()
            }
            MessageManage.objects.create(**message)
            result = {
                'status': 0,
                'msg': '添加成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _get_message(self, request):
        try:
            id = request.POST.get('id')
            message = MessageManage.objects.filter(id=id)[0]
            message_result = {
                'msg_group': message.msg_group,
                'msg_title': message.msg_title,
                'msg_note': message.msg_note,
                'msg_start': message.msg_start,
                'msg_end': message.msg_end,
                'msg_created': message.msg_created
            }
            return JsonResponse(message_result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _update_message(self, request):
        try:
            id = request.POST.get('id')
            message = {
                'msg_group': request.POST.get('msg_group'),
                'msg_title': request.POST.get('msg_title'),
                'msg_note': request.POST.get('msg_note'),
                'msg_start': request.POST.get('msg_start'),
                'msg_end': request.POST.get('msg_end')
            }
            MessageManage.objects.filter(id=id).update(**message)
            result = {
                'status': 0,
                'msg': '修改成功'
            }
            return JsonResponse(result)
        except Exception as e:
            logger.exception(e)
            raise Http404

    def _delete_message(self, request):
        try:
            id = request.POST.get('id')
            MessageManage.objects.filter(id=id).delete()
            result = {
                'status': 0,
                'msg': '删除成功'
            }
            return JsonResponse(result)
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
