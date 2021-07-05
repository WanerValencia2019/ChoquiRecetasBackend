import base64
import tempfile

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