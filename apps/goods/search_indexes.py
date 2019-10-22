#!/usr/bin/env python
# -*- coding: utf-8 -*-
from haystack import indexes
from goods.models import GoodsSKU


# 指定对于某个类的某些数据建立索引
# 索引类名格式：模型类+Index
class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引字段，use_template=True指定根据表中哪些字段建立索引文件，放在一个文件中
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 返回你的模型类
        return GoodsSKU

    # 建立索引数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
