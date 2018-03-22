import datetime

from django.db import models


class User(models.Model):
    """
    备用用户表
    """
    username = models.CharField(u'用户名', max_length=20, unique=True, help_text=u'用户名只能是数字、字母、下划线组成且只能以字母开头')
    password = models.CharField(u'密码', max_length=100, unique=True, help_text=u'密码只能是数字、字母、下划线组成')
    verify_code = models.CharField(u'验证码', max_length=4)  # 4位验证码
    verify_time = models.DateTimeField(u'验证码发送时间', blank=True, null=True)  # 1分钟内有效
    nick = models.CharField(u'姓名', max_length=20)
    phone = models.CharField(u'电话', max_length=20)
    email = models.CharField(u'邮箱', max_length=20, blank=True, null=True)
    company = models.CharField(u'公司名', max_length=50, blank=True, null=True)
    date_joined = models.DateTimeField(u'注册时间', default=datetime.datetime.now)
    is_active = models.BooleanField(u'是否激活', default=True, help_text=u'用户激活后方可登录')
    notes = models.TextField(u'备注', blank=True, null=True)
