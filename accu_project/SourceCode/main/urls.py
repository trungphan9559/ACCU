"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from main import views

urlpatterns = [
    path('admin/login/', views.redirect_login),
    path('admin/', admin.site.urls),
    path('customers/', include('f_1_1_customers.urls')), 
    path('sites/', include('f_1_2_sites.urls')), 
    path('accounts/', include('f_7_1_accounts.urls')), 
    path('accounts/', include('django.contrib.auth.urls')), 
    path('', include('accu_dashboard.urls')),


]
