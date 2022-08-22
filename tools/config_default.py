#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: config_default.py
# 说明: 
# 时间: 2022/08/19 20:59:05
# 作者: Azure
# 版本: 1.0

DEFAULT_CONFIG = r'''
# TJUPT_Bot 配置

# 以 "#" 开始的行为 注释，不会被程序读取，比如本行
# [注意]: 除非必要，请使用英文标点
# 修改完后，请将本文件名改为 `config.toml` 即，去掉文件名中的 `_demo`

# 用户相关
[user]
# 用户ID
id = "****"
# 对应密码
pwd = "*****"

# 定时器 [!不建议修改!]
# 增加每日0、6、7、8、12、18、20、22点签到各前10名，下次连续签到时，获得的魔力值将翻倍
[timer]
# 定时，每天尝试签到的时间点 
# 计划运行时，会找到与现在时间最近的一次签到时间点，并等待尝试签到
# 如果失败，会等待下一个时间点
# 如果都失败了，就会由 dead_line 接管，保持 连续签到 （前提是程序保持运行）
# 目前不支持 '00:00' !!
# 推荐默认！
points_in_time = ["06:00", "07:00", "08:00", "12:00"]
# dead_line 必须在上边的之后
# dead_line 作用是，当设定的时间点都 失败 后，为保证 连续签到 设计的
# 当 dead_line 也失败后，会发送邮件提醒你手动签到（如果打开邮箱功能）
dead_line = "18:00"
# 网络延迟提前量
# 可以按照经验适当增加此数值
p_t = "0.01"


# 邮件提醒
[email]
# 是否开启 0 关闭，1 开启
enable = 0
# 发送邮箱 可以与用户相同
sender = "f****@qq.com"

# 用户
user = "20*****@qq.com"

# 授权码，参考：https://service.mail.qq.com/cgi-bin/help?subtype=1&&no=1001256&&id=28
pwd = "mh********dgbd"

# 接受者 支持多个接收者
# 用用英文逗号隔开 比如：["user1", "user2", "user3"]
receivers = ["a******q@qq.com"]

# port
port = "465"

# host
host = "smtp.qq.com"

'''.strip()