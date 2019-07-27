# -*- coding:utf-8 -*-
# @Time    :2019/7/22 9:12
# @Author  :曾格

import socket
import logging
import json
from com.zg.qq.server.user_dao import UserDao
# 服务器端IP
SERVER_IP='127.0.0.1'
# 服务器端口号
SERVER_PORT=8888
# 操作命令
COMMAND_LOGIN = 1        # 登录命令
COMMAND_LOGOUT = 2       # 下线命令
COMMAND_SENDMSG = 3      # 发消息命令
COMMAND_REFRESH = 4      # 刷新好友列表命令

# 所有已经登录的客户端信息=》相当于session
clientlist=[]
server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP,SERVER_PORT))

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s % (filename)s [line:%(lineno)d] %(levelname)s % (message)s')
                    # datefmt='%a,%d %b %Y %H:%M:%S',
                    # filename='qq_server.log',
                    # filemode='w')

logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(threadName)s'
                    '%(name)s-%(funcName)s-%(levelname)s-%(message)s')
logger=logging.getLogger(__name__)

logger.info('服务器启动，监听自己的端口{0}...'.format(SERVER_PORT))    # 有时不会输出

# 创建字节序列对象，作为接收数据的缓冲区
buffer=[]
# 主循环
while True:
    # TODO 服务端处理
    try:
        # 接收数据包
        data,client_address=server_socket.recvfrom(1024)
        json_obj=json.loads(data.decode())
        logger.info('服务端接收客户端，消息:{0}'.format(json_obj))

        # 取出客户端传递过来的操作命令
        command=json_obj['command']
        if command==COMMAND_LOGIN:
            # 通过id查询用户信息
            userid=json_obj['user_id']
            userpwd=json_obj['user_pwd']
            logger.debug('user_id:{0} user_pwd:{1}'.format(userid,userpwd))
            dao=UserDao()
            user=dao.findbyid(userid)
            logger.info(user)    # 还可以这样的哦！

            # 判断客户端发送过来的密码与数据库密码是否一致
            if user is not None and user['user_pwd']== userpwd:  # 登录成功
                # 登录成功
                # 1，创建保存用户登录信息的二元组=》退出即注销的session
                clientinfo=(userid,client_address)  # ip和端口吗
                # 用户登录信息添加到clientlist
                clientlist.append(clientinfo)

                json_obj=user
                json_obj['result']='0'

                # 取出好友列表  =》 拿来操作
                dao=UserDao()
                friends=dao.findfriends(userid)
                # 返回clientinfo中userid列表  =》登录中的所有用户id
                cinfo_userids=list(map(lambda it:it[0],clientlist))
                print(list(cinfo_userids))

                for friend in friends:
                    fid=friend['user_id']
                    # 添加好友状态，‘1’在线，‘0’离线
                    friend['online']='0'
                    if str(fid) in cinfo_userids:   # 用户登录
                        friend['online']='1'

                # 把好友列表发送到客户端
                json_obj['friends']=friends
                logger.info('服务器端发送用户成功,消息：{0}'.format(json_obj))

                # json编码
                json_str=json.dumps(json_obj)
                # 给客户端发送数据=>通过sendto实现两台主机的交互，此时根据主机和端口怎么定位到文件呢？还是定位到程序？
                server_socket.sendto(json_str.encode(),client_address)

            else:    # 登录失败
                json_obj={}
                json_obj['result']='-1'
                # json编码
                json_str=json.dumps(json_obj)
                # 给客户端发送数据
                server_socket.sendto(json_str.encode(),client_address)
        elif command==COMMAND_SENDMSG:       # 用户发送消息
            # TODO 用户发送消息
            # 获得好友id
            fduserid=json_obj['receive_user_id']
            # 向客户端发送数据
            # 在clientlist中查找好友id
            filter_clientinfo=filter(lambda it:it[0]==str(fduserid),clientlist)
            clientinfo=list(filter_clientinfo)

            if len(clientinfo)==1:        # 为毛长度是1？clientinfo是个二维元组？是的
                logger.info("目标主机的信息：{0}".format(clientinfo))
                _,client_address=clientinfo[0]
                # 服务器端转发消息给客户端
                # JSON编码
                json_str=json.dumps(json_obj)
                server_socket.sendto(json_str.encode(),client_address)
            else:
                logger.info("clientlist中此好友id数:{0}".format(len(clientinfo)))

        elif command==COMMAND_LOGOUT:        # 用户下线命令
            # TODO 用户发送消息
            # 获得用户id
            userid=json_obj['user_id']
            for clientinfo in clientlist:
                cuserid , _= clientinfo
                if cuserid==userid:
                    clientlist.remove(clientinfo)
                    break
            logger.info(clientlist)

        # TODO 刷新用户列表
        # 如果clientlist中没有元素则跳到下次循环=>?跳出后，等待下一个数据包
        if len(clientlist)==0:
            continue
        json_obj=dict()
        json_obj['command']=COMMAND_REFRESH
        usersid_map=map(lambda it:it[0],clientlist)
        useridlist=list(usersid_map)
        json_obj['OnlineUserList']=useridlist

        for clientinfo in clientlist:
            _,address=clientinfo
            # json编码
            json_str=json.dumps(json_obj)
            # 给客户端发送数据
            server_socket.sendto(json_str.encode(),address)
    except Exception:
        import traceback as tb
        tb.print_exc()
        logger.info('timed outs')





