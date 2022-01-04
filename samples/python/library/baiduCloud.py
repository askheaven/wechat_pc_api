from aip import AipNlp, AipOcr


class NaturalLanguage:
	def __init__(self, options):
		if options['enable']:
			self.client = AipNlp(options['app_id'], options['api_key'], options['secret_key'])
			self.enable = True
		else:
			self.client = None
			self.enable = False

	# 情感倾向分析
	def sentiment_classify(self, text):
		if self.enable is False:
			return False
		result = self.client.sentimentClassify(text)
		if 'error_code' in result:
			print(result['error_msg'])
			return False
		return result

	# 对话情绪分析
	def emotion(self, text):
		if self.enable is False:
			return False
		result = self.client.emotion(text, {
			'scene': 'talk'
		})
		if 'error_code' in result:
			print(result['error_msg'])
			return False
		return result


class OpticalCharacterRecognition:
	def __init__(self, options):
		if options['enable']:
			self.client = AipOcr(options['app_id'], options['api_key'], options['secret_key'])
			self.enable = True
		else:
			self.client = None
			self.enable = False

	def basic_general(self, image):
		if self.enable is False:
			return False
		options = {
			'detect_direction': 'true'
		}
		result = self.client.basicGeneralUrl(image, options)

		return result

	def basic_accurate(self, image):
		if self.enable is False:
			return False
		options = {
			'detect_direction': 'true'
		}
		result = self.client.basicAccurate(image, options)

		return result
