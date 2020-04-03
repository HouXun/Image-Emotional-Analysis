"""mysite URL Configuration

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
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


from login import views

urlpatterns = [
    path('admin/', admin.site.urls),                #管理界面
    path(r'index/', views.index),                   #主页
    path(r'login/', views.login),                   #登录
    path(r'register/', views.register),             #注册
    path(r'logout/', views.logout),                 #登出
    path(r'captcha/', include('captcha.urls')),     #验证码
    path(r'',views.index),                          #默认访问主页
    path(r'show/',views.showImg)                    #预测及查看结果

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
