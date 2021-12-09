"""books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
#from .views import RegisterView, LogoutView
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name="register"),
    #path('login', LoginView.as_view())
    path('token', jwt_views.TokenObtainPairView.as_view(), name="login"),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name="refresh-token"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('user-list', views.userList, name="user-list"),
	path('user-detail/<str:pk>',views.userDetail, name="user-detail"),
    path('userInfo', views.UserInfoView.as_view(), name="uesrInfo"),
    path('update-userInfo', views.UserUpdateInfoView.as_view(), name="update-uesrInfo"),
    path('change_password', views.ChangePasswordView.as_view(), name="change_password"),
   # path('update-image', views.UpdateImageView.as_view(), name="update-image"),
    path('public-profile', views.PublicProfile.as_view(), name="public-profile"),
]

