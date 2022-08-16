#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: tjupt_bot.py
# 说明:
# 时间: 2022/08/15 19:29:12
# 作者: Azure
# 版本: 1.0

import pickle
from os.path import isfile
from typing import Union

import requests
import retry
from prettytable import PrettyTable
from requests.cookies import RequestsCookieJar

from tools import debug, error

from .config_file import ConfigFile


class Bot(object):
    def __init__(self, base_url: str, douban_path: str, cookie_path: str, config: ConfigFile) -> None:
        '''
        一天创建一个新的.
        '''
        self.base_url = base_url
        self.douban_path = douban_path
        self.cookie_path = cookie_path
        self.config = config

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
        })

        self.table = PrettyTable(['目标', '时间', '签到', 'TOP10'])

    def __load_cookies(self) -> RequestsCookieJar:
        '''
        读取本地的cookies.
        '''
        cookies = None
        if isfile(self.cookie_path):
            try:
                with open(self.cookie_path, 'rb') as fr:
                    cookies = pickle.load(fr)
            except Exception as e:
                error(f'打开Cookies文件{self.cookie_path}失败, 原因: {e}')
        else:
            debug(f'Cookies文件{self.cookie_path}不存在')

        if cookies:
            return cookies
        else:
            return RequestsCookieJar()
