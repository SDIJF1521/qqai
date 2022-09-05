from nonebot import export
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Message, GroupDecreaseNoticeEvent, GroupIncreaseNoticeEvent
from nonebot import on_notice

export = export()
export.name = '进群欢迎'
export.usage = '欢迎新人'

welcom = on_notice()

# 群友入群
@welcom.handle()  # 监听 welcom
async def h_r(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):  # event: GroupIncreaseNoticeEvent  群成员增加事件
    user = event.get_user_id()  # 获取新成员的id
    at_ = "本群通过祈愿召唤了勇者大人：[CQ:at,qq={}]".format(user)
    msg = at_ + '欢迎勇者大人：\n 您就是被命运召唤而来前来拯救我们的公会的勇者吗，快救救孩子们吧，希望勇者大人为我们而战！'
    msg = Message(msg)
    print(at_)
    if event.group_id == 566077032:
        await welcom.finish(message=Message(f'{msg}'))  # 发送消息

# 群友退群
@welcom.handle()
async def h_r(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State):  # event: GroupDecreaseNoticeEvent  群成员减少事件
    user = event.get_user_id()  # 获取新成员的id
    at_ = "[CQ:at,qq={}]".format(user)
    msg = at_ + '勇士离开了本群，大家快出来送别它吧！'
    msg = Message(msg)
    print(at_)

    if event.group_id == 566077032 :
        await welcom.finish(message=Message(f'{msg}'))  # 发送消息
