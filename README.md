# qqai
这是一个高度依赖mysql数据库的机器人
这个机器人有一下功能

签到
抽签
解签
帮助
群信息
点歌
酷我点歌
积分查询
天气
不良言语撤回  （不限制群管理和群主）
刷新

管理菜单    （只有群主&管理可用）

开启群禁言   （只有群主&管理可用）

关闭群禁言    （只有群主&管理可用）

\*[不良词汇添加] （只有群主&管理可用）

\-*[不良词汇删减] （只有群主&管理可用）

\$*[不良词汇查看]  （只有群主&管理可用）

<iframe src="//player.bilibili.com/player.html?aid=730212694&bvid=BV1PD4y1z7XL&cid=823693531&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>


如果你要使用这个机器人的话那么你需要这样做
首先请确保你的计算机上面有mysql数据库（最好mysql的用户名和密码都为root）和以下第三方库：
                                                 - pymsql
                                                 - datetime
                                                 - random
入上述的东西全度都具备了那那你需要先对数据库进行简单的操作，(在这里最好你拥有Navicat 15 for MySQL软件这样会便于你的操作)

首先你要创建一个名为qqai的数据库在数据库里面要创建5张表

第一张表名为web字段为name ; url 类型 varchar

第二张表名为qd 字段 name ; 积分 日期 ； 天数 类型 varchar ； int ; varchar ; int

第三张表名为cq 字段 name ; id ; 日期 类型 varchar ； int ; varchar

第四张表名为 gl 字段 admin 类型 varchar

第五表名为 word 字段 wordlist 类型 varchar

五张表创建完毕后再将sgin.txt文件导入进qqai数据库

到这里数据库的就配置完毕了接下来要对源码进行更改

web入库.py , 不良语句撤回.py , 抽签解签.py , 群管理系统.py , 签到.py 这些程序都是用到了mysql如果你的mysql用户名和密码不是root那么请吧这些文件的user=后面的改为你的mysql用户名password=后面的改为你的mysql密码

再接着把 群管理系统.py，不良语句撤回.py里面的群号 改为你自己的群号 ，把 群管理系统.py里面的群主qq改为你当前的群主qq号

上述操作都完成后请确保qq机器人为群管理否则将会用1/3的功能无法使用同时在使用机器人是您要做的第一件事情是使用刷新命令给群主和群管理添加操作权限如果不这样做的话机器人就无法发挥它应有的功效
