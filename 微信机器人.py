# -*- coding: utf-8; py-indent-offset:4 -*-
from wxauto import *
from pprint import pprint
import time

# 获取当前微信客户端
wx = WeChat()

# 获取会话列表
sx_list = wx.GetSessionList()
pprint(sx_list)

msg = '自动发送消息测试'
who = '禁言  白菜链接群'
who_list = [
    '禁言  白菜链接群',
    '熊志标',
    '文件传输助手',
    '🐯'
]


msgs = wx.GetLastMessage
pprint(msgs)
# for msg in msgs:
#     print('%s : %s'%(msg[0], msg[1]))

while True:
    for who in who_list:
        wx.ChatWith(who)  # 打开`文件传输助手`聊天窗口
        wx.SendMsg(msg+"--->"+who)  # 向`文件传输助手`发送消息：你好~
        time.sleep(1)