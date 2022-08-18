#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: tjupt_bot.py
# 说明:
# 时间: 2022/08/15 19:29:12
# 作者: Azure
# 版本: 1.0

import pickle
from os import makedirs
from os.path import isdir, isfile
from typing import Union

import requests
from prettytable import PrettyTable
from requests.cookies import RequestsCookieJar
from retry import retry

from tools import debug, error, info

from .config_file import UserConfig

CACHE_FOLDER = './cache'

if not isdir(CACHE_FOLDER):
    makedirs(CACHE_FOLDER)

DOUBAN_PATH = f'{CACHE_FOLDER}/douban.json'
COOKIE_PATH = f'{CACHE_FOLDER}/cookie.pkl'
BASE_URL = 'https://www.tjupt.org/'

file_userconfig = UserConfig()


class BotError(Exception):
    ...


class LoginError(BotError):
    ...


class CookiesError(BotError):
    ...


class Bot(object):
    def __init__(
        self,
        config: UserConfig = file_userconfig,
        douban_path: str = DOUBAN_PATH,
        base_url: str = BASE_URL,
        cookie_path: str = COOKIE_PATH
    ) -> None:
        '''
        一天创建一个新的.
        '''
        self.base_url = base_url
        self.douban_path = douban_path
        self.cookie_path = cookie_path
        self.config = config

        self.cookies: Union[RequestsCookieJar, None] = None
        self.data: Union[dict, None] = None

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
        })

        self.table = PrettyTable(['目标', '时间', '签到', 'TOP10'])

    def load_cookies(self) -> RequestsCookieJar:
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

    @retry(tries=5, exceptions=(LoginError, CookiesError))
    def login_and_get_cookies(self):
        '''登陆'''
        userid = self.config.user.id
        userpwd = self.config.user.pwd

        try:
            self.session.get(f'{self.base_url}login.php')
            res = self.session.post(f'{self.base_url}takelogin.php', {
                'username': userid,
                'password': userpwd
            })
        except Exception as e:
            raise LoginError(f'登陆失败(网页访问失败), 错误: {e}')

        if 'logout.php' in res.text:
            info(f'登陆成功：{userid}')
            try:
                with open(self.cookie_path, 'wb') as fr:
                    pickle.dump(self.session.cookies, fr)
                info(f'保存cookies成功: {self.cookie_path}')
            except Exception as e:
                self.session.cookies.clear()
                raise CookiesError(f'保存cookies失败: {self.cookie_path}, 错误: {e}')
        else:
            self.session.cookies.clear()
            raise LoginError(f'{userid}登陆失败')

    @retry(tries=2, exceptions=(LoginError, CookiesError))
    def login_try_cookie(self):
        '''通过cookie登陆'''
        self.session.cookies = self.load_cookies()
        try:
            res = self.session.get(self.base_url)
        except:
            raise LoginError('访问主页失败')
        if 'logout.php' in res.text:
            info(f'通过cookies登陆成功: {self.config.user.id}')
        else:
            self.login_and_get_cookies()
            raise LoginError('登陆失败')

