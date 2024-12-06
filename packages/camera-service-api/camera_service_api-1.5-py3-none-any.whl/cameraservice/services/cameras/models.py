from typing import Union, List


class ImageShape:
	def __init__(self, shape : Union[List[int]|None] = None ):
		if shape is None:
			self.width = 0
			self.height = 0
			self.channel = 0
		else:
			self.width = int(shape[0])
			self.height = int(shape[1])
			self.channel = int(shape[2])
		self.image_type = ""
		self.quality = 0
		self.method = 0


class ImageRequest:
	def __init__(self, sn, s:ImageShape):
		self.sn = sn
		self.imageShape = s
