"""metalamp_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from educational_service.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', main_page, name='home'),
    # path('tests/', tests, name='tests'),
    path('themes-with-tests/', Tests.as_view(), name='tests'),
    path('theme-info/<slug:slug>', theme_description, name='theme_desc'),
    path('tests/<int:pk>', theme_questions, name='test'),
    # path('tests/<int:pk>', ThemeQuestions.as_view(), name='test'),

    # path('api/v1', main_page, name='api'),
    path('registration', UserRegistration.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('logout', user_logout, name='logout'),
    # path('hello/2', MainPage.as_view(), name='main_page2')

    path('api/v1/', include('rest_api.urls'))
]
