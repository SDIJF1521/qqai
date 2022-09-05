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
qd = on_command("qd", aliases={"签到"},priority=5)                           #注册签到事件
@qd.handle()
async def Sign_in(event:Event,bot:Bot,S:GroupMessageEvent):
    cursor.execute('select name from qd')
    library = cursor.fetchall()
    name = []
    integral = random.randint(1, 20)
    for i in range(len(library)):                                           #从mysql数据库中获取neme
        name.append(library[i][0])
    user_id = event.get_user_id()
    ID = str(S.group_id)
    tobay = datetime.date.today()
    if not user_id+'|'+ID in name:                                        #判断用户id是否存在数据库中
        if str(tobay) == '2022-08-08' or str(tobay) == '2022-08-09':
            integral50 = integral+50
            cursor.execute('insert into qd (name,积分,日期,天数) values ("' + str(user_id) + '|' + ID + '",' + str(
                integral50) + ',"' + str(tobay) + '","1")')
            conn.commit()
            out = '[CQ:at,qq=' + str(user_id) + ']:\n签到成功获得: ' + str(integral)+ '点积分额外附加50点\n当前积分为:' + str(
                integral50) + '点\n' + '已签到: 1天'
            outp = Message(out)
            await qd.send(outp)
        #用户id不存在数据库中则进行存入操作
        else:
            cursor.execute('insert into qd (name,积分,日期,天数) values ("'+str(user_id)+'|'+ID+'",'+str(integral)+',"'+str(tobay)+'","1")')
            conn.commit()
            out = '[CQ:at,qq='+str(user_id)+']:\n签到成功获得: '+str(integral)+'点积分\n当前积分为:'+str(integral)+'点\n'+'已签到: 1天'
            outp = Message(out)
            await qd.send(outp)
    else:
        cursor.execute('select * from qd where name = "'+user_id+'|'+ID+'"')
        date = cursor.fetchone()
        if str(datetime.date.today()) != str(date[-2]):
            cursor.execute('update qd set 积分= 积分+'+str(integral)+' where name = "'+str(user_id)+'|'+ID+'"')
            cursor.execute('update qd set 日期= "'+str(datetime.date.today())+'" where name = "'+str(user_id)+'|'+ID+'"')
            cursor.execute('update qd set 天数= 天数 + 1 where name = "'+ str(user_id)+'|'+ID+'"')
            conn.commit()
            cursor.execute('select * from qd where name="'+str(user_id)+'|'+ID+'"')
            sql = cursor.fetchone()
            out = '[CQ:at,qq=' + str(user_id) + ']:\n签到成功获得: '+str(integral)+'点积分\n当前积分为: ' + str(sql[-3]) + '点\n'+'已签到: '+str(sql[-1])+'天'
            outp = Message(out)
            await qd.send(Message(outp))
        else:
            out = '[CQ:at,qq=' + str(user_id) + ']今天你已经签过到了请明天再来把(≧∇≦)ﾉ'
            await qd.send(Message(out))
query = on_command('cx',aliases={'积分查询'},priority=5)
@query.handle()
async def cx(event:Event,S:GroupMessageEvent,bot=Bot,):
    user_id = event.get_user_id()
    ID = str(S.group_id)
    cursor.execute('select * from qd where name="' + str(user_id) +'|' + ID + '"')
    sql = cursor.fetchone()
    out = '[CQ:at,qq=' + str(user_id) + '] 您当前的积分为：'+str(sql[-3])+'点'
    await query.send(Message(out))