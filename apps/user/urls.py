#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
# from user import views
from user.views import RegisterView, ActiveView, LoginView, LogoutView, UserInfoView, UserOrderView, AddressView

urlpatterns = [
    # url(r'^register$', views.register, name='register'),  # 注册
    # url(r'^register_handle$', views.register_handle, name='register_handle'),  # 注册处理

    url(r'^register$', RegisterView.as_view(), name='register'),  # 注册
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 激活

    url(r'^login$', LoginView.as_view(), name='login'),  # 激活
    url(r'^logout$', LogoutView.as_view(), name='logout'),  # 退出登录

    # url(r'^$', login_required(UserInfoView.as_view()), name='user'),  # 用户中心-信息页
    # url(r'^order$', login_required(UserOrderView.as_view()), name='order'),  # 用户中心-订单页
    # url(r'^address$', login_required(AddressView.as_view()), name='address'),  # 用户中心-地址页

    url(r'^$', UserInfoView.as_view(), name='user'),  # 用户中心-信息页
    url(r'^order$', UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    url(r'^address$', AddressView.as_view(), name='address'),  # 用户中心-地址页

]
