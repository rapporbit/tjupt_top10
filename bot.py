#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: bot.py
# 说明:
# 时间: 2022/08/19 15:54:57
# 作者: Azure
# 版本: 1.0

from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger

from tools import debug, error
from tools.tjupt_bot import Bot


def main():
    scheduler = BackgroundScheduler()
    try:
        bot = Bot()
        trs = []
        for item in bot.config.timer.points_in_time:
            item = item.split(':')
            item = [int(i) for i in item]
            if item[1] == 0:
                item[1] = 59
                item[0] = item[0] - 1
            else:
                item[1] = item[1] - 1

            debug(f'计划的时间: {item}')

            tr = CronTrigger(hour=item[0], minute=item[1])
            trs.append(tr)

        dead_line = bot.config.timer.dead_line.split(':', 1)
        dead_line = [int(i) for i in dead_line]
        if dead_line[1] == 0:
            dead_line[1] = 59
            dead_line[0] = dead_line[0] - 1
        else:
            dead_line[1] = dead_line[1] - 1

        tr_end = CronTrigger(
            hour=dead_line[0],
            minute=dead_line[1]
        )
        debug(f'最后的时间: {dead_line}')
        trs_ = OrTrigger(trs)
        # debug(trs_)
        if not len(trs):
            raise ValueError('时间列表不能是0个')

        scheduler.add_job(
            bot.tomorrow,
            tr_end,
            id='end',
            name='end'
        )
        scheduler.add_job(
            bot.auto_att_oneday,
            trs_,
            id='day',
            name='day'
        )
        scheduler.add_job(
            bot.tomorrow,
            CronTrigger(
                hour=23,
                minute=30
            ),
            id='tomorrow',
            name='tomorrow'
        )
        scheduler.start()

        while 1:
            sleep(60)

    except Exception as e:
        error(f'错误: {e}')
    finally:
        scheduler.pause()
        scheduler.remove_all_jobs()
        scheduler.shutdown()


if __name__ == '__main__':
    main()
