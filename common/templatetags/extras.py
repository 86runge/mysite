# coding=UTF-8
import os
import time
from django.conf import settings
from django.template import Library

register = Library()


@register.filter
def static_url(value):
    """在 js/css/img 后面添加最后修改时间的时间戳"""
    ts = time.time()
    if not settings.DEBUG:
        static_path = os.path.join(settings.STATIC_ROOT, value.replace("/", os.sep))
        if os.path.isfile(static_path):
            ts = os.stat(static_path).st_mtime
    sp = "?" if "?" not in value else "&"
    return settings.STATIC_URL + value + sp + 'v=%.1f' % ts


@register.filter
def media_url(value):
    """在 js/css/img 后面添加最后修改时间的时间戳"""
    ts = time.time()
    if not settings.DEBUG:
        media_path = os.path.join(settings.MEDIA_ROOT, value.replace("/", os.sep))
        if os.path.isfile(media_path):
            ts = os.stat(media_path).st_mtime
    sp = "?" if "?" not in value else "&"
    return settings.MEDIA_URL + value + sp + 'v=%.1f' % ts


@register.filter
def get_dict(value, args):
    """获取dict的值"""
    return value[args]
