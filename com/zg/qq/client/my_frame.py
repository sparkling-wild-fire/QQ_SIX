# -*- coding:utf-8 -*-
# @Time    :2019/7/20 15:47
# @Author  :曾格

""""定义Frame窗口基类"""

import logging
import socket
import sys # 这个模块可供访问由解释器使用或维护的变量和与解释器进行交互的函数。
           # os这个模块提供了一种方便的使用操作系统函数的方法。
import wx

logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# 服务器IP
SERVER_IP='127.0.0.1'
# 服务器端口号
SERVER_PORT=8888
# 服务器地址
server_address=(SERVER_IP,SERVER_PORT)

# 操作命令代码
COMMAD_LOGIN=1     # 登录命令
COMMAD_LOGOUT=2    # 下线命令
COMMAD_SENDMSG=3   # 发送消息命令
COMMAD_REFRESH=4   # 刷新好友列表命令

client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # UDP SOCKET
# 设置超时1秒，不再等待接收数据
client_socket.settimeout(1)

class MyFrame(wx.Frame):           # 所有界面的一些共有属性
    def __init__(self,title,size):
        super().__init__(parent=None,title=title,size=size,
                         style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)
        # 设置窗口居中
        self.Centre()
        # 设置Frame窗口内容面板
        self.contentpanel=wx.Panel(parent=self)

        ico=wx.Icon('resouce/icon/qq.ico',wx.BITMAP_TYPE_ICO)
        # 设置窗口图标
        self.SetIcon(ico)
        # 设置窗口的最大和最小尺寸
        self.SetSizeHints(size,size)
        self.Bind(wx.EVT_CLOSE,self.OnClose)

    def OnClose(self,event):
        # 退出系统
        self.Destroy()
        client_socket.close()
        sys.exit(0)

