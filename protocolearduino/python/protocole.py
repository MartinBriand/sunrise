from enum import IntEnum
import time

class CODEARD(IntEnum):
	FEED = 6,
	ACK = 10,
	ERRORARD = 11,  

class CODEPY(IntEnum):
	INITIAL = 2,
	SPEED = 3,
	MEMORY = 4,
	POS_0 = 5,
	DATA = 7,
	STOP = 8,
	START = 9,
	ERRORPY = 11,


def receiveCode(protocole):
	start = time.time()
	while time.time() - start < protocole.MAX_TIME_TO_RECEIVE_A_BYTE:
		if protocole.serial.in_waiting > 0:
			a = int.from_bytes(protocole.serial.read(1), byteorder='little')
			if a in [obj.value for obj in CODEARD]:
				return CODEARD(a)
			else:
				raise ValueError('Received a wrong byte code : ' + a)
			break
	raise IOError('Getting code was too long')



class Protocole:


	def __init__ (self, serial):
		self.serial = serial
		self.MAX_TIME_TO_RECEIVE_A_BYTE = 100 #in milliseconds

	def init(self):
		self.serial.write(int.to_bytes(CODEPY.INITIAL.value, 1, 'big'))
		#try:
		code = receiveCode(self)
		if code != CODEARD.ACK:
			raise ValueError('Wrong code, received {0} but expected {1}'.format(repr(code), repr(CODEARD.ACK)))
		#except Exception as e:
			#print(e)
			#self.handleException(e)




