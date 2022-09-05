from nonebot import on_command
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent,Message
import datetime
import pymysql
import random

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='qqai'
    )
cursor=conn.cursor()
draw = on_command('cq', aliases={'抽签'},priority=5)                         #注册抽签事件
@draw.handle()
async def cq (event:Event,bot:Bot,S:GroupMessageEvent):
    #获取数据库cq表的name信息
    cursor.execute('select name from cq')
    library = cursor.fetchall()
    name = []
    cursor.execute('select id from sgin')
    value = cursor.fetchall()
    tobay = datetime.date.today()
    id = random.randint(1,(len(value)))
    for i in range(len(library)):                                       #从mysql数据库中获取neme
        name.append(library[i][0])
    user_id = event.get_user_id()
    if not str(user_id) in name:                                        #判断用户id是否存在数据库中
        #用户id不在数据库中的执行事件
        cursor.execute('insert into cq (name,id,日期) values ("'+str(user_id)+'","'+str(id)+'","'+str(tobay)+'")')
        conn.commit()
        cursor.execute('select * from sgin where id = "'+str(id)+'"')
        sgin = cursor.fetchone()
        out = '[CQ:at,qq=' + str(user_id) +']\n抽到诸葛神签第'+str(id)+'签\n签诗:'+str(sgin[1]+'\n发送【解签】可解出该签诗')
        await draw.send(Message(out))
    else:
        cursor.execute('select * from cq where name = "'+user_id+'"')
        date = cursor.fetchone()
        if str(datetime.date.today()) != str(date[-1]):
            cursor.execute('update cq set id = '+str(id)+' where name = "'+str(user_id)+'"')
            cursor.execute('update cq set 日期 = "' + str(tobay) + '" where name = "' + str(user_id) + '"')
            conn.commit()
            cursor.execute('select * from sgin where id = "' + str(id) + '"')
            sgin = cursor.fetchone()
            out = '[CQ:at,qq=' + str(user_id) + ']\n抽到诸葛神签第' + str(id) + '签\n签诗:' + str(sgin[1] + '\n发送【解签】可解出该签诗')
            await draw.send(Message(out))
        else:
            out = '[CQ:at,qq=' + str(user_id) + ']您今天已经抽过签了请明天再来把ヽ(✿ﾟ▽ﾟ)ノ'
            await draw.send(Message(out))
draw = on_command('cq', aliases={'抽签'},priority=5)
Unmarshalling = on_command('jq',aliases={'解签'},priority=5)
@Unmarshalling.handle()
async def jq (event:Event,bot:Bot):
    if True:
       cursor.execute('select name from cq')
       library = cursor.fetchall()
       name = []
    for i in range(len(library)):  # 从mysql数据库中获取neme
        name.append(library[i][0])
    user_id = event.get_user_id()
    if not str(user_id) in name:
        out = '[CQ:at,qq=' + str(user_id) +']您还没有抽过签呢'
        await draw.send(Message(out))
    else:
        cursor.execute('select * from cq where name = "'+user_id+'"')
        date = cursor.fetchone()
        if str(datetime.date.today()) != str(date[-1]):
            out = '[CQ:at,qq=' + str(user_id) + ']您还没有抽过签呢'
            await draw.send(Message(out))
        else:
            cursor.execute('select * from cq where name = "'+user_id+'"')
            id = cursor.fetchone()
            cursor.execute('select * from sgin where id = "'+str(id[1])+'"')
            content = cursor.fetchone()
            out = '[CQ:at,qq=' + str(user_id) + ']签诗内容如下：\n'+content[2]
            await Unmarshalling.send(Message(out))