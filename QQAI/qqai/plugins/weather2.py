import requests
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import  Message

weather = on_command('tq',aliases={"天气", "天气预报"}, priority=5)


@weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值


@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(city: Message = Arg(), city_name: str = ArgPlainText("city")):
    url = f'http://wthrcdn.etouch.cn/weather_mini?city={city}'
    city_weather = requests.get(url=url).json()
    if city_weather['desc'] != 'OK':  # 如果参数不符合要求，则提示用户重新输入
        # 可以使用平台的 Message 类直接构造模板消息
        await weather.finish(city.template("你想查询的城市 {city} 暂不支持，暂支持国内城市"))

    city_weather = await get_weather(city=city_name, data=city_weather['data'])
    await weather.finish(city_weather)


# 在这里编写获取天气信息的函数
async def get_weather(city: str, data: dict) -> Message:
    city_weather = data

    city = city_weather['city']
    warn = city_weather['ganmao']
    now_tem = city_weather['wendu'] + '℃'
    yesterday = city_weather['yesterday']
    today = city_weather['forecast'][0]
    forecast = city_weather['forecast'][1:]

    face1 = Message('[CQ:face,id=190]')
    face2 = Message('[CQ:face,id=189]')
    k0 = '\u000a'
    k1 = '\u000a\u000a\t\t' + face1

    msg = face2 + f'城市：{city}' + k1 + '当前温度：' + now_tem + k1 + '昨日天气：' + get_day_weather(
        day_data=yesterday) + k1 + '今日天气：' + get_day_weather(
        day_data=today) + k1 + '未来天气：' + k0.join(get_day_weather(
        day_data=_) for _ in forecast) + k1 + '提醒：' + warn

    return msg


def get_day_weather(day_data: dict) -> str:
    k2 = '\u000a\t\t\t\t—'
    if 'fx' in day_data:
        msg = k2 + '时间：' + day_data['date'] + k2 + '天气：' + day_data['type'] + k2 + '高温：' + day_data[
                                                                                               'high'][
                                                                                           3:] + k2 + '低温：' + \
              day_data['low'][3:] + k2 + '风向：' + day_data['fx'] + k2 + '风力：' + day_data['fl'][9:11]
    else:
        msg = k2 + '时间：' + day_data['date'] + k2 + '天气：' + day_data['type'] + k2 + '高温：' + day_data[
                                                                                               'high'][
                                                                                           3:] + k2 + '低温：' + \
              day_data['low'][3:] + k2 + '风向：' + day_data['fengxiang'] + k2 + '风力：' + day_data['fengli'][9:11]
    return msg
