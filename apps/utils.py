import base64
import tempfile
from enum import Enum

def get_binary_content(base64_image):
	if len(base64_image) != 0 and len(base64_image)%4==0:
		encoded_bs4 = base64_image
		encoded_bytes=encoded_bs4.encode('utf-8')
		try: 
			binary = base64.decodebytes(encoded_bytes)
			fp = tempfile.TemporaryFile()
			fp.write(binary)
			return fp
		except:
			return None
	return None

class PreparationTime(Enum):
	SHORT = ('short', 'Corto (<20m)')
	MEDIUM = ('medium', 'Medio (20m-1h)')
	LONG = ('long', 'Largo (>1h)')

	@classmethod
	def get_value(cls, member):
		return cls[member].value[0]

class Difficulty(Enum):
	EASY = ('easy', 'Fácil')
	MEDIUM = ('medium', 'Intermedia')
	HARD = ('hard', 'Díficil')

	@classmethod
	def get_value(cls, member):
		return cls[member].value[0]


