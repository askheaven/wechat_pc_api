# -*- coding: utf-8 -*-
from message.replies import Replies

def talk_time():
	localtime = time.localtime(time.time())
	hours = localtime.tm_hour
	if 0 <= hours <= 5:
		return ''
	elif 5 < hours <= 11:
		return '早上'
	elif 11 < hours <= 14:
		return '中午'
	elif 14 < hours <= 18:
		return '下午'
	elif 18 < hours <= 24:
		return '晚上'

config = {
	"baidu_cloud": {
		"enable": False,
		"app_id": "",
		"api_key": "",
		"secret_key": ""
	},
}
amiya_name = ["兔兔", "阿米娅"]

class AmiyaBot(Replies):

	def __init__(self, wechat_manager):
		self.wechat_manager = wechat_manager
		self.my_wxid = None
		self.group = {}
		self.client_id = None

	def reply(self, to_wxid, text):
		self.wechat_manager.send_text(self.client_id, to_wxid, text)

	def init(self, client_id, wxid):
		self.client_id = client_id
		self.my_wxid = wxid


	@wechat.RECV_CALLBACK(in_class=True)
	def on_message(self, client_id, message_type, message_data):
		if message_type == MessageType.MT_USER_LOGIN:
			self.init(client_id, message_data.get("wxid"))
			# 获取所有群组
			wechat_manager.get_chatrooms(client_id)
		
		elif message_type == MessageType.MT_DATA_CHATROOMS_MSG:
			# 初始化群组
			for room_data in message_data:
				room_wxid = room_data.get("wxid", "")
				if not room_wxid:
					return
				self.group[room_wxid] ={
					"nickname":room_data.get("nickname"),
					"member_list":{}
				}
				room_member = wechat_manager.get_chatroom_members(client_id, room_wxid)

		elif message_type == MessageType.MT_DATA_CHATROOM_MEMBERS_MSG:

			room_wxid = message_data.get("group_wxid")
			member_dict = {member["wxid"]:member["nickname"] for member in message_data.get("member_list")}
			# 初始化群组成员
			if not self.group[room_wxid]["member_list"]:
				for room_data in message_data["member_list"]:
					self.group[room_wxid]["member_list"] = member_dict
				return
			# 欢迎新人
			new_member = list(set(member_dict.keys()).difference(set(self.group[room_wxid]["member_list"]).keys()))
			for member in new_member:
				wechat_manager.send_chatroom_at_msg(client_id, room_wxid, "欢迎@{}🎉🎉🎉🎉🎉".format(member_dict[member]), [member])

		elif message_type == MessageType.MT_RECV_SYSTEM_MSG:
			# 新人加群消息
			room_wxid = message_data.get("room_wxid", "")
			if not room_wxid:
				return
			room_member = wechat_manager.get_chatroom_members(client_id, room_wxid)
			
		elif message_type == MessageType.MT_RECV_TEXT_MSG:
			to_wxid = message_data["to_wxid"]
			from_wxid=message_data["from_wxid"]
			if from_wxid == self.my_wxid[client_id]:
				return
			if to_wxid.endswith("@chatroom"):
				data = {
					'text': message_data["msg"],
					'text_digits': '',
					'user_id':from_wxid,
					'is_at': False,
					'nickname': self.group[to_wxid]["member_list"][from_wxid],
					'to_wxid':to_wxid,
				}
				self.text_msg(data)



	



		# # 处理函数列表（有先后顺序）
		# reply_func = [
		# 	{
		# 		# 打招呼
		# 		'func': self.greeting,
		# 		'need_call': False
		# 	},
		# 	{
		# 		# 等待事件
		# 		'func': self.waiting,
		# 		'need_call': False
		# 	},
		# 	{
		# 		# 管理员指令
		# 		'func': self.admin,
		# 		'need_call': True
		# 	},
		# 	{
		# 		# 表情包
		# 		'func': self.face_image,
		# 		'need_call': True
		# 	},
		# 	{
		# 		# 信赖事件
		# 		'func': self.emotion,
		# 		'need_call': True
		# 	},
		# 	{
		# 		# 使用功能
		# 		'func': function.action,
		# 		'need_call': True,
		# 		'without_call': True
		# 	},
		# 	{
		# 		# 自然语言处理
		# 		'func': self.natural_language_processing,
		# 		'need_call': True
		# 	}
		# ]


# class AmiyaBot(wechat.CallbackHandler):

# 	my_wxid = {}
# 	group = {}
# 	client_id = None

# 	def Reply(self, client_id, to_wxid, text, *args):
# 		wechat_manager.send_text(client_id, to_wxid, text)

# 	@wechat.RECV_CALLBACK(in_class=True)
# 	def on_message(self, client_id, message_type, message_data):
		
