#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.core.cache import cache
from django.core.paginator import Paginator
from django_redis import get_redis_connection
from goods.models import GoodsType, GoodsSKU, IndexTypeGoodsBanner, IndexPromotionBanner, IndexGoodsBanner
from order.models import OrderGoods
# Create your views here.


# http://127.0.0.1:8000
class IndexView(View):
    '''首页'''
    def get(self, request):
        '''首页显示'''
        # 尝试从缓存中换取数据
        context = cache.get('index_page_data')

        if context is None:
            # 如果缓存中没有数据
            # 获取商品的种类信息
            types = GoodsType.objects.all()

            # 获取首页轮播商品信息
            goods_banners = IndexGoodsBanner.objects.all().order_by('index')

            # 获取首页促销活动信息
            promotion_banners = IndexTypeGoodsBanner.objects.all().order_by('index')

            # 获取首页分类商品展示信息
            for type in types:  # Goodstype
                # 获取type种类首页分类商品的图片展示信息
                image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
                # 获取type种类首页分类商品的文字展示信息
                title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

                # 动态给type增加属性，分别保管首页分类商品的图片展示信息和文字展示信息
                type.image_banners = image_banners
                type.title_banners = title_banners
            # 设置缓存
            # key value timeout
            context = {'type': types,
                       'goods_banners': goods_banners,
                       'promotion_banners': promotion_banners}
            cache.set('index_page_data', context, 3600)

        # 获取用户购物车中商品数目
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        # 组织模板上下文
        context.update(cart_count=cart_count)
        # 使用模板
        return render(request, 'index.html', context)


# /goods/商品id
class DetailView(View):
    '''详情页'''
    def get(self, request, goods_id):
        '''显示详情页'''
        try:
            sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return redirect(reverse('goods: index'))
        # 获取商品的分类信息
        types = GoodsType.objects.all()

        # 获取商品的评论信息
        sku_order = OrderGoods.objects.filter(sku=sku).exclude(comment='')

        # 新品信息
        new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

        # 获取用户购物车中商品数目
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

            # 添加用户历史浏览记录
            conn = get_redis_connection()
            history_key = 'history_%d' % user.id
            conn.lrem(history_key, 0, goods_id)
            # 把历史记录添加到列表的左侧
            conn.lpush(history_key, goods_id)
            # 只保存最近五条记录
            conn.ltrim(history_key, 0, 4)

        # 组织模板上下文
        context = {'sku': sku,
                   'type': type,
                   'ske_order': sku_order,
                   'new_skus': new_skus,
                   'cart_count': cart_count}
        # 使用模板
        return render(request, 'detail.html', context)


# 种类id,页码，排序方式
# restful api -> 请求一种资源
# list?type_id=种类id&page=页码&sort=排序方式
# /list/种类/页码/排序方式
# /list/种类/页码?sort=排序方式
class ListView(View):
    '''列表页'''
    def get(self, request, type_id, page):
        '''显示列表页'''
        # 获取种类信息
        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            # 种类不存在
            return redirect(reverse('goods:index'))
        # 获取商品分类信息
        types = GoodsType.objects.all()
        # 获取排序方式,
        # sort = default 按照默认id排序
        # sort = price 按照商品价格排序
        # sort = hot 按照商品销量排序
        sort = request.GET.get('sort')
        if sort == 'price':
            skus = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == 'hot':
            skus = GoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            sort = 'default'
            skus = GoodsSKU.objects.filter(type=type).order_by('-id')

        # 对数据进行分页
        paginator = Paginator(skus, 1)
        try:
            page = int(page)
            # 获取第page页的内容
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        skus_page = paginator.page(page)

        # 进行页码控制,页面上最多显示5个页码
        # 1.总页数小于5页,页面显示索引页码
        # 2.如果当前页时前三页,显示1-5页
        # 3.如果当前页时后三页,显示后5页
        # 4.其他情况，显示当前页的前两页，当前页，当前页的后两页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages+1)
        elif num_pages <= 3:
            page = range(1, 6)
        elif num_pages - page <=2:
            page = range(num_pages-4, num_pages+1)
        else:
            page = range(page-2, page+3)





        # 新品信息
        new_skus = GoodsSKU.objects.filter(type=type).order_by('-create_time')[:2]

        # 获取用户购物车中商品数目
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)
        # 组织模板上下文
        context = {'type': type,
                   'types': types,
                   'skus_page': skus_page,
                   'new_skus': new_skus,
                   'cart_count': cart_count,
                   'sort': sort
                   }
        # 使用模板
        return render(request, 'list.html', context)
