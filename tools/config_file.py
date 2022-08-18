#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: config_file.py
# 说明:
# 时间: 2022/08/15 19:29:46
# 作者: Azure
# 版本: 1.0

from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from typing import List, Union

import toml

from tools import debug, error, info, warn


class ConfigParserError(Exception):
    ...


CONFIG_PATH = './config.toml'


class User(object):
    ID = 'id'
    PWD = 'pwd'

    def __init__(self) -> None:
        self.id: Union[str, None] = None
        self.pwd: Union[str, None] = None


class Timer(object):
    POINTS_IN_TIME = 'points_in_time'
    DEAD_LINE = 'dead_line'

    def __init__(self) -> None:
        self.points_in_time: Union[List[str], None] = None
        self.dead_line: Union[str, None] = None


class Email(object):
    ENABLE = 'enable'
    SENDER = 'sender'
    USER = 'user'
    PWD = 'pwd'
    RECEIVERS = 'receivers'
    PORT = 'port'
    HOST = 'host'

    def __init__(self) -> None:
        self.enable = False
        self.sender: Union[str, None] = None
        self.user: Union[str, None] = None
        self.pwd: Union[str, None] = None
        self.receivers: Union[List[str], None] = None
        self.port: Union[str, None] = None
        self.host: Union[str, None] = None

    def send_email(self, title: str, content: str):
        '''
        发送邮件.
        :param title: 标题.
        :param content: 正文.
        '''

        if not self.enable:
            debug(f'未开启邮件服务，取消发送 {title}')
            info(f'EMAIL: {title} {content}')
            return False

        if self.sender is None or not len(self.sender):
            warn('取消发送，发件人未设定')
            return False

        if self.user is None or not len(self.user):
            warn('未设置用户')
            return False

        if not self.receivers and not len(self.receivers):
            warn('未设置收件人')
            return False

        if self.port is None or not len(self.port):
            # warn('未设置port，默认465')
            self.port = "465"

        if self.host is None or not len(self.host):
            # warn('未设置host，默认 smtp.qq.com')
            self.host = 'smtp.qq.com'

        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = Header(title, 'utf-8')
        message['From'] = Header(self.sender, 'utf-8')
        message['To'] = Header('TJUPT_Bot_Receiver', 'utf-8')

        try:
            smtp = SMTP_SSL(self.host, int(self.port))
            smtp.login(self.user, self.pwd)
            smtp.sendmail(self.user, self.receivers, message.as_string())
        except Exception as e:
            error(f'发送邮件: {title} 失败。原因: {e}')
            return False
        else:
            mess = ', '.join(self.receivers)
            info(f'发送成功，给: {mess}')
            info(f'EMAIL: {title} {content}')
            return True

        finally:
            smtp.quit()


class UserConfig(object):
    def __init__(self, file_path: str = CONFIG_PATH) -> None:
        self.path = file_path

        self.user: Union[User, None] = None
        self.timer: Union[Timer, None] = None
        self.email: Union[Email, None] = None

        self.file_parser()

    def file_parser(self):
        '''
        解析.
        '''
        # 读文件
        try:
            with open(self.path, 'r', encoding='utf-8') as fr:
                content = toml.load(fr)
            # 解析
            self.user = User()
            self.user.id = content.get('user').get(User.ID)
            self.user.pwd = content.get('user').get(User.PWD)

            self.timer = Timer()
            self.timer.points_in_time = content.get(
                'timer').get(Timer.POINTS_IN_TIME)
            self.timer.dead_line = content.get('timer').get(Timer.DEAD_LINE)

            self.email = Email()
            email_part: dict = content.get('email')
            self.email.enable = bool(email_part.get(Email.ENABLE))
            self.email.sender = email_part.get(Email.SENDER)
            self.email.user = email_part.get(Email.USER)
            self.email.pwd = email_part.get(Email.PWD)
            self.email.receivers = email_part.get(Email.RECEIVERS)
            self.email.port = email_part.get(Email.PORT)
            self.email.host = email_part.get(Email.HOST)

        except Exception as e:
            raise ConfigParserError(f'无法解析配置文件: {self.path}, 原因: {e}')
