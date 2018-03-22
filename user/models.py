# coding=UTF-8
"""
根据项目的业务逻辑重写(override)了django的auth模块
"""
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionManager, UserManager, GroupManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from decimal import Decimal
from common.district.models import District


class Permission(models.Model):
    """
    权限表
    """
    name = models.CharField(_(u'权限名'), max_length=255)
    content_type = models.ForeignKey(ContentType, models.CASCADE, verbose_name=_(u'归属模型'), related_name='perms')
    codename = models.CharField(_(u'权限码'), max_length=100)
    objects = PermissionManager()

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        unique_together = (('content_type', 'codename'),)
        ordering = ('content_type__app_label', 'content_type__model', 'codename')

    def __str__(self):
        return u"%s | %s | %s<%s>" % (self.content_type.app_label, self.content_type, self.codename, self.name,)

    def natural_key(self):
        return (self.codename,) + self.content_type.natural_key()

    natural_key.dependencies = ['contenttypes.contenttype']


class Group(models.Model):
    """
    用户群，群里的用户拥有该群绑定的权限
    """
    name = models.CharField(_(u'群名称'), max_length=80, unique=True)
    permissions = models.ManyToManyField(Permission, verbose_name=_(u'群权限'), blank=True, )
    is_active = models.BooleanField(_(u'是否激活'), default=True, help_text=_(u'用户群激活后权限才会生效'), )
    created = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    notes = models.TextField(_(u'备注'), default=True)

    objects = GroupManager()

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class PermissionsMixin(models.Model):
    """
    权限混合类，用于实现用户与用户群、用户与权限的关联及接口
    """
    is_superuser = models.BooleanField(_(u'超级用户'), default=False, help_text=_(u'超级用户拥有系统里的所有权限'), )
    groups = models.ManyToManyField(Group, verbose_name=_(u'用户群'), blank=True, help_text=_(u'用户群里的用户可以拥有此群上绑定的权限'),
                                    related_name="user_set", related_query_name="user", )
    permissions = models.ManyToManyField(Permission, verbose_name=_(u'用户权限'), blank=True, help_text=_(u'用户上绑定的权限'),
                                         related_name="user_set", related_query_name="user", )

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        返回用户群上绑定的权限集
        可选参数obj传值后仅返回obj上的权限集，但当前未实现此逻辑，故返回空集
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_all_permissions"):
                permissions.update(backend.get_all_permissions(self, obj))
        return permissions

    def has_perm(self, perm, obj=None):
        """
        判断用户是否拥有指定权限，perm的格式为app_label.codename，比如：goods.add_goods
        可选参数obj传值后仅返回obj是否拥有此权限，但当前未实现此逻辑，故返回False
        """
        # 激活后的超级用户拥有所有权限
        if self.is_active and self.is_superuser:
            return True

        # 其他人需要从权限后台(backends)中核查
        for backend in auth.get_backends():
            if not hasattr(backend, 'has_perm'):
                continue
            try:
                if backend.has_perm(self, perm, obj):
                    return True
            except PermissionDenied:
                return False
        return False

    def has_perms(self, perm_list, obj=None):
        """
        判断用户是否拥有指定的所有权限
        可选参数obj传值后仅返回obj是否拥有指定的所有权限，但当前未实现此逻辑，故返回False
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        如果用户拥有指定app_label下的任意一个权限，返回True
        """
        # 激活后的超级用户拥有所有权限
        if self.is_active and self.is_superuser:
            return True

        for backend in auth.get_backends():
            if not hasattr(backend, 'has_module_perms'):
                continue
            try:
                if backend.has_module_perms(self, app_label):
                    return True
            except PermissionDenied:
                return False
        return False


