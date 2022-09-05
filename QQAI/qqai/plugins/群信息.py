from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot,GroupMessageEvent
import ast
Group_information = on_command('qxx',aliases={'群信息'},priority=5)
@Group_information.handle()
async def qxx(bot:Bot,event:GroupMessageEvent):
    group = event.group_id
    information = await bot.call_api('get_group_info',**{'group_id':group})
    data = ast.literal_eval(str(information))
    msg = f"群号  ：{data['group_id']}\
          \n群名称：{data['group_name']}\
          \n成员数：{data['member_count']}\
          \n最大成员数：{data['max_member_count']}"
    await bot.send(
        event   = event,
        message = msg
    )