# 		# print(message_type, message_data)
# 		if message_type == MessageType.MT_USER_LOGIN:
# 			self.client_id = client_id
# 			self.my_wxid[client_id] = message_data.get("wxid")
# 			print(self.my_wxid)
# 			wechat_manager.get_chatrooms(client_id)
# 		elif message_type == MessageType.MT_DATA_CHATROOMS_MSG:
# 			for room_data in message_data:
# 				room_wxid = room_data.get("wxid", "")
# 				if not room_wxid:
# 					return
# 				self.group[room_wxid] ={
# 					"nickname":room_data.get("nickname"),
# 					"member_list":{}
# 				}
# 				room_member = wechat_manager.get_chatroom_members(client_id, room_wxid)

# 		elif message_type == MessageType.MT_DATA_CHATROOM_MEMBERS_MSG:
# 			room_wxid = message_data.get("group_wxid")
# 			member_dict = {member["wxid"]:member["nickname"] for member in message_data.get("member_list")}

# 			if not self.group[room_wxid]["member_list"]:
# 				for room_data in message_data["member_list"]:
# 					self.group[room_wxid]["member_list"] = member_dict
# 				return
# 			new_member = list(set(member_dict.keys()).difference(set(self.group[room_wxid]["member_list"]).keys()))
# 			for member in new_member:
# 				wechat_manager.send_chatroom_at_msg(client_id, room_wxid, "欢迎@{}🎉🎉🎉🎉🎉".format(member_dict[member]), [member])

# 		elif message_type == MessageType.MT_RECV_SYSTEM_MSG:
# 			room_wxid = message_data.get("room_wxid", "")
# 			if not room_wxid:
# 				return
# 			room_member = wechat_manager.get_chatroom_members(client_id, room_wxid)
# 		elif message_type == MessageType.MT_RECV_TEXT_MSG:
# 			to_wxid = message_data["to_wxid"]
# 			from_wxid=message_data["from_wxid"]
# 			if from_wxid == self.my_wxid[client_id]:
# 				return
# 			if to_wxid.endswith("@chatroom"):
# 				data = {
# 					'text': message_data["msg"],
# 					'text_digits': '',
# 					'user_id':from_wxid,
# 					'is_at': False,
# 					'nickname': self.group[to_wxid]["member_list"][from_wxid],
# 					'to_wxid':to_wxid,
# 				}
# 				self.text_msg(data)

# 	def text_msg(self, data):
# 		self.greeting(data)

# 	def greeting(self, data):
# 		message = data['text']
# 		nickname = data['nickname']

# 		for item in ['不能休息', '不能停', '不要休息', '不要停', '很多事情']:
# 			if item in message:
# 				pass

# 		for item in ['早上好', '早安', '中午好', '午安', '下午好', '晚上好']:
# 			if item in message:
# 				hour = talk_time()
# 				text = ''
# 				if hour:
# 					text += 'Dr.%s，%s好～' % (nickname, hour)
# 				else:
# 					text += 'Dr.%s，这么晚还不睡吗？要注意休息哦～' % nickname
# 				# status = sign_in(data)

# 				# if status['status']:
# 				# 	text += '\n' + status['text']

# 				# feeling = reward if status['status'] else 2
# 				# coupon = reward if status['status'] else 0
# 				# sign = 1 if status['status'] else 0

# 				return self.Reply(self.client_id, data["to_wxid"], text)

# 		if '签到' in message and word_in_sentence(message, amiya_name[0]):
# 			status = sign_in(data, 1)
# 			if status:
# 				feeling = reward if status['status'] else 2
# 				coupon = reward if status['status'] else 0
# 				sign = 1 if status['status'] else 0

# 				return self.Reply(self.client_id, data["to_wxid"], text)

# 		if '晚安' in message:
# 			return self.Reply(self.client_id, data["to_wxid"], 'Dr.%s，晚安～' % nickname)

# 		for name in amiya_name[1]:
# 			if message.find(name) == 0:
# 				text = '哼！Dr.%s不许叫人家%s，不然人家要生气了！' % (nickname, name)
# 				return self.Reply(self.client_id, data["to_wxid"], text)



# 		# # 处理函数列表（有先后顺序）
# 		# reply_func = [
# 		# 	{
# 		# 		# 打招呼
# 		# 		'func': self.greeting,
# 		# 		'need_call': False
# 		# 	},
# 		# 	{
# 		# 		# 等待事件
# 		# 		'func': self.waiting,
# 		# 		'need_call': False
# 		# 	},
# 		# 	{
# 		# 		# 管理员指令
# 		# 		'func': self.admin,
# 		# 		'need_call': True
# 		# 	},
# 		# 	{
# 		# 		# 表情包
# 		# 		'func': self.face_image,
# 		# 		'need_call': True
# 		# 	},
# 		# 	{
# 		# 		# 信赖事件
# 		# 		'func': self.emotion,
# 		# 		'need_call': True
# 		# 	},
# 		# 	{
# 		# 		# 使用功能
# 		# 		'func': function.action,
# 		# 		'need_call': True,
# 		# 		'without_call': True
# 		# 	},
# 		# 	{
# 		# 		# 自然语言处理
# 		# 		'func': self.natural_language_processing,
# 		# 		'need_call': True
# 		# 	}
# 		# ]
		