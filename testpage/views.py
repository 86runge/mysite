# coding=utf-8
import logging
from django.shortcuts import render
from django.views import View

logger = logging.getLogger('site.%s' % __name__)


class TestDistrict(View):

    def get(self, request):
        return render(request, 'testpage/district.html')
