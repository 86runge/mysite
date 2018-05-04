# coding=UTF-8
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from backend.views import IndexView, BasicSettingsView, UserManageView, StaffManageView, RoleManageView, \
    MessageManageView, GoodsListView, EnterpriseListView, OrderListView, EshopDecorationView, ExcelExportView, \
    ExcelImportView

app_name = "backend"

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('basic_settings/', BasicSettingsView.as_view(), name='basic_settings'),
    path('user_manage/', UserManageView.as_view(), name='user_manage'),
    path('staff_manage/', StaffManageView.as_view(), name='staff_manage'),
    path('role_manage/', RoleManageView.as_view(), name='role_manage'),
    path('message_manage/', MessageManageView.as_view(), name='message_manage'),
    path('goods_list/', GoodsListView.as_view(), name='goods_list'),
    path('enterprise_list/', EnterpriseListView.as_view(), name='enterprise_list'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('eshop_decoration/', EshopDecorationView.as_view(), name='eshop_decoration'),

    # 文件导入导出
    path('excel_export/', ExcelExportView.as_view(), name="excel_export"),
    path('excel_import/', ExcelImportView.as_view(), name="excel_import"),
]
