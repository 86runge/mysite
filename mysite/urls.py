"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from eshop.views import IndexView, LoginView
from django.contrib.staticfiles import views
from mysite import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^favicon.ico$', views.serve, {'path': 'common/images/favicon.ico'}),
    re_path('^(index/|)$', IndexView.as_view(), name='index'),
    re_path('^(login/|)$', LoginView.as_view(), name='login'),
    path('common/', include('common.urls'), name='common'),
    path('eshop/', include('eshop.urls'), name='eshop'),
    path('backend/', include('backend.urls'), name='backend'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    from django.contrib.staticfiles import views

    urlpatterns += [
        re_path(r'^favicon.ico$', views.serve, {'path': 'common/images/favicon.ico'}),
    ]
