# coding = UTF-8
from django.urls import path
from .views import IndexView, LoginView, LogoutView

app_name = 'eshop'

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]