from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent
BZ = on_command('help',aliases={'帮助'},priority=5)
@BZ.handle()
async def bz (event:GroupMessageEvent):
    user = event.group_id
    if user == 566077032:
        await BZ.send('1. /官网 \n2. /入库 \n3. /签到 \n4. /点歌\n5. /抽签\n6. /解签 \n7. /积分查询\n8. /群信息\n9. /天气\n10. /刷新')
    else:
        await BZ.send('1. /官网 \n2. /入库 \n3. /签到 \n4. /点歌\n5. /抽签\n6. /解签 \n7. /积分查询\n8. /群信息\n9. /天气')