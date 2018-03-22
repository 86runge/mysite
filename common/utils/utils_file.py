# coding=UTF-8
import base64
import os

import time
import datetime
import shutil
import zipfile
import logging

from django.conf import settings
from django.http import HttpResponse


# ===========================================================================================================
# 文件上传工具类
# ===========================================================================================================

logger = logging.getLogger(__name__)


class FileUploadUtil(object):
    """
    文件上传下载工具类
    """
    file_obj = None             # 待上传文件对象
    file_name = None            # 传入的文件名【不带扩展名】
    file_extension = None       # 传入的文件类型【文件扩展名】

    new_file_name = None        # 新的文件名，存入时文件名【新文件名，带扩展名】
    real_path = None            # 文件实际全路径【目录】
    file_path = None            # 文件存放路径【相对路径】
    absolute_path = None        # 文件绝对路径【C:/tmp/test.zip】
    max_size = None             # 文件上传大小限制

    def __init__(self, src_file_obj, dst_file_path=settings.UPLOAD_DEFAULT_FOLDER, max_size=settings.UPLOAD_DEFAULT_SIZE):
        """
        初始化文件上传对象
        :param src_file_obj: 待上传文件流
        :param dst_file_path: 待上传文件存放路径(默认上传到media/tmp目录)
        :param max_size: 默认文件上传大小
        """
        self.file_obj = src_file_obj
        self.set_file_info(src_file_obj.name)
        self.set_new_name()
        self.set_real_path(dst_file_path)
        self.max_size = max_size
        self.file_path = "%s%s" % (dst_file_path, self.new_file_name)
        self.absolute_path = "%s%s" % (self.real_path, self.new_file_name)

    def set_file_info(self, src_file_name):
        """
        从传入的文件名中拆分文件名称和文件格式
        :param src_file_name: 待操作的文件全路径名称
        :return:
        """
        file_tmp_name, file_extension = FileOperateUtil.extract_file_name(src_file_name)
        self.file_name = file_tmp_name
        self.file_extension = file_extension

    def set_new_name(self):
        """
        根据文件类型，加上当前时间的年月日时分秒生成新的文件名
        :return:
        """
        current_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.new_file_name = "%s%s" % (current_timestamp, self.file_extension)

    def set_real_path(self, dst_file_path):
        """
        设置文件实际文件路径（拼接上：settings.MEDIA_ROOT）
        :param dst_file_path: 文件存放文件夹路径
        :return: 文件绝对路径
        """
        self.real_path = "%s/%s" % (settings.MEDIA_ROOT, dst_file_path)

    def upload_file(self, is_new_folder=False):
        """
        上传文件:
            上传的文件数据，可直接从FileUploadUtil对象中获取
        :param is_new_folder: 若目录不存在时，是否自动新建该目录
        :return: 返回boolean 成功返回true,失败返回false
        """
        try:
            # 第一步判断文件目录是否存在,不存在会抛出异常
            FileOperateUtil.validate_folder_exists(self.real_path, is_new_folder)
            # 判断文件大小
            FileOperateUtil.validate_file_size(self.file_obj, self.max_size)
            # 上传文件到指定目录
            FileOperateUtil.copy_file_chunks(self.file_obj, self.real_path+self.new_file_name)
        except Exception as e:
            logger.debug("文件上传发生异常，%s" % e)
            return False
        return True

    @staticmethod
    def download_file(src_file_path, down_file_name=None):
        """
        下载文件，返回带有文件流的response响应
        :param src_file_path: 待下载文件路径
        :param down_file_name: 下载时指定文件名
        :return: 带有文件流的response响应
        """
        real_path = "%s/%s" % (settings.MEDIA_ROOT, src_file_path)
        # 判断该文件目录是否存在
        if os.path.exists(real_path):
            # 判断文件是否是文件
            if os.path.isfile(real_path):
                # 获取文件本身自己的名称
                filename = os.path.basename(real_path)
                # 若未指定下载文件名，则已文件本身名称为准
                if down_file_name is None:
                    down_file_name = filename
                # 读取文件流，并构造请求响应
                response = HttpResponse(FileOperateUtil.file_iterator(real_path))
                # 设置响应流
                response['Content_type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename={0}'.format(down_file_name.encode('utf-8').decode('utf-8'))
            else:
                response = HttpResponse("下载失败,不是一个文件!", content_type="text/plain;charset=utf-8")
        else:
            response = HttpResponse("文件不存在,下载失败!", content_type="text/plain;charset=utf-8")
        return response

    @staticmethod
    def upload_base64_file(base64_obj, dst_file_path=settings.UPLOAD_DEFAULT_FOLDER, file_ext=".jpg"):
        """
        上传base64文件流到服务器指定目录
        :param dst_file_path: 文件存放路径 "tmp/"
        :param base64_obj: base64流对象
        :param file_ext:   新文件扩展名：默认.jpg
        :return: 文件上传存入的文件目录
        """
        ret = {'status': False, 'msg': ''}
        try:
            # 将base64转成文件流对象
            file_str = base64_obj.split(',')[1].encode('utf-8')
            file_data = base64.b64encode(file_str)
            # 当前时间戳：年月日时分秒
            cur_time = int(round(time.time() * 1000))
            # 拼接新的文件名
            file_name = "%s%s" % (cur_time, file_ext)
            # 拼接文件存放目录
            file_path = "%s/%s" % (settings.MEDIA_ROOT, dst_file_path)
            save_path = "%s%s%s" % (dst_file_path, file_name, file_ext)
            # 判断文件目录
            FileOperateUtil.validate_folder_exists(file_path, is_create=True)
            try:
                # 拼接文件最终存放全路径
                real_path = "%s%s" % (file_path, file_name)
                # 上传文件操作
                destination = open(real_path, 'wb+')
                # 写入文件
                destination.write(file_data)
                ret = {'status': 200, 'msg': '上传成功', 'file_path': save_path}
            except Exception as e:
                logger.debug("上传base64文件，写文件发生异常，%s" % e)
                raise Exception("上传base64文件，写文件发生异常")
            finally:
                destination.close()
        except Exception as e:
            logger.debug("上传base64文件发生异常,%s" % e)
            ret = {'status': 500, 'msg': e}
        return ret

    @staticmethod
    def download_batch_file(src_file_folder, zip_folder=settings.ZIP_DEFAULT_FOLDER, down_file_name=None, is_delete=True):
        """
        将文件夹压缩打包下载
        :param src_file_folder: 要下载的文件目录
        :param zip_folder: 打包存放目录
        :param down_file_name: 下载时指定文件名
        :param is_delete: 下载完成后是否删除打包的文件，默认：删除
        :return: 带有文件流的response响应
        """
        # 判断待打包目录是否存在，不存在则抛出异常
        FileOperateUtil.validate_folder_exists(src_file_folder)
        # 判断打包存放目录是佛存在，不存在则新建
        FileOperateUtil.validate_folder_exists(zip_folder, is_create=True)
        # 设置响应头
        if os.path.exists(src_file_folder):
            cur_time = int(round(time.time() * 1000))
            zip_file_name = "%s" % cur_time
            zip_file_path = "%s/%s" % (settings.MEDIA_ROOT, zip_folder, zip_file_name)
            # 打包该目录
            FileOperateUtil.zip_dir(src_file_folder, zip_file_path)
            # 判断打包生成的文件是否是个文件
            if os.path.isfile(zip_file_path):
                filename = os.path.basename(zip_file_path)
                # 若未指定下载文件名，则已文件本身名称为准
                if down_file_name is None:
                    down_file_name = filename
                # 读取文件流，并构造请求响应
                response = HttpResponse(FileOperateUtil.file_iterator(zip_file_path))
                response['Content_type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename={0}'.format(down_file_name.encode('utf-8'))
            else:
                response = HttpResponse("下载失败,不是一个文件!", content_type="text/plain;charset=utf-8")
        else:
            response = HttpResponse("文件不存在,下载失败!", content_type="text/plain;charset=utf-8")
        return response


# ===========================================================================================================
# 文件操作工具类
# ===========================================================================================================


class FileOperateUtil(object):
    """
    文件操作类
    """

    @staticmethod
    def file_iterator(down_file):
        """根据文件路径获取待下载文件流"""
        content = open(down_file, 'rb+').read()
        return content

    @staticmethod
    def extract_file_name(src_file_name):
        """
        从完整路径名称中提取文件扩展名
        :param src_file_name:
        :return: 文件扩展名元组（文件路径，文件扩展名） eg:C:/tmp/test.ext --> ('C:/tmp/', '.txt')
        """
        ext_meta = os.path.splitext(src_file_name)
        return ext_meta

    @staticmethod
    def validate_folder_exists(folder, is_create=False):
        """
        判断文件目录是否存在，如果不存在则创建
        :param folder: 待判断目录
        :param is_create: 是否创建
        :return:
        """
        if not os.path.exists(folder):
            if is_create:
                os.makedirs(folder)
            else:
                raise Exception("该目录不存在，请先创建该目录")
        return True

    @staticmethod
    def validate_file_size(src_file_path, limit_size):
        """
        判断文件大小，不能小于指定文件大小，更不能大于最大文件限制
        :param src_file_path:源文件
        :param limit_size: 限制大小
        :return:
        """
        if isinstance(src_file_path, object):  # 文件对象
            file_size = src_file_path.size
        else:
            file_size = os.path.getsize(src_file_path)
        # 判断文件大小，是否小于最大文件限制
        if file_size >= settings.UPLOAD_MAX_SIZE:
            raise Exception("上传失败,文件过大，超过10M")
        else:
            if file_size >= limit_size:
                raise Exception("上传失败，文件过大")
        return True

    @staticmethod
    def copy_file_chunks(src_file_obj, dst_file_path):
        """
        文件复制到指定目录【因为chunks貌似只有从request拿到的文件流才有，所以此方法只用于文件上传】
        :param src_file_obj: 待复制文件流对象
        :param dst_file_path: 存放目标文件路径，带文件名的完整路径 如:c:/tmp/test.txt
        :return:
        """
        # 创建存放文件流对象
        destination = open(dst_file_path, 'wb+')
        try:
            # 循环源文件块对象
            for chunk in src_file_obj.chunks():
                # 将文件流写入
                destination.write(chunk)
        except Exception as e:
            logger.debug("复制文件失败,%s" % e)
            os.remove(dst_file_path)
            raise Exception("复制文件失败,%s" % e)
        finally:
            logger.debug("关闭文件destination")
            destination.close()
        return True

    @staticmethod
    def copy_file(src_file_path, dst_file_path):
        """
        文件复制到指定目录【任意文件】
        :param src_file_path: 待复制文件完整路径
        :param dst_file_path: 存放目标文件路径，带文件名的完整路径 如:c:/tmp/test.txt
        :return:
        """
        # 判断源文件是否是文件
        if not os.path.isfile(src_file_path):
            raise Exception("上传失败，不是一个文件!")
        # 创建存放文件流对象
        destination = open(dst_file_path, 'wb+')
        try:
            src_file = open(src_file_path, "rb+")
            # 循环源文件块对象
            for line in src_file:
                # 将文件流写入
                destination.write(line)
        except Exception as e:
            logger.debug("复制文件失败,%s" % e)
            os.remove(dst_file_path)
            raise Exception("复制文件失败,%s" % e)
        finally:
            destination.close()
        return True

    @staticmethod
    def zip_dir(tar_dir_name, zip_file_name):
        """
         函数目的: 压缩指定目录为zip文件
         使用DEMO: FileOperateUtil.zip_dir("C:/tmp/", "E:/test.zip")
        :param tar_dir_name: 待压缩的目录
        :param zip_file_name:  压缩后的zip文件路径 eg:C:/tmp/test.zip
        :return: boolean ,True-成功，False-失败
        """
        file_list = []
        ret = False
        try:
            # 判断是否为文件
            if os.path.isfile(tar_dir_name):
                file_list.append(tar_dir_name)
            else:
                # 循环目录，读取文件列表
                for root, dirs, files in os.walk(tar_dir_name):
                    for name in files:
                        file_list.append(os.path.join(root, name))
            # 创建ZIP文件操作对象
            zf = zipfile.ZipFile(zip_file_name, "w", zipfile.zlib.DEFLATED)
            try:
                for tar in file_list:
                    arc_name = tar[len(tar_dir_name):]
                    zf.write(tar, arc_name)
                ret = True
            except Exception as e:
                logger.debug("压缩文件发送异常，%s" % e)
                raise Exception("压缩文件发送异常")
            finally:
                zf.close()
        except Exception as e:
            logger.debug("---- 压缩文件发生异常，%s --" % e)
            ret = False
        return ret

    @staticmethod
    def unzip_file(zip_file_name, unzip_dir_path):
        """
        解压zip文件到指定目录
        使用DEMO：FileOperateUtil.unzip_file("C:/tmp/test.zip", "c:/tmp/zip/")
        :param zip_file_name: 为zip文件路径，
        :param unzip_dir_path:  为解压文件后的文件目录
        :return : boolean
        """
        # 判断目标文件目录是否存在，不存在就创建
        if not os.path.exists(unzip_dir_path):
            os.mkdir(unzip_dir_path)
        # 创建zip操作对象
        zf_obj = zipfile.ZipFile(zip_file_name)
        try:
            for name in zf_obj.namelist():
                name = name.replace('\\', '/')
                if name.endswith('/'):
                    p = os.path.join(unzip_dir_path, name[:-1])
                    if os.path.exists(p):
                        # 如果文件夹存在，就删除之：避免有新更新无法复制[递归删除]
                        shutil.rmtree(p)
                    os.mkdir(p)
                else:
                    ext_filename = os.path.join(unzip_dir_path, name)
                    ext_dir = os.path.dirname(ext_filename)
                    if not os.path.exists(ext_dir):
                        os.mkdir(ext_dir)
                    outfile = open(ext_filename, 'wb')
                    try:
                        outfile.write(zf_obj.read(name))
                    except Exception as e:
                        logger.debug("写文件发生异常 %s" % e)
                        raise Exception("解压文件发生异常")
                    finally:
                        outfile.close()
        except Exception as e:
            logger.debug("解压文件发生异常 %s" % e)
            raise Exception(e)
            shutil.rmtree(unzip_dir_path)
        return True


