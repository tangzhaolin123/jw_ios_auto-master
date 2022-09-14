#coding:utf-8
from time import sleep
import traceback
import random
import configparser
from jw_ios_case import JiWei
#from jw_case import SameOperation
from datetime import datetime
from datetime import timedelta
import re
import os
import json
import requests
import xlrd
import configparser
from PIL import Image
import multiprocessing
from pathlib import Path
import wda

def message(content):
	try:
		data = {
		"msgtype":"text",
		"text":{
			"content":"测试："+content
		}
		}
		headers1 = {
			"Content-Type": "application/json;charset=UTF-8"
		}
		data = json.dumps(data, ensure_ascii=False)
		data = data.encode(encoding="utf-8")
		r = requests.post(url=URL, data=data,headers=headers1,timeout=3)
		r = json.loads(r.text)
		return r
	except:
		pass

def dingtalk_robot(total,pass_total,fial_total,report_url):
    headers = {'Content-Type':'application/json'}

    data_dict = {
        "msgtype":"markdown",

        "markdown":{
            "title":"测试报告",
           "text":"#### 测试报告 \n\n"
				  "![report](https://p0.itc.cn/images01/20220617/8863a4f8f774447e9f7b076c6524158d.jpeg)"
                  "> **用例总数:** **"+str(total)+"**\n\n"
                  "> **PASS:** **<font color=#7CFCOO>"+str(pass_total)+"</font>**\n\n"
                  "> **FAIL:** **<font color=#FF0000>"+str(fial_total)+"</font>**\n\n"
				  "[查看详情]"+report_url
        }
    }

    json_data =json.dumps(data_dict)
    for r_i in range(0,3):
        response = requests.post(URL, data = json_data,headers = headers,timeout=5)
        print ('发送报告',r_i)
        if response.status_code == requests.codes.ok:
           break

class DingMessage:
	def __init__(self):
		# self.URL = "https://oapi.dingtalk.com/robot/send?access_token=c553bbae288a266b5d2d4a382a41b54f332cdab43c1e6a94cff949766c5e05f6"  # Webhook地址
		self.URL = URL
		self.headers = {'Content-Type':'application/json'}
	def dingtalk_testexception(self,case_code,case_name,premise_conditions,case_steps,expected_result,result_url,app_version):
		if "重新" in case_code:
			data_dict = {
				"msgtype": "markdown",

				"markdown": {
					"title": "异常重新测试提示",
					"text": "#### **<font color=#9ACD32>" + case_code + "测试通过**</font>\n\n"
					"> **用例名称:** <font color=#000000>" + case_name + "</font>\n\n"
					"> **前置条件:** <font color=#000000>" + premise_conditions + "</font>\n\n"
					"> **操作步骤:** <font color=#000000>" + case_steps + "</font>\n\n"
					"> **预期结果:** <font color=#000000>" + expected_result + "</font>\n\n"
					"> **APK版本:** <font color=#000000>" + app_version + "</font>\n\n"
				}
			}
		elif "重执行2次" in case_code:
			data_dict = {
				"msgtype": "markdown",

				"markdown": {
					"title": "测试异常提示",
					"text": "#### **<font color=#FF0000>" + case_code + "测试异常**</font>\n\n"
																		"> **用例名称:** <font color=#000000>" + case_name + "</font>\n\n"
																														 "> **前置条件:** <font color=#000000>" + premise_conditions + "</font>\n\n"
																																												   "> **操作步骤:** <font color=#000000>" + case_steps + "</font>\n\n"
																																																									 "> **预期结果:** <font color=#000000>" + expected_result + "</font>\n\n"
																																																																							"> **APK版本:** <font color=#000000>" + app_version + "</font>\n\n"
																																																																																				"[查看报错时图片](" + result_url + ')'
				}
			}

		else:
			data_dict = {
				"msgtype":"markdown",

				"markdown":{
					"title":"测试异常提示",
				   "text":"#### **<font color=#FF0000>"+case_code+"测试异常**</font>\n\n"
						  "> **用例名称:** <font color=#000000>"+case_name+"</font>\n\n"                        
						  "> **前置条件:** <font color=#000000>"+premise_conditions+"</font>\n\n"                        
						  "> **操作步骤:** <font color=#000000>"+case_steps+"</font>\n\n"
						  "> **预期结果:** <font color=#000000>"+expected_result+"</font>\n\n"
						  "> **APK版本:** <font color=#000000>" + app_version + "</font>\n\n"
						  "[查看报错时截图](" + result_url + ')'
				}
			}

		json_data =json.dumps(data_dict)
		response = requests.post(self.URL, data = json_data,headers = self.headers,timeout=6)

	def dingtalk_testpass(self,case_code,case_name,premise_conditions,case_steps,expected_result,app_version):
		data_dict = {
			"msgtype": "markdown",

			"markdown": {
				"title": "测试通过提示",
				"text": "#### **<font color=#9ACD32>" + case_code + "测试通过**</font>\n\n"
				"> **用例名称:** <font color=#000000>" + case_name + "</font>\n\n"
				"> **前置条件:** <font color=#000000>" + premise_conditions + "</font>\n\n"
				"> **操作步骤:** <font color=#000000>" + case_steps + "</font>\n\n"
				"> **预期结果:** <font color=#000000>" + expected_result + "</font>\n\n"
				"> **APK版本:** <font color=#000000>" + app_version + "</font>\n\n"
			}
		}
		json_data =json.dumps(data_dict)
		#response = requests.post(self.URL, data = json_data,headers = self.headers,timeout=6)
		for r_i in range(0, 3):
			response = requests.post(self.URL, data = json_data,headers = self.headers,timeout=6)
			#print('发送报告', r_i)
			if response.status_code == requests.codes.ok:
				#print (response.status_code,requests.codes.ok)
				break


	def dingtalk_robot(self,total,pass_total,fial_total,report_url):
		data_dict = {
			"msgtype":"markdown",

			"markdown":{
				"title":"测试报告",
			   "text":"#### 测试报告 \n\n"
					  "![report](http://tangjw.xyz/test_report.png)"
					  "> **用例总数:** **"+str(total)+"**\n\n"
					  "> **PASS:** **<font color=#7CFCOO>"+str(pass_total)+"</font>**\n\n"
					  "> **FAIL:** **<font color=#FF0000>"+str(fial_total)+"</font>**\n\n"
					  "[查看详情]"+report_url
			}
		}

		json_data =json.dumps(data_dict)

		# response = requests.post(self.URL, data = json_data,headers = self.headers,timeout=6)
		for r_i in range(0, 3):
			response = requests.post(self.URL, data = json_data,headers = self.headers,timeout=6)
			#print('发送报告', r_i)
			if response.status_code == requests.codes.ok:
				#print (response.status_code,requests.codes.ok)
				break
