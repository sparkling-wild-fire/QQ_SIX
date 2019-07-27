# -*- coding:utf-8 -*-
# @Time    :2019/7/20 16:17
# @Author  :曾格

""""用户登录窗口"""
import json
from com.zg.qq.client.my_frame import *   # 把一些全局变量也引入,并且使用模块里的函数不需要加模块名
from com.zg.qq.client.friends_frame import FriendsFrame

class LoginFrame(MyFrame):
    def __init__(self):
        super().__init__(title='QQ登录',size=(340,255))

        # 创建顶部图片
        topimage=wx.Image('resouce/images/QQ11.jpg',wx.BITMAP_TYPE_JPEG)

        # 百度上这种很煞笔的方法来更改image的宽高
        #topimage = wx.ImageFromBitmap(topimage)
        topimage=topimage.Scale(340,50,wx.IMAGE_QUALITY_HIGH)
        topimage = wx.BitmapFromImage(topimage)

        topimage_sb=wx.StaticBitmap(self.contentpanel,bitmap=topimage)

        # 创建界面控件
        middlepanel=wx.Panel(self.contentpanel,style=wx.BORDER_DOUBLE)
        accountid_st = wx.StaticText(middlepanel,label='QQ号码')
        password_st = wx.StaticText(middlepanel,label='QQ密码')
        self.account_id_txt = wx.TextCtrl(middlepanel)
        self.password_txt = wx.TextCtrl(middlepanel, style=wx.TE_PASSWORD)
        st = wx.StaticText(middlepanel,label='忘记密码？')
        st.SetForegroundColour(wx.BLUE)

        # 创建FlexGrid布局fgs对象
        fgs = wx.FlexGridSizer(3, 3, 8, 15)
        fgs.AddMany([(accountid_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
                     (self.account_id_txt, 1, wx.CENTER | wx.EXPAND),
                     wx.StaticText(middlepanel),
                     (password_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
                     (self.password_txt, 1, wx.CENTER | wx.EXPAND),
                     (st,1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
                     wx.StaticText(middlepanel),
                     (wx.CheckBox(middlepanel, - 1, '自动登录'), 1, wx.CENTER | wx.EXPAND),
                     (wx.CheckBox(middlepanel, - 1, '隐身登录'), 1, wx.CENTER | wx.EXPAND)])

        # 设置flexGrid布局对象
        fgs.AddGrowableRow(0, 1)
        fgs.AddGrowableRow(1, 1)
        fgs.AddGrowableCol(0, 1)
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableCol(2, 1)
        panelbox = wx.BoxSizer()
        panelbox.Add(fgs, -1, wx.CENTER | wx.ALL | wx.EXPAND, border = 10)
        middlepanel.SetSizer(panelbox)

        # 创建按钮对象
        okb_btn = wx.Button(parent=self.contentpanel, label='登录')
        self.Bind(wx.EVT_BUTTON, self.okb_btn_onclick, okb_btn)
        cancel_btn = wx.Button(parent=self.contentpanel, label='取消')
        self.Bind(wx.EVT_BUTTON, self.cancel_btn_onclick, cancel_btn)

        # 创建水平BOX布局hbox对象
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(parent=self.contentpanel, label='申请号码↓'),
                 1, wx.CENTER | wx.ALL | wx.EXPAND, border = 10)
        hbox.Add(okb_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border = 10)
        hbox.Add(cancel_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border = 10)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topimage_sb, - 1, wx.CENTER | wx.EXPAND)
        vbox.Add(middlepanel, -1, wx.CENTER | wx.ALL |wx.EXPAND, border = 5)
        vbox.Add(hbox, -1, wx.CENTER | wx.BOTTOM, border = 1)
        self.contentpanel.SetSizer(vbox)

    def okb_btn_onclick(self,event):
        account = self.account_id_txt.GetValue()
        password = self.password_txt.GetValue()
        user = self.login(account, password)

        if user is not None:
            logger.info('登录成功.')
            next_frame=FriendsFrame(user)
            next_frame.Show()
            self.Hide()
        else:
            logger.info('登录失败。')
            dlg=wx.MessageDialog(self,'您QQ号码不正确','登录失败',wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def cancel_btn_onclick(self, event):
        # 退出系统
        self.Destroy()
        sys.exit(0)

    def login(self,userid,password):
        """"客户端向服务器发送登录请求"""
        json_obj=dict()
        json_obj['command']=COMMAD_LOGIN
        json_obj['user_id']=userid
        json_obj['user_pwd']=password

        # json编码
        json_str=json.dumps(json_obj)  # 将json对象编码为json字符串
        logger.info(json_str)
        # 给服务器端发送数据，哪个程序绑定了这个地址就发到哪里
        client_socket.sendto(json_str.encode(),server_address)

        # 从服务器端接受数据,阻止程序的继续进行
        json_data,_=client_socket.recvfrom(1024)  # 服务器返回json数据
        # json解码
        json_obj=json.loads(json_data.decode())
        logger.info('从服务器端接收数据：'.format(json_obj))

        if json_obj['result']=='0':
            # 登录成功
            print(json_obj)
            return json_obj