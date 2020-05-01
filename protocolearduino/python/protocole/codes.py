from enum import IntEnum

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

class ERRORARDCODE (IntEnum): #more than 20
  WRONG_INSTRUCTION = 20,
  TOO_MANY_INSTRUCTIONS = 21,
  START_WITHOUT_INITIALIZATION = 22,
  ASK_FEED_BAD_ANSWER = 23,
  RECEIVED_WRONG_MEMORY = 24,
  BYTE_TIMEOUT = 25,