from enum import IntEnum
from time import sleep
import traceback

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


def receive_code(protocole):
	"""receive a code and return it if there is no error"""
	protocole.serial.timeout = protocole.MAX_TIME_TO_RECEIVE_A_BYTE
	b = protocole.serial.read(1)
	if len(b) == 1:
		i = int.from_bytes(b, byteorder='little')
		if i in [obj.value for obj in CODEARD]:
			return CODEARD(i)
		else:
			raise ValueError('Received a wrong byte code : ' + str(i))
	raise IOError('Getting code was too long')

def receive_specific_code(protocole, code):
	"""Receive a code and check if it the one expected in code. If not, raise an error. If yes, do nothing."""
	b = receive_code(protocole)
	if b != code:
		raise ValueError('Wrong code, received {0} but expected {1}'.format(repr(code), repr(CODEARD.ACK)))


def receive_uint32_t(protocole):
	protocole.serial.timeout = 4* protocole.MAX_TIME_TO_RECEIVE_A_BYTE
	b = protocole.serial.read(4)
	if len(b) == 4:
		return int.from_bytes(b, byteorder='little')
	raise IOError('Getting uint32_t was too long')




class Protocole:
#Be careful !! We send data with big bytes first and receive them with little bytes first

	def __init__ (self, serial, speed):
		self.serial = serial
		self.MAX_TIME_TO_RECEIVE_A_BYTE = 100 #in milliseconds
		self.data_initialized = False
		self.memory_initialized = False
		self.speed_of_iter_initialized = False
		self.pos_0_inititialized = False
		self.is_started = False
		self.speed_of_iter = speed


	def init(self): #works well (tested)
		self.__init__(self.serial, self.speed_of_iter)
		#protocole
		self.serial.write(int.to_bytes(CODEPY.INITIAL.value, 1, 'big'))
		#check
		try:
			receive_specific_code(self, CODEARD.ACK)
			print('Init is a success')
		except Exception:
			traceback.print_exc()
			self.send_error()


	def send_error(self):
		#protocole
		self.__init__(self.serial, self.speed_of_iter)
		self.serial.write(int.to_bytes(CODEPY.ERRORPY.value, 1, 'big'))
		sleep(2) #to let enough time to the Arduino board to empty the stack of bytes sent

	def send_speed(self): #works bad
		#protocole
		self.serial.write(int.to_bytes(CODEPY.SPEED.value, 1, 'big'))
		#first ack
		receive_specific_code(self, CODEARD.ACK)
		#value
		self.serial.write(int.to_bytes(self.speed_of_iter, 4, 'big'))
		#check
		try:
			received = receive_uint32_t(self)
			if received != self.speed_of_iter:
				raise ValueError('Wrong speed, received {0}, but expected {1}'.format(received, self.speed_of_iter))
			self.speed_of_iter_initialized = True
			print("Speed successfully sent")
		except Exception:
			traceback.print_exc()
			self.send_error()

		



	def ask_memory(self):
		#protocole
		self.serial.write(int.to_bytes(CODEPY.MEMORY.value, 1, 'big'))
		#receive and check
		try:
			received = receive_uint32_t(self)
			self.serial.write(int.to_bytes(received, 4, 'big'))
			receive_specific_code(self, CODEARD.ACK)
			self.memory = received
			self.memory_initialized = True
			print("Memory successfully received : {0}".format(self.memory))
		except Exception:
			traceback.print_exc()
			self.send_error()



	# def send_pos_0(self):
	# 	return None

	# def send_data(self):
	# 	return None

	def send_stop(self):
		#protocole
		self.serial.write(int.to_bytes(CODEPY.STOP.value, 1, 'big'))
		#ack
		try:
			receive_specific_code(self, CODEARD.ACK)
			print("Stop is successfully sent")
		except Exception:
			traceback.print_exc()
			self.send_error()


	def send_start(self):
		#protocole
		self.serial.write(int.to_bytes(CODEPY.START.value, 1, 'big'))
		#ack
		try:
			receive_specific_code(self, CODEARD.ACK)
			print ('Start successfully sent')
		except:
			traceback.print_exc()
			self.send_error()


	# def handle_arduino_exception(self):
	# 	return None

	# def handle_feed_demand(self):
	# 	return None



