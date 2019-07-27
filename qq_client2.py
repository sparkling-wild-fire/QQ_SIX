# -*- coding:utf-8 -*-
# @Time    :2019/7/24 9:51
# @Author  :曾格

# -*- coding:utf-8 -*-
# @Time    :2019/7/21 21:52
# @Author  :曾格

import logging
import wx
from com.zg.qq.client.login_frame import LoginFrame

logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(threadName)s'
                    '%(name)s-%(funcName)s-%(levelname)s-%(message)s')
logger=logging.getLogger(__name__)

class App(wx.App):
    def OnInit(self):
        # 创建窗口对象
        frame=LoginFrame()
        frame.Show()
        return True

if __name__=='__main__':
    app=App()
    app.MainLoop()