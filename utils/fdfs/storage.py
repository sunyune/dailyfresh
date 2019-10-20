#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    '''fast_dfs我那件存储类'''
    def __init__(self, client_conf=None, base_url=None):
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        '''打开文件时使用'''
        pass

    def _save(self, name, content):
        ''''''
        # 上传文件的名字
        # content：包含上传文件内容的file对象
        # 创建以恶搞fdfs_client对象
        client = Fdfs_client(self.client_conf)

        # 上传文件到fast_dfs系统中
        res = client.upload_appender_by_buffer(content.read())

        if res.get('Status') != 'Upload successed.':
            # 上传失败异常捕获
            raise Exception('上传我呢见到fast_dfs失败')

        # 获取上传文件的id
        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        '''django判断文件名是否可用'''
        return False

    def url(self, name):
        '''返回访问文件的url'''
        return self.base_url+name
