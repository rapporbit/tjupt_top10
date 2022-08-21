#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: tjupt_bot.py
# 说明: 尽量TOP10!
# 时间: 2022/08/15 19:29:12
# 作者: Azure
# 版本: 1.0

import json
import pickle
import random
import re
import time
from os import makedirs
from os.path import isdir, isfile
from typing import List, Union

import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from requests.cookies import RequestsCookieJar
from requests.utils import requote_uri
from retry import retry

from tools import debug, error, info, warn

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


class DoubanError(BotError):
    ...


class DoubanIdNotFoundError(DoubanError):
    ...


class AutoOnceError(BotError):
    ...


class TooLateError(BotError):
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
        bot.
        '''
        self.base_url = base_url
        self.douban_path = douban_path
        self.cookie_path = cookie_path
        self.config = config

        self.cookies: Union[RequestsCookieJar, None] = None
        self.data: Union[dict, None] = None
        # 登陆状态
        self.login_status = False
        self.att_status = False
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
            self.login_status = True
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
        # 先检查登陆状态
        if self.login_status:
            return
        # 先读取cookies
        self.session.cookies = self.load_cookies()
        # 尝试登陆
        try:
            res = self.session.get(self.base_url)
        except:
            raise LoginError('访问主页失败，请检查网络')

        if 'logout.php' in res.text:
            self.login_status = True
            info(f'通过cookies登陆成功: {self.config.user.id}')
        else:
            self.login_and_get_cookies()
            raise LoginError('登陆失败，请检查 用户名或密码，或tjupt网站错误')

    def save_douban_data(self):
        '''保存豆瓣数据'''
        try:
            with open(self.douban_path, 'w', encoding='utf-8') as fr:
                if self.data is not None:
                    json.dump(self.data, fr, ensure_ascii=False, indent=1)
                    debug(f'豆瓣数据保存到: {self.douban_path}')
        except Exception as e:
            raise DoubanError(f'保存豆瓣数据出错: {self.douban_path}, 原因: {e}')

    def load_douban_data(self):
        '''加载豆瓣数据'''
        try:
            if not isfile(self.douban_path):
                raise DoubanError('文件不存在')
            with open(self.douban_path, 'r', encoding='utf-8') as fr:
                self.data: dict = json.load(fr)
                if not isinstance(self.data, dict):
                    raise DoubanError('格式不匹配')
        except Exception as e:
            debug(f'豆瓣数据{self.douban_path} 读取失败, 原因: {e}')

    def get_id(self, title: str) -> str:
        '''获取ID'''
        if self.data is None:
            self.data = {}

        if title in self.data:
            return self.data[title]

        time.sleep(random.random() * 5)

        try:
            res = requests.get(f"https://movie.douban.com/j/subject_suggest?q={requote_uri(title)}", headers={
                "User-Agent": self.session.headers.get("User-Agent"),
                "Referer": "https://movie.douban.com/"
            })
        except Exception as e:
            raise DoubanError(f'访问豆瓣错误: {e}')

        try:
            url_id: str = re.findall(
                r'(?<=/)p\d+(?=\.)', res.json()[0]['img'])[0]
            self.data[title] = url_id
            debug(f'获取豆瓣数据: {title}, {url_id}')
            return url_id
        except Exception as e:
            raise DoubanIdNotFoundError(
                f'从网页获取豆瓣数据失败: {title}, 原因: {e}, 返回内容: {res.text}')

    def attendance_once(self, target_time: Union[float, None], p_t: float = 0.01):
        '''
        签到, 推荐提前至少7秒执行，但也别太早，防止过期
        :param target_time: 签到时间戳.
        :param  p_t: 为了平衡网络延迟设置的提前量.
        '''
        try:
            response = self.session.get(f"{self.base_url}attendance.php")
            if 'login.php' in response.text:
                # debug(f'未登陆')
                self.login_try_cookie()
                response = self.session.get(f"{self.base_url}attendance.php")

            text = response.text

            if '今日已签到' in text:
                info(f'今日已签到: {self.config.user.id}')
                self.att_status = True
                return

            tree = BeautifulSoup(text, "html.parser")
            captcha_image = tree.select_one(
                ".captcha > tr > td > img").attrs["src"]
            captcha_image_id = re.findall(
                r"(?<=/)p\d+(?=\.)", captcha_image)[0]
            captcha_options = re.findall(
                r'<input name="answer" type="radio" value="(\d+-\d+-\d+ \d+:\d+:\d+&amp;(\d+))"/>([^<>]*?)<',
                str(tree.select_one(".captcha form table")))

            available_choices = []

            for value, id, title in captcha_options:
                value = str(value)
                value = value.replace("&amp;", "&")
                try:
                    url_id = self.get_id(title)
                except:
                    continue
                if captcha_image_id == url_id:
                    available_choices.append({
                        "value": value,
                        "id": id,
                        "title": title,
                        "url_id": url_id,
                        "captcha_image": captcha_image,
                    })

                    debug(
                        f"可选: {json.dumps(available_choices[-1], ensure_ascii=False)}")

            if not len(available_choices):
                raise AutoOnceError('无可选的')
            else:
                debug(f'可选的: {available_choices}')
            self.save_douban_data()

            data = {
                "answer": available_choices[0]["value"],
                "submit": "提交"
            }

            # 在此定时！
            if target_time is not None:
                spend = target_time - time.time() - p_t

                if spend < 0:
                    raise TooLateError('太晚了！很可能不是TOP10了')
                else:
                    time.sleep(spend)

            response = self.session.post(
                f"{self.base_url}attendance.php", data)
            if "签到成功" in response.text:
                info(f'签到成功: {self.config.user.id}')
                self.att_status = True
                return
            else:
                raise AutoOnceError('未发现"签到成功"')

        except Exception as e:
            raise AutoOnceError(f'签到时错误: {e}')

    def last_att(self):
        '''
        确保签到成功.
        '''
        self.att_status = False
        self.login_status = False
        try_times = 5

        while 1:
            try_times -= 1
            if try_times <= 0:
                error(f'签到失败，尝试邮件通知!')
                self.config.email.send_email(
                    'TJUPT_Bot 通知',
                    '签到失败，请手动签到!'
                )
                return
            try:
                self.attendance_once(None)
                return
            except AutoOnceError as e1:
                warn(f'此次签到失败 {e1}，继续尝试 {try_times}')
                # continue
            except Exception as e2:
                error(f'未处理错误: {e2}')
                # continue

    def auto_att_oneday(self):
        '''
        根据调用时候的时间，来选择签到.(提前一段时间调用，1min左右)\n
        每过一天，那么记得重置一下att_status.
        '''
        if self.att_status:
            return
        _t = time.time()
        # 解析选择的时间点
        ava_times: List[float] = []

        for item in self.config.timer.points_in_time:
            item = item.strip()
            item = item.split(':', 1)

            item = time.strftime(
                f'%Y-%m-%d {item[0]}:{item[1]}:00', time.localtime())

            # debug(f'设置的时间点: {item}')
            item = time.mktime(time.strptime(item, r'%Y-%m-%d %H:%M:%S'))
            ava_times.append(item)

        ava_times.sort()

        # 找到目标时间点
        for i in range(len(ava_times)):
            if _t >= ava_times[i]:
                continue
            else:
                temp_time_s = time.strftime(
                    r'%Y-%m-%d %H:%M:%S', time.localtime(ava_times[i]))
                debug(f'找到: {temp_time_s}')
                try:
                    self.attendance_once(ava_times[i], self.config.timer.p_t)
                except Exception as e:
                    error(f'此次尝试签到失败: {e}')
                break
        else:
            warn(f'未找到对应的时间点，强制签到.')
            self.last_att()

    def tomorrow(self):
        self.last_att()
        self.att_status = False
        self.login_status = False
        # 缓存别太多
        self.load_douban_data()
        if len(self.data) >= 200:
            self.data = {}
            self.save_douban_data()
            info(f'清理豆瓣数据缓存: {self.douban_path}')
