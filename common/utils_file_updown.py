# coding:UTF-8
import base64

from django.http import HttpResponse
from django.conf import settings

import datetime
import os
import uuid
import urllib


class FileOperateUtil:
    """文件操作工具类，文件上传，下载"""
    def __init__(self):
        pass

    @staticmethod
    def upload_file(file_name, file_obj):
        """
        @:description 保存单个文件到服务器
        @:param  file_name 仓库名
        @:param  file_obj 待上传文件对象
        @return file_relative_path:文件服务存放地址,filename:上传后存放的文件名
        """
        # 拆离出文件名和文件格式后缀
        original_name, file_extension = os.path.splitext(file_obj.name)
        # 拼接新的文件名
        filename = "%s%s" % (str(uuid.uuid1()), file_extension)
        # 拼接文件上传目录
        time = datetime.datetime.now()
        # path = 根目录/年/月/日
        path = "%s/%s/%s/%s/%s/" % (settings.MEDIA_ROOT, file_name, time.year, time.month, time.day)
        # 如果目录不存在，创建此目录
        if not os.path.exists(path):
            os.makedirs(path)
        # 拼接文件上传存放文件路径
        real_path = "%s%s" % (path, filename)
        if not os.path.isfile:
            raise Exception("上传失败，不是一个文件!")
        # 上传文件操作
        destination = open(real_path, 'wb+')
        for chunk in file_obj.chunks():
            destination.write(chunk)
        destination.close()
        file_relative_path = "%s/%s/%s/%s/%s" % (file_name, time.year, time.month, time.day, filename)
        return file_relative_path,filename

    @staticmethod
    def save_base64_file(file_name, base64_obj, file_extension=".jpg"):
        """
        @:description 保存单个文件到服务器
        @:param  file_name 文件上传存放文件路径名，最终路径：media/传入路径/年/月/日
        @:param  base64_obj 待上传base64流对象
        @:param file_extension 文件类型
        """
        # 将base64转成文件流对象
        #imgdata = base64_obj.split(',')[1].decode('base64')
        imgdata = base64.b64decode(base64_obj.split(',')[1])
        # 拼接新的文件名
        filename = "%s%s" % (str(uuid.uuid1()), file_extension)
        # 拼接文件上传目录
        time = datetime.datetime.now()
        # path = 根目录/年/月/日
        path = "%s/%s/%s/%s/%s/" % (settings.MEDIA_ROOT, file_name, time.year, time.month, time.day)
        # 如果目录不存在，创建此目录
        if not os.path.exists(path):
            os.makedirs(path)
        # 拼接文件上传存放文件路径
        real_path = "%s%s" % (path, filename)
        if not os.path.isfile:
            raise Exception("上传失败，不是一个文件!")
        # 上传文件操作
        destination = open(real_path, 'wb+')
        # 写入文件
        destination.write(imgdata)
        # 关闭文件流
        destination.close()
        file_relative_path = "%s/%s/%s/%s/%s" % (file_name, time.year, time.month, time.day, filename)
        return file_relative_path

    @staticmethod
    def save_http_file(file_name, url, file_extension=".jpg"):
        """
        @:description 保存单个文件到服务器
        @:param  file_name 文件上传存放文件路径名，最终路径：media/传入路径/年/月/日
        @:param  url http链接
        @:param file_extension 文件类型
        """
        # 拼接新的文件名
        filename = "%s%s" % (str(uuid.uuid1()), file_extension)
        # 拼接文件上传目录
        time = datetime.datetime.now()
        # path = 根目录/年/月/日
        path = "%s/%s/%s/%s/%s/" % (settings.MEDIA_ROOT, file_name, time.year, time.month, time.day)
        # 如果目录不存在，创建此目录
        if not os.path.exists(path):
            os.makedirs(path)
        # 拼接文件上传存放文件路径
        real_path = "%s%s" % (path, filename)
        urllib.request.urlretrieve(url, real_path)
        file_relative_path = "%s/%s/%s/%s/%s" % (file_name, time.year, time.month, time.day, filename)
        return file_relative_path