from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Bot,GroupMessageEvent
import requests
import re
import os
request_a_song = on_command("dg",aliases={"点歌"}, priority=5)


@request_a_song.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值


@request_a_song.got("city", prompt="歌名：")
async def handle_city(bot:Bot,event:GroupMessageEvent,city_name: str = ArgPlainText("city")):
    try:
        url = 'https://music.cyrilstudio.top/search?keywords=' + city_name
        a = requests.get(url)
        a.encoding = 'utf-8'
        print(re.findall('id":(\d+.)', a.text)[0][0:-1])
        print(re.findall('id":(\d+.)', a.text))

        Data = requests.get('http://music.163.com/song/media/outer/url?id=' + re.findall('id":(\d+.)', a.text)[0][0:-1] + '.mp3').content
        with open(city_name + '.mp3', mode='wb') as f:
            f.write(Data)
            f.close()
        print('Ok')
        await bot.call_api('upload_group_file',**{'group_id':event.group_id,'file':'C:/Users/83968/Desktop/qqAI/QQAI/'+city_name + '.mp3','name':city_name+'.mp3'})
        os.remove('C:/Users/83968/Desktop/qqAI/QQAI/'+city_name + '.mp3')
    except:
        os.remove('C:/Users/83968/Desktop/qqAI/QQAI/' + city_name + '.mp3')
        print('OK')
        await request_a_song.finish('小白找不到歌曲{{{(>_<)}}}')

KW_request_a_song = on_command("kwdg",aliases={"酷我点歌"}, priority=5)


@KW_request_a_song.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值


@KW_request_a_song.got("city", prompt="歌名：")
async def handle_city(bot:Bot,event:GroupMessageEvent,city_name: str = ArgPlainText("city")):
    url = 'http://search.kuwo.cn/r.s?all=' + city_name + '&ft=music& itemset=web_2013&client=kt&pn={1}&rn={2}&rformat=json&encoding=utf8'
    a = requests.get(url)
    a.encoding = 'utf-8'
    s = re.findall('(MUSIC_\d+)', a.text)
    print(a.text, '\n', s[0])
    URL = requests.get(
        'http://antiserver.kuwo.cn/anti.s?type=convert_url&rid=' + s[0] + '&format=aac|mp3&response=url')
    await KW_request_a_song.finish(URL.text)