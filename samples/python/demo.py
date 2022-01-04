# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wechat
import json
import time
from wechat import WeChatManager, MessageType, WxidConst
import traceback
import os
from playsound import playsound

current_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
os.chdir(father_path)


# 这里测试类回调， 函数回调与类回调可以混合使用
class LoginTipBot(wechat.CallbackHandler):

	my_wxid = {}

	@wechat.RECV_CALLBACK(in_class=True)
	def on_message(self, client_id, message_type, message_data):
		# 判断登录成功后，就向文件助手发条消息
		if message_type == MessageType.MT_USER_LOGIN:
			self.my_wxid[client_id] = message_data.get("wxid")

		# 过滤非消息
		if not isinstance(message_data, dict):
			print(message_type)
			return
		# 获取群聊关注信息
		if self.is_room_msg(message_data) and message_data.get("room_wxid") in WxidConst.FORCE_ROOM:
			if message_type == MessageType.MT_RECV_LINK_MSG and "餐品赠送" in message_data.get("raw_msg", ""):
				playsound("C:\Windows\Media\Ring03.wav")
		# 发送消息
		if message_data.get("from_wxid") == self.my_wxid[client_id]:
			print(message_type, message_data)
		if message_data.get("from_wxid") in WxidConst.FORCE_WX:
			print(message_type, message_data)


	def is_room_msg(self, message_data):
		if message_data.get("msg", "").endswith("@chatroom"):
			return True
		return False


if __name__ == "__main__":
	bot = LoginTipBot()

	wechat_manager = WeChatManager(libs_path='../../libs')

	# 添加回调实例对象
	wechat_manager.add_callback_handler(bot)
	wechat_manager.manager_wechat(smart=True)

	# 阻塞主线程
	while True:
		time.sleep(0.5)
