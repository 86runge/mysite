import datetime

from django.db import models

"""
null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填。
"""


class Permission(models.Model):
    """
    权限表
    """
    name = models.CharField(u'权限名', max_length=255)


class Group(models.Model):
    """
    用户群，群里的用户用该群绑定的权限
    """
    name = models.CharField(u'群名称', max_length=80, unique=True)
    permissions = models.ManyToManyField(Permission, verbose_name=u'群权限', blank=True, )


class PermissionsMixin(models.Model):
    """
    权限混合类
    """
    is_superuser = models.BooleanField(u'超级用户', default=False, help_text=u'超级用户拥有系统里的所有权限', )
    groups = models.ManyToManyField(Group, verbose_name=u'用户群', blank=True, help_text=u'用户群里的用户可以拥有此群上绑定的权限',
                                    related_name="user_set", related_query_name="user", )
    permissions = models.ManyToManyField(Permission, verbose_name=u'用户权限', blank=True, help_text=u'用户上绑定的权限',
                                         related_name="user_set", related_query_name="user", )


class User(models.Model):
    """
    用户表
    """
    username = models.CharField(u'用户名', max_length=20, unique=True, help_text=u'用户名只能是数字、字母、下划线组成且只能以字母开头')
    password = models.CharField(u'密码', max_length=20, unique=True, help_text=u'密码只能是数字、字母、下划线组成')
    verify_code = models.CharField(u'短信验证码', max_length=6, blank=True, null=True)  # 6位验证码
    verify_time = models.DateTimeField(u'验证码发送时间', blank=True, null=True)  # 1分钟内有效
    nick = models.CharField(u'姓名', max_length=20, blank=True, null=True)
    phone = models.CharField(u'电话', max_length=20, blank=True, null=True)
    email = models.CharField(u'邮箱', max_length=20, blank=True, null=True)
    company = models.CharField(u'公司名', max_length=50, blank=True, null=True)
    date_joined = models.DateTimeField(u'注册时间', default=datetime.datetime.now)
    is_active = models.BooleanField(u'是否激活', default=True, help_text=u'用户激活后方可登录')
    notes = models.TextField(u'备注', blank=True, null=True)
