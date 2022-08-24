#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: one_day.py
# 说明:
# 时间: 2022/08/24 15:12:16
# 作者: Azure
# 版本: 1.0

from tools.tjupt_bot import Bot
from version import hello

hello()

bot = Bot()

bot.auto_att_oneday()