class User(AbstractBaseUser, PermissionsMixin):
    """
    系统用户表
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_(u'用户名'), max_length=150, unique=True, help_text=_(u'必填, 由字母、数字和下划线组成，最长150个字符'),
                                validators=[username_validator], error_messages={'unique': _(u"用户名已存在"), }, )
    nick = models.CharField(_(u'昵称'), max_length=150, blank=True)
    phone = models.CharField(_(u'电话'), max_length=20)
    email = models.EmailField(_(u'邮箱'), blank=True)
    verify_code = models.CharField(_(u'验证码'), max_length=4)  # 4位验证码
    is_staff = models.BooleanField(_(u'内部职员'), default=False, help_text=_(u'只有内部职员可以登录系统管理后台'), )
    is_active = models.BooleanField(_(u'是否激活'), default=True, help_text=_(u'用户激活后方可登录'), )
    date_joined = models.DateTimeField(_(u'注册时间'), auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.nick

    def get_short_name(self):
        return self.nick

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        给此用户发送邮件
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Department(models.Model):
    """
    部门表
    """
    name = models.CharField(_(u'部门名称'), max_length=50, unique=True)
    is_active = models.BooleanField(_(u'是否激活'), default=True, help_text=_(u'失效后不会成为部门的可选项'), )
    created = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    notes = models.TextField(_(u'备注'), default=True)


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(_(u'角色名称'), max_length=50, unique=True)
    groups = models.ManyToManyField(Group, verbose_name=_(u'用户群'), blank=True, help_text=_(u'角色拥有其所在用户群上绑定的所有权限'),
                                    related_name="role_set", related_query_name="role", )
    is_active = models.BooleanField(_(u'是否激活'), default=True, help_text=_(u'失效后不会成为角色的可选项'), )
    created = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    notes = models.TextField(_(u'备注'), default=True)


class Staff(models.Model):
    """
    职员表
    """
    user = models.OneToOneField(User, models.CASCADE, verbose_name=u'登录用户')
    department = models.OneToOneField(Department, models.SET_NULL, null=True, verbose_name=u'部门')
    role = models.OneToOneField(Role, models.SET_NULL, null=True, verbose_name=u'角色')
    superior = models.ForeignKey('self', models.SET_NULL, null=True, verbose_name=u'直属上级')


class CustomerLevel(models.Model):
    """
    客户等级
    """
    name = models.CharField(_(u'名称'), max_length=50, unique=True)
    discount_rate = models.DecimalField(_(u'折扣率'), max_digits=10, decimal_places=4, default=Decimal(0))
    credit_limit = models.DecimalField(_(u'信用额度'), max_digits=20, decimal_places=2, default=Decimal(0))
    is_default = models.BooleanField(_(u'是否默认'), default=False, help_text=_(u'设为默认后新客户注册时会自动选中此等级'), )
    notes = models.TextField(_(u'备注'), default=True)


class Customer(models.Model):
    """
    客户表
    """
    user = models.OneToOneField(User, models.CASCADE, verbose_name=u'登录用户')
    companyname = models.CharField(_(u'公司名称'), max_length=100, unique=True)
    level = models.ForeignKey(CustomerLevel, models.SET_NULL, null=True, verbose_name=u'客户等级')
    legalman = models.CharField(_(u'法人'), max_length=50, blank=True)
    linkman = models.CharField(_(u'联系人'), max_length=50)
    phone = models.CharField(_(u'联系人电话'), max_length=20)
    district = models.ForeignKey(District, models.SET_NULL, blank=True, null=True, verbose_name=u'所在地区')
    address = models.CharField(_(u'公司地址'), max_length=255, blank=True)
    points = models.DecimalField(_(u'线上余额/积分'), max_digits=20, decimal_places=2, default=Decimal(0))
    credit_limit = models.DecimalField(_(u'信用额度'), max_digits=20, decimal_places=2, default=Decimal(0))
    notes = models.TextField(_(u'备注'), default=True)


class Overdraft(models.Model):
    """
    客户透支总额表
    """
    customer = models.OneToOneField(Customer, models.CASCADE, verbose_name=u'客户')
    overdraft = models.DecimalField(_(u'透支总额'), max_digits=20, decimal_places=2, default=Decimal(0))
    updated = models.DateTimeField(_(u'更新时间'), auto_now_add=True)


class ShippingAddress(models.Model):
    """
    收货地址
    """
    customer = models.ForeignKey(Customer, models.CASCADE, verbose_name=u'客户')
    district = models.ForeignKey(District, models.PROTECT, verbose_name=u'所在地区')
    address = models.CharField(_(u'公司地址'), max_length=255)
    receiver = models.CharField(_(u'收件人'), max_length=50)
    phone = models.CharField(_(u'收件人电话'), max_length=20)
    is_default = models.BooleanField(_(u'是否默认'), default=False)

