# tjupt_qiandao_top10

#### 介绍
-   TJUPT 努力TOP10


#### 声明
-   本脚本仅作为学习使用，使用本脚本的签到功能属于 **不正当** 的行为
-   请维护 *TJUPT* 的良好环境
-   大部分代码 *参考/直接使用* 自 [TjuptAutoAttendance](https://github.com/Xzonn/TjuptAutoAttendance)
-   原版最好的功能是可以用 GitHub Action 来自动完成，但是稳定性欠佳，速度也有优化空间，同时也没有失败提醒
-   此版本缺少了对 GitHub Action 的支持，只能本地使用
-   因为众所周知的原因GitHub连接有点费事，并且用 GitHub Action 比较难优化速度
-   但是原版确实很方便，如果你并不需要较高的稳定性（连续签到 & 手动检查），或等其作者更新，也是非常推荐



#### 软件架构
-   python@3.9


#### 运行逻辑 & 注意事项
-   此版本增加了失败时邮件通知（推荐使用QQ邮箱，亲测icloud邮箱延迟太高）
-   提前获取签到页面及答案，等到预定时间提交答案，来最大化答题速度，考虑到延迟，可以手动指定提前多久


#### 安装教程

1.  安装依赖: `pip install -r requirements.txt`
2.  按照 `./config.toml` 的示例填写

#### 使用说明

1.  运行 `python ./bot.py`
2.  邮箱部分 *如果打开了* 参数请参考: [qq smtp](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=166)

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

