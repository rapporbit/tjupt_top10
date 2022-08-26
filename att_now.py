#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: att_now.py
# 说明: 
# 时间: 2022/08/26 09:40:24
# 作者: Azure
# 版本: 1.0

from tools.tjupt_bot import Bot
from version import hello

hello()

bot = Bot()


bot.last_att(True)


