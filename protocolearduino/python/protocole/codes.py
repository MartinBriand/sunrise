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