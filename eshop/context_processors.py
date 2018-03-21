# coding=UTF-8


def page_mark(request):
    return {'PAGE_MARK': request.path_info.count('/') >= 3 and request.path_info.split('/') or ''}
