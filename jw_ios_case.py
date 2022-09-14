#-*- coding:utf-8 -*-
from time import sleep

import ele as ele
import wda
import os
import re
from PIL import Image,ImageStat
import math
import operator
from functools import reduce
import threading
import configparser
#import cv2

#cfgpath = "ios_dbconf.ini"
#config = configparser.ConfigParser()
#config.read(cfgpath, encoding="gb2312")
#phone_num = config.get('sec1', '手机登录的号码')
#phone_pwd = config.get('sec1', '手机登录的密码')
wda.DEBUG = True
class JiWei:
    @classmethod
    def jwt_01(cls, c, video_camera_name):  # 周云婷手机登录
        #with c.alert.watch_and_click(['提示', '取消']):
             #c(name="取消").click()
        c.session('com.co.Yoosee')#打开app
        c(type='XCUIElementTypeTextField').clear_text() #清除当前账号
        c(type='XCUIElementTypeTextField').set_text("13016129715") #输入手机号
        c(type='XCUIElementTypeSecureTextField').set_text("qwe12345")# 输入正确密码
        c(name="登录").click()
        c(name="同意并继续").click()
        c(name="以后").click()
        if c(type='XCUIElementTypeStaticText'):#如果有添加设备按钮则退出登录
            c(name="我的").click()
            c(type="XCUIElementTypeStaticText").click()
            c(name="退出登录").click()
        return False
        sleep(5)
        c.session().app_terminate('com.co.Yoosee')  # 关闭app

    @classmethod
    def jwt_14(cls, c, video_camera_name):#周云婷手机登录
        c.session('com.co.Yoosee')
        c(name="微信").click()
        c(name="同意并继续").click()
        c(name="更多选项").click()
        c(name="登录其他帐号").click()
        sleep(5)
        c.session().app_terminate('com.co.Yoosee')  # 关闭app



















        # a = c.app_current()
        # #print (a)
        # #print(c.alert.exists)
        # if c.alert.watch_and_click(['提示', '取消']):
        # #with c.alert.watch_and_click(['提示', '取消']):
        #      c(name="取消").click()
        # #c.screenshot('screen.png')
        # #c(name="取").click()
        # # u.app_clear('com.yoosee')  # 清除应用数据
        # # # u.watcher.stop()
        # # SameOperation().app_go(u)
        # # if u(text='用户服务协议和隐私政策概要').exists:
        # #     u(resourceId='com.yoosee:id/tv_no').click(timeout=5)
        # #     sleep(3)
        # #     assert not u(text='登录').exists, '未进入登录界面'
        # # else:
        # #     assert u(text='用户服务协议和隐私政策概要').exists, '用户服务协议弹窗不存在'