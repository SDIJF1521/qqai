from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
import pymysql
import requests
import re
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='qqai'
    )
cursor=conn.cursor()

web = on_command("web", aliases={"官网"}, priority=5)

@web.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    cursor.execute('select name from web')
    library = cursor.fetchall()
    name = []
    for i in range(len(library)):
        name.append(library[i][0])

    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值




@web.got("city", prompt="你想查询那个官网")
async def handle_city(event:GroupMessageEvent,bot:Bot, city_name: str = ArgPlainText("city")):
    DANGER = r'(!)|(-- -)|(#)|(or)|(ande)|(slelct)(from)|(union)|(ORDER)'
    testing = re.search(DANGER,city_name,re.I)
    if testing != None:
        await Warehousing.send('小白判断可能存在SQL注入威胁程序终止,(是小白做错什么了)')
    else:
        cursor.execute('select name from web')
        library = cursor.fetchall()
        name = []
        for i in range(len(library)):
            name.append(library[i][0])



        city_weather = await get_weather(city_name)
        await web.finish(city_weather)




#获取url
async def get_weather(city: str) -> str:
    cursor.execute('select name from web')
    library = cursor.fetchall()
    name = []
    for i in range(len(library)):
        name.append(library[i][0])

    if city not in name:  # 判断网站是否在数据库中
        await web.send('很抱歉小白没有收录该网站，您可以使用入库命令进行网站的收录')
    else:
        cursor.execute('select * from web where name=%s',city)
        library_data = cursor.fetchone()
        Url = library_data[1
        ]
        return f"{city}官网是:http://"+Url

Warehousing = on_command('Warehousing',aliases={"入库"}, priority=4)
@Warehousing.handle()
async def parameter (matcher: Matcher, args: Message = CommandArg()):
    Protoginseng= args.extract_plain_text()  # 首次发送命令时跟随的参数
    if Protoginseng:
        matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值
@Warehousing.got("city", prompt="请按 网站名称|网址 方式写入")
async def Deposit(event:GroupMessageEvent,bot:Bot, city_name: str = ArgPlainText("city")):
    try:
        cursor.execute('select name from web')
        library = cursor.fetchall()
        name = []
        for i in range(len(library)):       #提取网址和名称
            name.append(library[i][0])

        name1 = ''
        url = ''
        A = 0
        await Warehousing.send(url)
        while A < len(city_name)+1 and city_name[A] != '|':
            name1 = name1+city_name[A]
            A+=1
        DANGER = r'(!)|(-- -)|(#)|(or)|(and)|(slelct)|(\')|(FROM)|(union)|(ORDER)'
        #await Warehousing.send(name1)
        url = url+city_name[A+1:len(city_name)]
        #判断网站是否存在数据库
        testing = re.search(DANGER,name1,re.I)
        if testing != None:
            await Warehousing.send('小白判断可能存在SQL注入威胁程序终止,(是小白做错什么了)')
        else:
            if name1 in name:
                await Warehousing.send('该网站已被收录')
            else:
                try:
                    await Warehousing.send(url)
                    Response_value = requests.get('http://'+url)
                    Response = str(Response_value)
                    await Warehousing.send('insert into web (name,url) values (%s,%s")'%(name1,url))
                    if Response != '<Response [200]>':
                        await Warehousing.send('小白找不到该网站无法进行收录')
                    else:
                        cursor.execute('insert into web (name,url) values ("%s","%s")'%(name1,url))
                        await Warehousing.send('网站已经成功收录')
                        conn.commit()
                except:
                    await Warehousing.send('程序出错了小白无法进行收录::>_<::')
    except:
        await Warehousing.send('程序错误已终止{{{(>_<)}}}')