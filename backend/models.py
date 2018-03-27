from django.db import models
from django.utils.translation import gettext_lazy as _

# 消息分组
SYSTEM_MESSAGE = 1
BACKEND_MESSAGE = 2
ESHOP_MESSAGE = 3
MEMBER_MESSAGE = 4
MESSAGE_GROUP = [
    (SYSTEM_MESSAGE, '系统消息'),
    (BACKEND_MESSAGE, '后台消息'),
    (ESHOP_MESSAGE, '前台消息'),
    (MEMBER_MESSAGE, '会员消息')
]


class CustomerService(models.Model):
    """
    客服列表
    """
    cs_phone = models.CharField(_(u'客服电话'), max_length=11)
    cs_qq = models.CharField(_(u'客服QQ'), max_length=15)
    cs_weixin = models.CharField(_(u'客服微信二维码图片'), max_length=100)
    cs_note = models.TextField(_(u'备注'))


class MessageManage(models.Model):
    message_group = models.IntegerField(_(u'消息分组'), choices=MESSAGE_GROUP)
    message_note = models.TextField(_(u'消息内容'))
    message_start = models.DateTimeField(_(u'消息开始时间'), blank=True, null=True)
    message_end = models.TextField(_(u'消息结束时间'), blank=True, null=True)
