#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),  # 使用富文本编辑框配置
    url(r'^search', include('haystack.urls')),  # 全文检索框架
    url(r'^user/', include(('user.urls', 'user'), namespace='user')),  # 用户模块
    url(r'^cart/', include(('cart.urls',  'cart'), namespace='cart')),  # 购物车模块
    url(r'^order/', include(('order.urls', 'order'), namespace='order')),  # 订单模块
    url(r'^/', include(('goods.urls', 'goods'), namespace='goods')),  # 商品模块

    # url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT})
]

