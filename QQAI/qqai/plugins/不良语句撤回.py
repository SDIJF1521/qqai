from nonebot import on_regex, on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Bot,Event,Message
import re
import pymysql
price = False
#连接数据库
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='qqai'
    )

cursor=conn.cursor()


blacklist = on_command('*',priority=9)
delete = on_command('-*',priority=9)
withdraw = on_regex('.+',priority=10)
inquire = on_command('$*',priority=9)
@blacklist.handle()
async def forbid_word(event1:GroupMessageEvent,event:Event):
    cursor.execute('select admin from gl')
    library = cursor.fetchall()
    userID = []
    for i in range(len(library)):
        userID.append(str(library[i][0]))
    user_id = event.get_user_id()
    user = event1.group_id
    if user_id in userID and user == 群号:
        cursor.execute('select wordlist from word')
        blacklist_word = cursor.fetchall()
        blacklist_word_list = []
        for i in range(len(blacklist_word)):
            blacklist_word_list.append(blacklist_word[i][0])
        print(blacklist_word_list)
        Data = event.get_event_description()
        criterion = re.compile('\*(.+)')
        original_data = (criterion.search(Data).group())[1:len((criterion.search(Data).group()))-1]       #提取参数

        if len(original_data) > 0:
            record = ''
            record1=''
            woed1 = re.split('\|',original_data)           #分割参数
            for i in range(len(woed1)):
                if not woed1[i] in blacklist_word_list:
                    sql = "insert into word (wordlist) values (%s)"
                    cursor.execute(sql , (woed1[i]))
                    conn.commit()
                    record = record+'|'+woed1[i]+'|'
                else:
                    record1=record1+'|'+woed1[i]+'|'
            await blacklist.send('操作成功\n'+record+'\n词汇添加成功\n'+record1+'\n词汇已存在数据库')
    else:
        await blacklist.send('没有数据？')




@delete.handle()
async def dl(event1:GroupMessageEvent,event:Event):
    cursor.execute('select admin from gl')
    library = cursor.fetchall()
    userID = []
    for i in range(len(library)):
        userID.append(str(library[i][0]))
    user_id = event.get_user_id()
    user = event1.group_id
    if user_id in userID and user == 群号:
        cursor.execute('select wordlist from word')
        blacklist_word = cursor.fetchall()
        blacklist_word_list = []
        for i in range(len(blacklist_word)):
            blacklist_word_list.append(blacklist_word[i][0])
        print(blacklist_word_list)
        Data = event.get_event_description()
        criterion = re.compile('\*(.+)')
        original_data = (criterion.search(Data).group())[1:len((criterion.search(Data).group()))-1]       #提取参数
        if len(original_data) >0:
            record = ''
            record1=''
            woed1 = re.split('\|',original_data)           #分割参数
            for i in range(len(woed1)):
                if woed1[i] in blacklist_word_list:
                    cursor.execute( "delete from word where wordlist = %s", (woed1[i]))
                    conn.commit()
                    record = record+'|'+woed1[i]+'|'
                else:
                    record1=record1+'|'+woed1[i]+'|'
            await blacklist.send('操作成功\n'+record+'\n词汇删除成功\n'+record1+'\n词汇不在数据库')
    else:
        await blacklist.send('没有数据？')
#消息撤回事件
@withdraw.handle()
async def WM(event:GroupMessageEvent,bot:Bot):
    user = event.group_id
    if user == 群号:
        cursor.execute('select wordlist from word')
        word = cursor.fetchall()
        word_list = []
        for i in range(len(word)):
            word_list.append(word[i][0])
        cursor.execute('select admin from gl')
        library = cursor.fetchall()
        userID = []
        for i in range(len(library)):
            userID.append(str(library[i][0]))
        for i in range(len(userID)):
            userID[i] = str(userID[i])
        if not  str(event.get_user_id()) in userID:
            print(userID, '\n' + str(event.get_user_id()))
            Data1 = re.compile('.+|').findall(event.get_event_description())
            Data2 = ''
            for i in Data1:
                Data2= Data2+i
            for j in word_list:
                Data = re.compile(j,re.IGNORECASE).findall(re.compile('] "(.+)').search(Data2).group().replace(' ',''))
                print(Data2 ,'\n'+re.compile('\[群:群号] "(.+)').search(Data2).group().replace(' ',''),'\n',Data,'\n'+j)
                if len(Data) !=0:
                    await bot.delete_msg(message_id=event.message_id)
                    break
@inquire.handle()
async def CK(event:GroupMessageEvent,Event:Event):
    cursor.execute('select admin from gl')
    library = cursor.fetchall()
    userID = []
    for i in range(len(library)):
        userID.append(str(library[i][0]))
    user_id = Event.get_user_id()
    user = event.group_id
    if user_id in userID and user == 群号:
        cursor.execute('select wordlist from word')
        blacklist_word = cursor.fetchall()
        blacklist_word_list = []
        for i in range(len(blacklist_word)):
            blacklist_word_list.append(blacklist_word[i][0])
        await inquire.send(str(blacklist_word_list))
