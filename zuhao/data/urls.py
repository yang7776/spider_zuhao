"""zuhao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # 渲染路由
    path('show_zuhao/', show_zuhao, name='show_zuhao'),
    path('show_zu_good/', show_zuhao_good, name='szg'),
    path('show_zu_info/', user_detail, name='user_info'),
    # 功能路由
    path('get_zuhao/', get_zuhao_data, name='get_zuhao'),
    path('get_zuhao_infor_data/', get_zuhao_ifnor_data, name='gzi'),
    path('infor_three/',infor_three,name='infor_three'),
]
