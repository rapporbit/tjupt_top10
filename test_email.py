#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: test_email.py
# 说明: 
# 时间: 2022/08/19 18:50:55
# 作者: Azure
# 版本: 1.0

from tools.config_file import UserConfig
from tools import debug, info

conf = UserConfig()

if conf.email.send_email('TJUPT_Bot 邮箱测试', '如果你及时收到了本邮件，说明通过了测试，可以放心使用邮箱提醒功能'):
    info(f'【测试】：{conf.email.receivers} 发送成功')
else:
    info(f'【测试】：{conf.email.receivers} 发送失败，请检查是否开启了email功能或者相关参数')
