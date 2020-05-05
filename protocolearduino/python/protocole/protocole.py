from .codes import CODEARD, CODEPY, ERRORARDCODE
from .utils import *
import traceback
import numpy as np
import threading
from time import sleep
import serial


class Protocole:
#Be careful !! We send data with big bytes first and receive them with little bytes first

	def __init__ (self, serial_port, serial_baudrate, speed_of_iter, pos_0, data):
		self.serial = serial.Serial('COM4', 9600)
		sleep(3)
		self._MAX_TIME_TO_RECEIVE_A_BYTE = 10 #in seconds
		self._memory_initialized = False
		self._speed_of_iter_initialized = False
		self._pos_0_inititialized = False
		self._pos_0 = pos_0
		self.is_started = False
		self._speed_of_iter = speed_of_iter
		self._data = data
		self._pos_in_data = 0

		#threads
		self._thread_lock = threading.Lock()
		self._check_thread = threading.Thread(name = 'check', target = self._check_feed_or_error)
		self._is_check_thread_alive = True
		#reset

		self.serial.reset_input_buffer()
		self.serial.reset_output_buffer()


	def stop_and_close(self):
		return self.stop() and self.close()

	def close(self):
		if self.is_started:
			print("Can't close, please stop first")
			return False
		self._is_check_thread_alive = False
		self.serial.close() #enough time to close the connection
		sleep(3)
		print('Protocole is closed')
		return True

	def change_values(self, **new_values):
		self.stop_and_close()
		previous_values = {'speed_of_iter': self._speed_of_iter, 'pos_0':self._pos_0, 'data':self._data}
		for kw in new_values:
			if kw not in previous_values:
				raise ValueError('Kwargs must be speed_of_iter, pos_0 or data, {0} is not accepted'.format(kw))
		previous_values.update(new_values)
		self._speed_of_iter = previous_values['speed_of_iter']
		self._pos_0 = previous_values['pos_0']
		self._data = previous_values['data']
		print ('Values successfully changed')
		return True
	

	def _check_feed_or_error (self):
		from time import time, sleep
		while True:
			self._thread_lock.acquire()
			if self.serial.in_waiting > 0:
				code = receive_code(protocole = self, timeout = False)
				if code == CODEARD.FEED:
					print('Received feed from Arduino in check thread')
					self._handle_feed_demand()
				elif code == CODEARD.ACK:
					self._send_error()
					raise IOError('Received ack in wrong thread from Arduino')
				elif code == CODEARD.ERRORARD:
					self._handle_arduino_exception()
			self._thread_lock.release()
			if(not self._is_check_thread_alive):
				break

	def setup(self):
		self.close()
		res = (self._init() and
			self._ask_memory() and
			self._send_pos_0() and
			self._send_speed()
			)
		self._is_check_thread_alive = True
		self._check_thread.start()
		if res:
			print("Setup successfully finished")
		return res

	

	def _init(self): #works well (tested)
		self.__init__(self.serial.port, self.serial.baudrate, self._speed_of_iter, self._pos_0, self._data)
		#protocole
		self.serial.write(int.to_bytes(CODEPY.INITIAL.value, 1, 'big'))
		#check
		receive_specific_code(self, CODEARD.ACK)
		print('Init is a success')
		return True


	def _send_speed(self): #works well (tested)
		#protocole
		self.serial.write(int.to_bytes(CODEPY.SPEED.value, 1, 'big'))
		#first ack
		receive_specific_code(self, CODEARD.ACK)
		#value
		self.serial.write(int.to_bytes(self._speed_of_iter, 4, 'big'))
		#check
		received = receive_uint32_t(self)
		if received != self._speed_of_iter:
			self._send_error()
			raise ValueError('Wrong speed_of_iter, received {0}, but expected {1}'.format(received, self._speed_of_iter))
		self._speed_of_iter_initialized = True
		print("Speed_of_iter successfully sent")	
		return True

	def _ask_memory(self): #works well (tested)
		#protocole
		self.serial.write(int.to_bytes(CODEPY.MEMORY.value, 1, 'big'))
		#receive and check
		received = receive_uint32_t(self)
		self.serial.write(int.to_bytes(received, 4, 'big'))
		receive_specific_code(self, CODEARD.ACK)
		self.memory = received
		self._memory_initialized = True
		print("Memory successfully received : {0}".format(self.memory))
		return True


	def _send_pos_0(self): #works well (tested with positive and negative values)
		#protocole
		self.serial.write(int.to_bytes(CODEPY.POS_0.value, 1, 'big'))
		#first ack
		receive_specific_code(self, CODEARD.ACK)
		#send
		send_vector_of_8_int32_t(self, self._pos_0)
		#second ack
		receive_specific_code(self, CODEARD.ACK)
		self._pos_0_inititialized = True
		print('Pos_0 successfully sent')
		return True


	def _send_data(self):
		#protocole
		self.serial.write(int.to_bytes(CODEPY.DATA.value, 1, 'big'))
		#first ack
		receive_specific_code(self, CODEARD.ACK)
		#send
		#create data first
		data_to_send = np.zeros((self.memory, 8), dtype = 'int32')
		for k in range(min(self.memory, len(self._data) - self._pos_in_data)):
			data_to_send[k] = self._data[self._pos_in_data + k]
		#send data
		for k in range(len(data_to_send)):
			send_vector_of_8_int32_t(self, data_to_send[k])

		#second ack
		receive_specific_code(self, CODEARD.ACK)
		self._pos_in_data += self.memory
		print("Data successfully sent :")
		print(data_to_send)


	def stop(self):
		self._thread_lock.acquire()
		res = self._stop()
		self._thread_lock.release()
		sleep(0.5)#to let time to the ckeck feed to get messages
		return res

	def _stop(self): #works well (tested)
		#protocole
		self.serial.write(int.to_bytes(CODEPY.STOP.value, 1, 'big'))
		#ack
		receive_specific_code(self, CODEARD.ACK)
		self.is_started=False
		print("Stop successfully sent")
		return True

	def start(self):
		"""returns true if has started and false if a stop blocked the demand"""
		self._thread_lock.acquire()
		res = self._start()
		self._thread_lock.release()
		sleep(0.5) # to let time to the check feed to get messages
		return res

	def _start(self): #works well (tested)
		""""""
		#check
		if not self._memory_initialized:
			raise ValueError("Memory not initialized")
		elif not self._pos_0_inititialized:
			raise ValueError('pos_0 not initialized')
		elif not self._speed_of_iter_initialized:
			raise ValueError('speed_of_iter not initialized')
		#protocole
		self.serial.write(int.to_bytes(CODEPY.START.value, 1, 'big'))
		code = receive_code(self)
		#feed
		self.is_started = True #will help to know if went through stop or not
		if code == CODEARD.FEED:
			print('feed in start')
			self._handle_feed_demand()
			#then ack
			receive_specific_code(self, CODEARD.ACK)
		#or just ack
		elif code != CODEARD.ACK:
			self._send_error()
			raise IOError('Did not receive ACK or FEED as expected')
		if not self.is_started:
			print('Start demand was stopped because Arduino has already executed the full move')
			return False
		else:
			print ('Start successfully sent')
			return True


	def _send_error(self): #not tested yet
		#protocole
		"Sending an Error"
		self.close()
		self.__init__(self.serial.port, self.serial.baudrate, self._speed_of_iter, self._pos_0, self._data)
		self.serial.write(int.to_bytes(CODEPY.ERRORPY.value, 1, 'big'))
		sleep(2) #to let enough time to the Arduino board to empty the stack of received bytes (bytes sent by python)


	def _handle_feed_demand(self):
		if self._pos_in_data >= len(self._data):
			self._stop()
		else:
			self._send_data();


	def _handle_arduino_exception(self):
		error_ard_code = receive_error_code(self)
		raise IOError('Arduino sent an error : {0}'.format(repr(error_ard_code)))

