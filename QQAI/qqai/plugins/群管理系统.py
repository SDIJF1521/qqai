from nonebot import on_command
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, Bot
import pymysql
import ast
import re
# 连接数据库
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='qqai'
    )
cursor = conn.cursor()


# 操作事件
menu = on_command('管理菜单', priority=5)
@menu.handle ()
async def cd (event:Event,event1:GroupMessageEvent,bot:Bot):
    cursor.execute('select admin from gl')
    library = cursor.fetchall()
    userID = []
    for i in range(len(library)):
        userID.append(str(library[i][0]))
    user_id = event.get_user_id()
    user = event1.group_id
    await menu.send(str(user))
    if user_id in userID and user == 群号:
        await menu.send('群管菜单 \n1. /开启群禁言\n2. /关闭群禁言\n3. /禁言\n4. /踢出')

#no群禁言事件
Taboo_NO = on_command('开启群禁言',priority=5)
@Taboo_NO.handle()
async def jy_no(event:Event,bot:Bot,event1:GroupMessageEvent):
    cursor.execute('select admin from gl')
    library = cursor.fetchall()
    userID = []
    for i in range(len(library)):
        userID.append(str(library[i][0]))
    user_id = event.get_user_id()
    user = event1.group_id
    if user_id in userID and user == 群号:
        implement = await bot.call_api('set_group_whole_ban',**{'group_id':群号,'enable':True})
        await Taboo_NO.send(Message('[CQ:tts,text=群禁言已开启]'))
#off群禁言事件
Taboo_OOF = on_command('关闭群禁言',priority=5)
@Taboo_OOF.handle()
async def jy_oof(event:Event,bot:Bot,event1:GroupMessageEvent):
    user_id = event.get_user_id()
    cursor.execute('select admin from gl')
    library = cursor.fetchall()
    userID = []
    for i in range(len(library)):
        userID.append(str(library[i][0]))
    user_id = event.get_user_id()
    user = event1.group_id
    if user_id in userID and user == 群号:
        implement = await bot.call_api('set_group_whole_ban',**{'group_id':群号,'enable':False})
        await Taboo_NO.send(Message('[CQ:tts,text=群禁言已关闭]'))
#禁言事件
banned_to_post = on_command('禁言',priority=5)
@banned_to_post.handle()
async def jy(event:Event,Event:GroupMessageEvent,bot:Bot):
    cursor.execute('select admin from gl')
    library = cursor.fetchall()
    userID = []
    for i in range(len(library)):
        userID.append(str(library[i][0]))
    user_id = event.get_user_id()
    user = Event.group_id
    if user_id in userID and user == 群号:

        primary_bata = Event.get_event_description()
        rule=re.compile('\[CQ:at,qq=(\d+)]')
        name_list=rule.findall(primary_bata)             #提取用户账号
        rule_time = re.compile(']</le> (\d+)')
        time_list=rule_time.findall(primary_bata)        #提取设置禁言时间
        if not len(name_list) == 0:
            for i in range(0,len(time_list)):
                time_list[i]=int(time_list[i])
            if len(name_list) == len(time_list):
                for i in range(0, len(name_list)):  # jiangsj
                    time_list[i] = int(time_list[i])
                Relation = dict(zip(name_list,time_list))
                print(name_list, '\n',time_list, '\n',primary_bata,'\n',Relation)
                if not '群主' in name_list:
                    msg = ''
                    msg1=''
                    name = []
                    name1=[]
                    for j in range(0,len(Relation)):
                        print(Relation[name_list[j]])
                        Execute = await bot.call_api('set_group_ban',**{"group_id":Event.group_id,'user_id':name_list[j],'duration':Relation[name_list[j]]*60})
                        if not Relation[name_list[j]] == 0:
                            msg = msg+'[CQ:at,qq=%s]\n' % (name_list[j])
                            name.append(name_list[j])                      # 禁言名单
                        else:
                            name1.append(name_list[j])                    # 放出名单
                            for i in range(len(name1)):
                                msg1 = msg1 +'[CQ:at,qq=%s]\n' % (name1[i])
                    if len(name) > 0:
                        await banned_to_post.send(Message('禁言成功\n'+msg+"\n已被关进小黑屋(●\'◡\'●)"))
                    if len(name1) > 0:
                        await banned_to_post.send(Message(msg1 + "\n已被管理放出小黑屋(●\'◡\'●)"))
                else:
                    await banned_to_post.send('该用户是白名单成员无法被禁言哦(^///^)')
            else:
                await banned_to_post.send('小白检测到一个用户的禁言时间未设置程序终止')
        else:
            await banned_to_post.send('name_list = NULL程序终止')
#踢出事件
Kick_out = on_command('踢出',priority=5)
@Kick_out.handle()
async def TC(Event:Event,event:GroupMessageEvent,bot:Bot):
    cursor.execute('select admin from gl')
    library = cursor.fetchall()
    userID = []
    for i in range(len(library)):
        userID.append(str(library[i][0]))
    user_id = Event.get_user_id()
    user = event.group_id
    if  user_id in userID and user == 群号:
        Data = event.get_event_description()
        rule = re.compile('\[CQ:at,qq=(\d+)]')
        name_list = rule.findall(Data)
        for i in name_list:
            await bot.call_api('set_group_kick',**{'group_id':event.group_id,'user_id':int(i)})
        await Kick_out.send('操作成功')
#刷新事件
Refresh = on_command('sx',aliases={'刷新'},priority=5)
@Refresh.handle()
async def sx (bot:Bot,Event:GroupMessageEvent):
    user = Event.group_id
    if user == 群号:
        cursor.execute('select admin from gl')
        library = cursor.fetchall()
        userID = []
        for i in range(len(library)):
            userID.append(str(library[i][0]))
        print(library)
        user = await bot.call_api('get_group_member_list',**{'group_id':Event.group_id})
        Admin = []
        for ID in user:
            admin = ID['user_id']
            identity = await bot.call_api('get_group_member_info',**{'group_id':Event.group_id,'user_id':admin})
            data = ast.literal_eval(str(identity))
            msg = f'{data["role"]}'
            print(msg)
            if msg == 'owner' or msg == 'admin':
                Admin.append(str(ID['user_id']))
                if not str(admin) in userID:
                    cursor.execute('insert into gl (admin) values ("%s")',(int(admin)))
                    conn.commit()
        Notadmin = set(userID) - set(Admin)
        print(userID)
        print(Admin)
        for i in Notadmin:
            cursor.execute('delete from gl where admin = %s',i)
            conn.commit()
        at = ''
        for j in Admin:
            print(j)
            at=at+('.'
                   '[CQ:at,qq='+j+'];\n')
        print(at)
        mag=Message('刷新完毕!\n管理成员:\n'+at)
        await Refresh.send(mag)
