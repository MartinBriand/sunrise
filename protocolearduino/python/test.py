from protocole.protocole import Protocole
import serial
import numpy as np
from time import sleep

# ser = serial.Serial('COM4', 9600)
# print(ser)
protocole = Protocole(
	'COM4', 9600,
	4000,
	np.array([-9,-8,-7,-6,-5,-4,-3,-2], dtype='int32'),
	np.array([[1,4,1,4,1,4,1,4],[2,3,2,3,2,3,2,3], [1,2,1,2,1,2,1,2], [2,1,2,1,2,1,2,1], [2,2,2,2,2,2,2,2], [3,1,3,1,3,1,3,1]], dtype='int32'),
)

protocole.setup()
protocole.start()
protocole.stop()
protocole.start()
protocole.close()
protocole.stop_and_close()
# protocole.start()
# sleep(2)
# protocole.change_values(pos_0=np.array([2,3,4,5,6,7,8,9], dtype='int32'))
# protocole.setup()
# protocole.start()
# sleep(3)
# protocole.close()


