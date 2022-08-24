#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: version.py
# 说明:
# 时间: 2022/08/24 15:03:11
# 作者: Azure
# 版本: 1.0

class Version(object):
    # 版本号，如果带有beta字符则为测试版
    VERSION = '0.2.0'
    # 发布日期 年-月-日
    RELEASE = '2022-08-24'

    # 横幅
    BANNER = r"""
  ______  ____  ______  ______   __          __ 
 /_  __/ / / / / / __ \/_  __/  / /_  ____  / /_
  / /_  / / / / / /_/ / / /    / __ \/ __ \/ __/
 / / /_/ / /_/ / ____/ / /    / /_/ / /_/ / /_  
/_/\____/\____/_/     /_/    /_.___/\____/\__/  
"""

    # 发布说明
    NOTE = r'''
    1. 增加稳定性;
    2. 修复bug;'''


def hello():
    '''say hello'''
    print(Version.BANNER)
    print(f'版本号：{Version.VERSION}', f'发布日期：{Version.RELEASE}')
    print()
    print(f'发布说明：{Version.NOTE}')
    print()
    if 'beta' in Version.VERSION:
        print('你正在使用的是测试版！')
        print('可能会经常出现BUG！')
        print('请及时回到正式版！')

    print('\n你好！欢迎使用本程序！\n')


if __name__ == '__main__':
    hello()
