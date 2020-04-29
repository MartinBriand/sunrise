from time import sleep
from .codes import CODEARD, CODEPY
import traceback
import numpy as np

def receive_code(protocole, timeout = True):
	"""receive a code and return it if there is no error"""
	if timeout:
		protocole.serial.timeout = protocole.MAX_TIME_TO_RECEIVE_A_BYTE
	else:
		protocole.serial.timeout = None

	b = protocole.serial.read(1)
	if len(b) == 1:
		i = int.from_bytes(b, byteorder='little')
		if i in [obj.value for obj in CODEARD]:
			return CODEARD(i)
		else:
			raise ValueError('Received a wrong byte code : ' + str(i))
	raise IOError('Getting code was too long')


def receive_specific_code(protocole, code, timeout = True):
	"""Receive a code and check if it the one expected in code. If not, raise an error. If yes, do nothing."""
	b = receive_code(protocole, timeout)
	if b == CODEARD.ERRORARD:
		protocole._handle_arduino_exception()
		raise IOError('Received an error code from Arduino')

	elif b != code:
		raise ValueError('Wrong code, received {0} but expected {1}'.format(repr(b), repr(code)))


def receive_uint32_t(protocole):
	protocole.serial.timeout = 4* protocole.MAX_TIME_TO_RECEIVE_A_BYTE
	b = protocole.serial.read(4)
	if len(b) == 4:
		return int.from_bytes(b, byteorder='little')
	raise IOError('Getting uint32_t was too long')

def send_vector_of_8_int32_t (protocole, vector):
	"""Vector MUST be an int32_t numpy vector of lenght 8"""
	if len(vector) != 8:
		raise ValueError('Vector has length {0} but 8 was expected'.format(len(vector)))
	if vector.dtype != np.dtype('int32'):
		raise ValueError('Vecotr has dtype {0} but {1} was expected'.format(repr(vector.dtype), repr(np.dtype('int32'))))
	to_send = np.zeros(len(vector), dtype='uint32')
	for k in range (len(vector)):
		to_send[k] = int(vector[k]) + 2147483648
	for k in range (len(vector)):
		protocole.serial.write(int.to_bytes(int(to_send[k]), 4, 'big'))
