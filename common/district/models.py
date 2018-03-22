# coding=UTF-8
from django.db import models
from django.utils.translation import gettext_lazy as _


class District(models.Model):
    """
    行政区划
    数据源参考:
    http://passer-by.com/data_location/list.json
    https://github.com/mumuy/widget
    """
    code = models.IntegerField(_(u'行政编码'), primary_key=True)
    name = models.CharField(_(u'中文名'), max_length=50)
    is_active = models.BooleanField(_(u'是否启用'), default=True)
    notes = models.TextField(_(u'备注'), default=True)

    def __str__(self):
        return self.name