# access_key = 'gMQ_x2DD6xcBsHf7Bwn4iRGFLwLilsmiW5DG3RsI'
# secret_key = 'CAvmXjwUEZm8d8h_gStjOLKqy9ssx6mSHtlcFsdf'


from urllib.parse import urljoin
space2url ={
    "jwtime1":"http://tangjw.xyz",
    "x":"123"
}
def up2qiniu(local_img,space_name,img_name):
    """
    本图图片的上传
    :param local_img: 本地图片路径
    :param space_name: 云服务器的空间名称
    :param img_name: 上传后的网络上保存的图片名称
    :return img_url: 远程图片的路径(绝对路径)
    """

    from qiniu import Auth, put_file, etag
    import qiniu.config

    access_key = 'YX6Pck4xl_IXjhy9Oay7SsTB_d_XXyCrGlnnvTX7'
    secret_key = 'DQNnoew9MuGzXV3s6BL5B5BD711IQHcEQwhtnMww'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'jwtime1'

    # 上传后保存的文件名
    key = img_name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = r'D:\jw8'

    ret, info = put_file(token, key, local_img)
    img_url = urljoin(space2url[space_name], img_name)
    return img_url
# res = up2qiniu(r'c.png', "jwtime1","c.png")

class Template_mixin(object):
    """html报告"""
    HTML_TMPL = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>自动化测试报告</title>
            <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
            <h1 style="font-family: Microsoft YaHei">自动化测试报告</h1>
            <p class='attribute'><strong>测试人员 : </strong> 钉钉机器人</p>
            <p class='attribute'><strong>开始时间 : </strong> %(startTime)s</p>
            <p class='attribute'><strong>合计耗时 : </strong> %(totalTime)s</p>
            <p class='attribute'><strong>测试结果 : </strong> %(value)s</p>
            <p class='attribute'><strong>APK版本 : </strong> %(appVersion)s</p>
            <style type="text/css" media="screen">
        body  { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px;}
        </style>
        </head>
        <body>
            <table id='result_table' class="table table-condensed table-bordered table-hover">
                <colgroup>
                    <col align='left' />
                    <col align='right' />
                    <col align='right' />
                    <col align='right' />
                </colgroup>
                <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
                    <th>用例编号</th>
                    <th>模块</th>
                    <th>用例名称</th>
                    <th>前置条件</th>
                    <th>测试步骤</th>
                    <th>预期结果</th>
                    <th>用例执行结果</th>
                    <th>失败原因</th>
                    <th>备注</th>
                </tr>
                %(table_tr)s
            </table>
            %(caseList)s
            %(robotlog)s
        </body>
        </html>"""

    TABLE_TMPL = """
        <tr class='failClass warning'>
            <td>%(step)s</td>
            <td>%(case_module)s</td>
            <td>%(case_name)s</td>
            <td>%(case_antecedents)s</td>
            <td>%(case_testProcedure)s</td>
            <td>%(case_expectedResult)s</td>
            <td>%(runresult)s</td>
            <td>%(reason)s</td>
            <td>%(case_notes)s</td>
        </tr>"""

def app_excel_field(case_code):
    # app_xlsfile = os.getcwd() + '\\app_auto_case.xlsx'  # 打开指定路径中的xls文件
	app_xlsfile = 'app_auto_case.xlsx'
	app_book = xlrd.open_workbook(app_xlsfile)
	app_sheet0 = app_book.sheet_by_index(1)
	app_row_n = app_sheet0.nrows - 1
	for row_i in range(0,app_row_n):
		if case_code == app_sheet0.col_values(0, start_rowx=0, end_rowx=None)[row_i]:
			return app_sheet0.row_values(row_i, start_colx=0, end_colx=7)

class CaseExcel:
    def __init__(self):
        self.app_xlsfile = 'app_auto_case.xlsx'
        self.app_book = xlrd.open_workbook(self.app_xlsfile)#打开文件
        self.app_sheet0 = self.app_book.sheet_by_index(1)#通过索引顺序获取
        self.app_row_n = self.app_sheet0.nrows - 1

    def app_excel_field(self,case_code):
        for row_i in range(0,self.app_row_n):
            if case_code == self.app_sheet0.col_values(0, start_rowx=0, end_rowx=None)[row_i]:#返回由该列中所有单元格的数据组成的列表
                return self.app_sheet0.row_values(row_i, start_colx=0, end_colx=6)#返回由该行中所有单元格的数据组成的列表

    def auto_caselist(self):
        CodeList = self.app_sheet0.col_values(0, start_rowx=1, end_rowx=None)#返回由该列中所有单元格的数据组成的列表
        whether = self.app_sheet0.col_values(6, start_rowx=1, end_rowx=None)#返回由该列中所有单元格的数据组成的列表
        # print (CodeList,"\n",whether)
        autocase_codelist = []
        for list_code in range(0,len(CodeList)):
            CodeList[list_code].replace('jwt_', '')
            if whether[list_code].strip() == 'NA' or whether[list_code].strip() == 'NT':#不要NA用例、NT用例
                autocase_codelist.append(CodeList[list_code])
        # print(CodeList)
        executed_case = [item for item in CodeList if item not in set(autocase_codelist)]
        return executed_case
    def app_case_name(self,case_code):
        CodeList1 = self.app_sheet0.col_values(0, start_rowx=1, end_rowx=None)#返回由该列中所有单元格的数据组成的列表

        CodeList2 = self.app_sheet0.col_values(2, start_rowx=1, end_rowx=None)  # 返回由该列中所有单元格的数据组成的列表
        autocase_casename = []
        # print (CodeList1,'\n',CodeList2)
        match_name =  dict(zip(CodeList1, CodeList2))
        return match_name[case_code]
#auto upgrade version
class AutoUpgrade:
    def app_id(self):
        URL = "http://www.pgyer.com/apiv1/app/getAppKeyByShortcut"
        headers = {'Content-Type':'application/json'}

        data = {
            "shortcut": (None, "ptY3"),
            "_api_key": (None, "cbe11636fc4031641cccbcb648227d6c")
        }
        response = requests.request("POST", URL, files=data)
        jdata = json.loads(response.text)
        # print(type(jdata),jdata)
        return jdata['data']['appKey']

    def down_app(self):
        data_dict = {
            "aKey": AutoUpgrade.app_id(self),
            "_api_key": 'cbe11636fc4031641cccbcb648227d6c'
        }
        install_url = 'http://www.pgyer.com/apiv1/app/install?aKey=%s&_api_key=%s' % (
        data_dict['aKey'], data_dict['_api_key'])
        # print(install_url)
        url = install_url
        r = requests.get(url, stream=True)
        f = open("1.apk", "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        f.close()

class AppLog:
	def __init__(self):
		self.a = '/sdcard/Android/data/com.yoosee/files/Log/'
		self.b = '/sdcard/Android/data/com.yoosee/files/Documents/'
		self.c = '/sdcard/Android/data/com.yoosee/files/Documents/errorLog/'

	def log_sum(self,file):
		try:
			list_a = os.listdir(self.a)
			for i in range(0,len(list_a)):
				if '.log' in list_a[i]:
					# print (list_a[i])
					# 打开文件
					log_a = self.a+list_a[i]
			# 		fo_a = open(log_a, "r", encoding="utf-8")
			# # print("文件名为: ", fo.name)
			# 		line_a = fo_a.read()
			#
			# 		# file = "1.log"
			# 		with open(file, 'a') as f:
			# 			f.write(line_a)

					with open(log_a, 'r', encoding='utf-8') as f:
						fo_a = reversed(f.readlines())
						fi = 0
						for line in fo_a:
							# print(line.strip())
							with open(file, 'a') as f:
								f.write(line.strip() + '\n')
							fi = fi + 1
							if fi == 200:
								break
					# fo_a.close()
					os.remove(log_a)
		except:
			pass
				# Documents文件下的
		try:
			list_b = os.listdir(self.b)
			for i in range(0, len(list_b)):
				if '.log' in list_b[i]:
					# print(list_b[i])
					# 打开文件
					log_b = self.b + list_b[i]
					fo_b = open(log_b, "r", encoding="utf-8")
					# print("文件名为: ", fo.name)
					line_b = fo_b.read()

					# file = "1.log"
					with open(file, 'a') as f:
						f.write(line_b)
					fo_b.close()
					os.remove(log_b)
		except:
			pass
		try:
			list_c = os.listdir(self.c)
			for i in range(0, len(list_c)):
				if '.log' in list_c[i]:
					# print(list_c[i])
					# 打开文件
					log_c = self.c + list_c[i]
					fo_c = open(log_c, "r", encoding="utf-8")
					# print("文件名为: ", fo.name)
					line_c = fo_c.read()

					# file = "1.log"
					with open(file, 'a') as f:
						f.write(line_c)
					fo_c.close()
					os.remove(log_c)
			# with open(file, 'r', encoding='utf-8') as f:
			# 	a = reversed(f.readlines())
			# 	i = 0
			# 	for line in a:
			# 		print(line.strip())
			# 		with open('log_new.log', 'a') as f:
			# 			f.write(line.strip() + '\n')
			# 		i = i + 1
			# 		if i == 500:
			# 			break
		except:
			pass

class SanAppLog:
	def __init__(self):
		self.a_1 = '/sdcard/Android/data/com.yoosee/files/Log/'
		self.a_2 = '/sdcard/Android/data/com.yoosee/files/Documents/'
		self.a_3 = '/sdcard/Android/data/com.yoosee/files/Documents/errorLog/'
		self.b_1 = '/sdcard/Android/data/com.yoosee/files/Log/.'
		self.b_2 = '/sdcard/Android/data/com.yoosee/files/Documents/.'
		self.b_3 = '/sdcard/Android/data/com.yoosee/files/Documents/errorLog/.'

	def sanxing_log(self, u, file):
		for i in range(1, 4):
			log_name = 'name_list.txt'
			list_1 = 'self.b_' + str(i)
			u.pull(eval(list_1), log_name)

			with open(log_name, 'r') as f:
				a = f.read()
			# print(a)

			b = re.findall('<a href="(.*)">', a)
			# print(b)  # [('life is short, i use python', 'i love it')]
			list = []
			for j in range(0, len(b)):
				if '.log' in b[j]:
					# list.append(b[i])
					# print (list)
					list_2 = 'self.a_' + str(i)
					u.pull(eval(list_2) + b[j], str(j) + '.log')
					with open(str(j) + '.log', 'r') as f:
						a_1 = f.read()
					with open(file, 'a') as f:
						f.write(a_1)

					if list_2 == 'self.a_1':
						with open(str(j) + '.log', 'r', encoding='utf-8') as f:
							fo_a = reversed(f.readlines())
							fi = 0
							for line in fo_a:
								# print(line.strip())
								with open(file, 'a') as f:
									f.write(line.strip() + '\n')
								fi = fi + 1
								if fi == 200:
									break
					else:
						with open(str(j) + '.log', 'r') as f:
							a_1 = f.read()
						with open(file, 'a') as f:
							f.write(a_1)

class ResizeImage:
	def resize_image(self,file, width, height, type):
		img = Image.open(file)
		#out = img.resize((width, height), Image.ANTIALIAS)  # resize image with high-quality
		out = img.resize((width, height), Image.Resampling.LANCZOS)
		out.save(file, type)

class FileUp:
    def find_queue(self,queue):
        file_list = os.listdir()
        #print(file_list)
        # file_list =['1234.txt', '2022-202.zip', '2022-203.zip']
        for file_name in file_list:
            if queue.full():
                print("队列已满!")
                break
            if 'jw2022-' in file_name:
                queue.put(file_name)
                print(file_name)
                sleep(0.5)

    def up_queue(self,queue):
        # 循环读取队列消息
        while True:
            # 队列为空，停止读取
            if queue.empty():
                print("---队列已空---")
                break

            # 读取消息并输出
            result = queue.get()
            print(result)
            res = up2qiniu(result, "jwtime1", result)
            sleep(5)
            r = requests.get(url=res)
            if r.status_code == 200:
                os.remove(result)

    def main(self):
        #while True:
            # 创建消息队列
        queue = multiprocessing.Queue(5)
        # 创建子进程
        p1 = multiprocessing.Process(target=self.find_queue, args=(queue,))
        p1.start()
        # 等待p1写数据进程执行结束后，再往下执行
        p1.join()
        p1 = multiprocessing.Process(target=self.up_queue, args=(queue,))
        p1.start()
        sleep(3)

if __name__ == '__main__':
	#配置文件读取参数
	cfgpath = "ios_dbconf.ini"
	config = configparser.ConfigParser()
	config.read(cfgpath, encoding="gb2312")
	video_camera_name = config.get('sec1', '摄像头设备ID')
	URL = config.get('sec1', '钉钉消息Webhook地址')
	devices_name = config.get('sec1', '手机设备名')
	rounds = config.get('sec2', '用例执行轮次')
	phone_num = config.get('sec1', '手机登录的号码')
	phone_pwd = config.get('sec1', '手机登录的密码')
	erro_notifi = config.get('sec2', '异常报错通知')
	pass_notifi = config.get('sec2', '测试通过通知')
	pass_report = config.get('sec2', '通过的用例在报告中展示')
	print ('video',video_camera_name)
	#rounds = '1'
	c = wda.Client()
	c.wait_ready(timeout=300)
	c.implicitly_wait(30.0)
	i = 0
	app_version = '1.1.0'
	while i<int(rounds):
		is_execute = []
		# old_appid = config.get('sec1', 'APP的id')
		#new_appid = AutoUpgrade().app_id()
		i=i+1
		print(('Testing time: %d') % (i))
		# Caselist = [30,31,32,33]
		# Caselist = [36,37]
		Caselist = config.get('sec2', '执行的用例').split(",")

		case_len = len(Caselist)
		count_success = 0
		fail_caselog = []
		robot_loglist = []
		case_number = []
		pass_number = []
		start_time = datetime.now()
		# u.watcher.stop()
		for l0 in range(1, len(Caselist) + 1):
			# 监控弹框
			# u.watcher.when("同意").click()
			# u.watcher.when("允许").click()
			# u.watcher.when("仅在前台使用应用时允许").click()
			# u.watcher.when("仅在使用该应用时允许").click()
			# u.watcher.when("仅在使用中允许").click()
			# u.watcher.when("双指可放大画面").click()
			# u.watcher.when("可以尝试上下左右拖动画面").click()
			# u.watcher.when("深入了解").click()
			# u.watcher.when("消息通知说明").press("back")
			# u.watcher.when("close").click()
			# u.watcher.when('继续安装').click()
			# u.watcher.when('不再提醒').click()
			# u.watcher.when('下次再说').click()
			# u.watcher.when("您将不再接收此设备的报警推送").press("back")

			interval_time1 = datetime.now()
			a0 = int(Caselist[l0 - 1])
			is_execute.append(Caselist[l0 - 1])
			#print(a, len(list1))
			w_report = ''
			robot_log_w = ''
			#termux后台运行
			# u.app_start('com.termux')
			# sleep(1)
			# u.press("home")
			# sleep(1)
			# print (a0)
			#监视器控制
			# if a0 == 1 or a0 == 2:
			# 	# 停止所有监视
			# 	u.watcher.stop()
			# elif a0 == 3:
			# 	u.watcher.when("我知道了").click()
			# 	u.watcher.when("忽略").click()
			# 	u.watcher.start()
			# elif a0 == 79 or a0 == 80 or a0 == 81 or a0 == 82 or a0 == 83 or a0 == 84 or a0 == 85 or a0 == 86:
			# 	u.watcher.start()
			# elif a0 ==95 or a0 ==96 or a0 ==97 or a0 ==98 or a0 ==99 or a0 ==100:
			# 	u.watcher.when("我知道了").click()
			# 	u.watcher.when("发现新固件").press("back")
			# 	u.watcher.start()
			# else:
			# 	u.watcher.when("取消推送").press("back")
			# 	u.watcher.when("我知道了").click()
			# 	u.watcher.when("发现新固件").press("back")
			# 	u.watcher.start()

			try:
				if a0 < 10:
					u0 = "JiWei.jwt_0" + str(a0)
					print(u0)
					eval(u0)(c,video_camera_name)
				else:
					u0 = "JiWei.jwt_" + str(a0)
					print(u0)
					eval(u0)(c,video_camera_name)
				# u.app_start('com.termux')
				# u.press("home")
				count_success = count_success + 1
			except Exception as err:
				# print ('出错',err)
				# a1 = traceback.format_exc()
				# print(a1)
				# message(a1)
				# dt1 = datetime.now()
				# dt2 = dt1.strftime('%Y-%m-%d %H.%M.%S')
				#截图
				try:
					dt1 = datetime.now()
					dt2 = dt1.strftime('%Y-%m-%d_%H.%M.%S')
					image = 'jw'+dt2 + ".png"
					#u.screenshot(image)
					c.screenshot().save(image)

					#修改大小
					ResizeImage().resize_image(image,216,492,'png')
					#上传
					res = up2qiniu(image, "jwtime1", image)
					# os.remove(image)
					#上传是否成功
					sleep(2)
					upload_or_not = requests.get(url=res)
					if upload_or_not.status_code == 200:
						os.remove(image)
				except:
					res = space2url['jwtime1']+'/'+image
					print ("截图获取失败")
					# app log获取
					# log_path = '/sdcard/Android/data/com.yoosee/files/Log/gw_sdk_ad_1.log'
				# try:
				# 	log_file ='jw'+ dt2 + ".log"
				# 	# u.pull(log_path, log_file)
				# 	if devices_brand == 'vivo' or devices_brand == 'OPPO':
				# 		AppLog().log_sum(log_file)
				# 	else:
				# 		SanAppLog().sanxing_log(u, log_file)
				# 	log_res = up2qiniu(log_file, "jwtime1", log_file)
				# 	# print (log_res)
				# 	try:
				# 		# os.remove(log_file)
				# 		sleep(2)
				# 		upload_or_not = requests.get(url=log_res)
				# 		if upload_or_not.status_code == 200:
				# 			os.remove(log_file)
				#
				# 	except:
				# 		pass
				# except:
				# 	print ("log获取失败")
				# 	log_res = space2url['jwtime1']+'/'+log_file
				#本次不算，重新开始
				# if l0 == 1:
				# 	i=i - 1
				# 	break

				# image = os.getcwd() + "\\" + dt2 + ".png"
				# d.screenshot(image)

				a1 = traceback.format_exc()
				print(a1)
				# if a1.find("AssertionError") >= 0:
				# 	pos1 = a1.find('AssertionError')
				# # print (pos1)
				# 	pos3 = a1[pos1 + 15:(pos1 + 40)]
				# else:
				pos1 = a1.find('in jwt')
				pos2 = a1.find('\n',pos1+10)
				pos_1 = a1[pos1-23:pos2]
				pos3 = re.sub('\n', "", pos_1)
				w_report += '<a href=' + res + '>image </a>' #+ '<a href=' + log_res + '> LOG</a>' + '<br />'# '<a href='+res+'>图片</a>'
				robot_log_w += dt2 + u0 + pos3 + '\n'
				case_testexceptioninformation = app_excel_field(u0.replace('JiWei.', ''))

				try:
					if erro_notifi == '是':
						interval_time2 = datetime.now()
						if interval_time2 - interval_time1 > timedelta(seconds=20):
							#message(w)
							DingMessage().dingtalk_testexception(case_testexceptioninformation[0],case_testexceptioninformation[2],case_testexceptioninformation[3],case_testexceptioninformation[4],case_testexceptioninformation[5],res,app_version)
				except:
					pass
				#SameOperation().quit_app(u)
				#是否因为锁屏而报错
				# if u.info.get("screenOn") != True:
				# 	u.screen_off()
				# 	u.unlock()
				#重试
				for retry_n in range(1,3):
				#重试一次
					try:
						# if retry_n == 2:
						# 	# 开始录制视频
						# 	video_start_time = datetime.now()
						# 	video_name = video_start_time.strftime('%Y-%m-%d_%H.%M.%S')
						# 	video = 'jw' + video_name + ".mp4"
						# 	u.screenrecord(video)

						eval(u0)(c,video_camera_name)
						# message(u0+"重新执行"+str(retry_n)+"次OK")
						if erro_notifi == '是':
							DingMessage().dingtalk_testexception(case_testexceptioninformation[0]+"重新执行"+str(retry_n)+"次",case_testexceptioninformation[2],case_testexceptioninformation[3],case_testexceptioninformation[4],case_testexceptioninformation[5],res,app_version)

						count_success = count_success + 1
						# if retry_n == 2:
						# 	u.screenrecord.stop()
						# 	sleep(2)
						break
					except Exception as err:
						a1 = traceback.format_exc()
						print(a1)
						#截图
						try:
							# dt1 = datetime.now()
							# dt2 = dt1.strftime('%Y-%m-%d_%H.%M.%S')
							# image = dt2 + ".png"
							# u.screenshot(image)
							# # 修改大小
							# ResizeImage().resize_image(image, 216, 492, 'png')
							# # 上传
							# res = up2qiniu(image, "jwtime1", image)
							# # os.remove(image)
							# #是否上传成功，成功了删除
							# sleep(2)
							if retry_n == 2:
								# sleep(2)
								# u.screenrecord.stop()
								# sleep(3)
								# res = up2qiniu(video, "jwtime1", video)
								# sleep(6)
								#print (res)
								sleep(2)
							else:
								dt1 = datetime.now()
								dt2 = dt1.strftime('%Y-%m-%d_%H.%M.%S')
								image ='jw'+ dt2 + ".png"
								#u.screenshot(image)
								c.screenshot().save(image)
								# 修改大小
								ResizeImage().resize_image(image, 216, 492, 'png')
								# 上传
								res = up2qiniu(image, "jwtime1", image)
								# os.remove(image)
								#是否上传成功，成功了删除
								sleep(2)
								upload_or_not = requests.get(url=res)
								if upload_or_not.status_code == 200:
									os.remove(image)

							# upload_or_not = requests.get(url=res)
							# #print ('是否成功上传',upload_or_not.status_code)
							# if upload_or_not.status_code == 200:
							# 	if retry_n == 2:
							# 		os.remove(video)
							# 	else:
							# 		os.remove(image)
						except:
							# if retry_n == 2:
							# 	res = space2url['jwtime1'] + '/' + video
							# 	print("视频获取失败")
							# else:
							res = space2url['jwtime1']+'/'+image
							print("截图获取失败")
							# app log获取
							# log_path = '/sdcard/Android/data/com.yoosee/files/Log/gw_sdk_ad_1.log'
						# try:
						# 	log_file ='jw' + dt2 + ".log"
						# 	# u.pull(log_path, log_file)
						# 	if devices_brand == 'vivo' or devices_brand == 'OPPO':
						# 		AppLog().log_sum(log_file)
						# 	else:
						# 		SanAppLog().sanxing_log(u,log_file)
						# 	log_res = up2qiniu(log_file, "jwtime1", log_file)
						# 	# print (log_res)
						# 	try:
						# 		# os.remove(log_file)
						# 		# 是否上传成功，成功了删除
						# 		sleep(2)
						# 		upload_or_not = requests.get(url=log_res)
						# 		if upload_or_not.status_code == 200:
						# 			os.remove(log_file)
						# 	except:
						# 		pass
						# except:
						# 	print ("log获取失败")
						# 	log_res = space2url['jwtime1']+'/'+log_file
						#保存上传回放视频
						# if retry_n == 2:
						# 	try:
						# 		u.screenrecord.stop()
						# 		res = up2qiniu(video, "jwtime1", video)
						# 		# os.remove(video)
						# 	except:
						# 		res = ''
						# 		print("回放视频获取失败")

						pos1 = a1.find('in jwt')
						pos2 = a1.find('\n', pos1 + 10)
						pos_1 = a1[pos1 - 23:pos2]
						pos3 = re.sub('\n', "", pos_1)
						# w = u0+"重新执行"+str(retry_n)+"次仍报错"+pos3+'\n'+ res
						#w_report += u0+"重新执行"+str(retry_n)+"次仍报错"+pos3+'\n' +'<br />'+ '<a href='+res+'>查看报错图片</a>' +'<br />' #'<a href='+res+'>图片</a>'
						#if retry_n == 2:
							# w_report += '<a href=' + res + '>Retest' + str(
							# 	retry_n) + 'video </a>'
						# else:
						w_report += '<a href='+res+'>Retest'+str(retry_n)+'image </a>'  #+'<a href='+log_res+'> Retest'+str(retry_n)+'LOG</a>' +'<br />'#'<a href='+res+'>图片</a>'
						robot_log_w += dt2+u0+"重新执行"+str(retry_n)+"次仍报错"+pos3+'\n'
						# fail_caselog.append(w_report)
						# case_number.append(u0)
						#删除视频
						# if retry_n == 2 and res != '':
						# 	upload_or_not = requests.get(url=res)
						# 	if upload_or_not.status_code == 200:
						# 		os.remove(video)
						try:
							if erro_notifi == '是':
								interval_time3 = datetime.now()
								if interval_time3 - interval_time2 > timedelta(seconds=20):
									DingMessage().dingtalk_testexception(case_testexceptioninformation[0]+"重执行"+str(retry_n)+"次仍",
																		 case_testexceptioninformation[2],
																		 case_testexceptioninformation[3],
																		 case_testexceptioninformation[4],
																		 case_testexceptioninformation[5], res,app_version)
						except:
							pass

					if retry_n == 2:
						fail_caselog.append(w_report)
						case_number.append(u0)
						robot_loglist.append(robot_log_w)
					#SameOperation().quit_app(u)
				# if u.uiautomator.running() == False:
				# 	u.uiautomator.start()
			#关闭监视
			# u.watcher.stop()
			try:
				FileUp().main()
			except:
				pass
			#u.watcher.reset()
			# 通过通知
			if u0 not in case_number:
				pass_number.append(u0)
				case_testexceptioninformation = app_excel_field(u0.replace('JiWei.', ''))
				try:
					if pass_notifi == '是':
						DingMessage().dingtalk_testpass(case_testexceptioninformation[0],
														case_testexceptioninformation[2],
														case_testexceptioninformation[3],
														case_testexceptioninformation[4],
														case_testexceptioninformation[5], app_version)
				except:
					pass

			# 控制随时输出报告
			config.read(cfgpath, encoding="gb2312")
			do_not_run = config.get('sec1', '是否继续执行自动化')
			if do_not_run == '否':
				break
		# count_case_fail = case_len - count_success
		if do_not_run == '否':
			count_case_fail = len(is_execute) - count_success
			case_len = len(is_execute)
		else:
			count_case_fail = case_len - count_success
		#报告详情
		report_time = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
		report_file = report_time + ".html"
		total_time = datetime.now() - start_time

		#机器人日志
		dt3 = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
		robot_log_file = dt3 + ".txt"
		#for execute_i in range(0,len(is_execute)):
			#with open(robot_log_file, 'a') as f:
				#f.write(is_execute[execute_i]+'、  ')

		#robot_log = open(robot_log_file, 'a')
		#robot_loglist = '1234'
		if robot_loglist !=[]:
			for robot_i in range(0, len(robot_loglist)):
				with open(robot_log_file, 'a') as f:
					f.write('\n' + robot_loglist[robot_i] + '\n')
		# robot_log.flush()
		#robot_log.close()
		else:
			robot_loglist = '无日志'
			with open(robot_log_file, 'a') as f:
				f.write('\n' + robot_loglist + '\n')
		robot_log_singleurl =up2qiniu(robot_log_file, "jwtime1", robot_log_file)
		os.remove(robot_log_file)
		robot_log_url = '<a href='+robot_log_singleurl+'>查看机器人日志</a>'
		# print (robot_log_singleurl)

		#html报告
		table_tr0 = ''
		html = Template_mixin()
		for n in range(0,len(fail_caselog)):
			case_information = app_excel_field(case_number[n].replace('JiWei.', ''))
			#print (case_information )
			table_td = html.TABLE_TMPL % dict(
				step= case_information[0],
				case_module=case_information[1],
				case_name=case_information[2],
				case_antecedents=case_information[3],
				case_testProcedure=case_information[4],
				case_expectedResult=case_information[5],
				runresult='<font color="red">Fail</font>',
				reason=fail_caselog[n],
				case_notes=case_information[6],

			)
			table_tr0 += table_td
		if pass_report == '是':
			for n in range(0, len(pass_number)):
				case_information = app_excel_field(pass_number[n].replace('JiWei.', ''))
				# print (case_information )
				table_td = html.TABLE_TMPL % dict(
					step=case_information[0],
					case_module=case_information[1],
					case_name=case_information[2],
					case_antecedents=case_information[3],
					case_testProcedure=case_information[4],
					case_expectedResult=case_information[5],
					runresult='<font color="green">Pass</font>',
					reason='',
					case_notes=case_information[6],

				)
				table_tr0 += table_td
		case_url = '<a href=https://docs.qq.com/sheet/DTlZ5aEJEcUJwSVl6>查看测试用例</a>'
		total_str = '共 %s，通过 %s，失败 %s，通过率 %s' % (
		count_case_fail + count_success, count_success, count_case_fail, str(round(count_success / (count_case_fail + count_success),2) * 100) + '%')
		# start_time = '2022-04-30_15:15'
		# total_time = '00:01:05'
		output = html.HTML_TMPL % dict(
			value=total_str,
			table_tr=table_tr0,
			startTime=start_time,
			totalTime=total_time,
			appVersion= app_version,
			caseList=case_url,
			robotlog= robot_log_url
		)

		# 生成html报告

		with open(report_file, 'wb') as f:
			f.write(output.encode('utf-8'))

		report_url = '('+up2qiniu(report_file, "jwtime1", report_file)+')'
		os.remove(report_file)

		#if i == 1 or i == 2 or i == 3 or i%30 == 0:#前三次报告发出来，后面每20次发一次报告
		# if i == 20:
		DingMessage().dingtalk_robot(str(case_len),str(count_success),str(count_case_fail),report_url)
	# u.app_uninstall('com.yoosee')
	# 	try:
	# 		FileUp().main()
	# 	except:
	# 		pass
		if do_not_run == '否':
			break
		# elif count_case_fail >=20:
		# 	u.screen_off()
		# 	u.unlock()
		# elif count_case_fail >=40:
		# 	sleep(8000)
		# 	break
