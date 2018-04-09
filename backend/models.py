from django.db import models
from django.utils.translation import gettext_lazy as _

# 服务时间段
MORNING = 1
AFTERNOON = 2
DAY = 3
NIGHT = 4
ALL = 5
SERVICE_TIME = [
    (MORNING, '早上'),
    (AFTERNOON, '下午'),
    (DAY, '白天'),
    (NIGHT, '晚上'),
    (ALL, '全天')
]

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
    service_time = models.IntegerField(_(u'服务时间段'), choices=SERVICE_TIME)
    cs_join_time = models.DateTimeField(_(u'客服创建时间'), auto_now_add=True)
    is_active = models.BooleanField(_(u'是否开启'), default=False)
    cs_note = models.TextField(_(u'备注'))


class MessageManage(models.Model):
    msg_group = models.IntegerField(_(u'消息分组'), choices=MESSAGE_GROUP)
    msg_title = models.CharField(_(u'消息标题'), max_length=100)
    msg_note = models.TextField(_(u'消息内容'))
    msg_created = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    msg_start = models.DateTimeField(_(u'消息开始时间'), blank=True, null=True)
    msg_end = models.DateTimeField(_(u'消息结束时间'), blank=True, null=True)
