# coding=UTF-8
from common.utils.utils_file import FileUploadUtil, FileOperateUtil
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
# Create your views here.


class FileOPView(View):

    def get(self, request):
        """

        :param request:
        :return:
        """
        return render(request, "demo/file/file_index.html", {})

    def post(self, request):
        """
        :param request:
        :return:
        """
        if request.method == "POST":
            op = request.POST.get('op')
            if op == "upload":
                return FileOPView.upload(request)
            elif op == "upload_64":
                return FileOPView.upload_64(request)
            elif op == "upload_unzip":
                return FileOPView.upload_unzip(request)
            else:
                return JsonResponse("未知错误")
        return JsonResponse("未知错误")

    @staticmethod
    def upload(request):
        """
        文件上传
        :param request:
        :return:
        """
        file_obj = request.FILES.get("up_file")
        file_upload = FileUploadUtil(file_obj, "upload/", 100*1024*1024)
        flag = file_upload.upload_file(is_new_folder=True)
        if flag:
            ret = {'status': 200, 'msg': '上传成功', 'file_info': file_upload.file_path}
        else:
            ret = {'status': 500, 'msg': '上传失败', 'file_info': file_upload.file_path}
        return JsonResponse(ret)

    @staticmethod
    def upload_64(request):
        """
        文件上传
        :param request:
        :return:
        """
        img_data = request.POST.get("img_data")
        ret = FileUploadUtil.upload_base64_file(img_data, 'upload/img/', '.jpg')
        return JsonResponse(ret)

    @staticmethod
    def upload_unzip(request):
        """
        文件上传并解压缩
        :param request:
        :return:
        """
        # 先上传文件
        file_obj = request.FILES.get("up_file")
        file_upload = FileUploadUtil(file_obj, "upload/", 100 * 1024 * 1024)
        flag = file_upload.upload_file(is_new_folder=True)
        ret = {'status': 500, 'msg': '文件上传失败'}
        if flag:
            try:
                if file_upload.file_extension != '.zip':
                    raise Exception("该文件不是zip文件，无法解压")
                unzip_folder = request.POST.get('unzip_folder')
                unzip_path = "%s/%s%s/" % (settings.MEDIA_ROOT, unzip_folder, file_upload.file_name)
                # 解压缩
                FileOperateUtil.unzip_file(file_upload.absolute_path, unzip_path)
                print("------------ 成功 ------------------")
                ret = {'status': 500, 'msg': '文件上传成功，并已解压'}
            except Exception as e:
                print("------------ 解压缩文件发生异常 ---%s" % e)
                ret = {'status': 500, 'msg': str(e)}
        return JsonResponse(ret)


class FileDownLoad(View):
    """
    文件下载
    """

    def get(self, request):
        """
        文件下载
        :param request:
        :return:
        """
        file_path = request.GET.get("file_path")
        return FileUploadUtil.download_file(file_path)
