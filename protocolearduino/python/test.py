from protocole.protocole import Protocole
import serial
from time import sleep
import numpy as np
from threading import Lock

protocole = Protocole(
	serial.Serial('COM4', 9600),
	4000,
	np.array([-9,-8,-7,-6,-5,-4,-3,-2], dtype='int32'),
	np.array([[1,4,1,4,1,4,1,4],[2,3,2,3,2,3,2,3], [1,2,1,2,1,2,1,2], [2,1,2,1,2,1,2,1], [2,2,2,2,2,2,2,2], [3,1,3,1,3,1,3,1]], dtype='int32'),
	Lock()
)
sleep(3) # let enought time to the serial connection to connect
#p.init()

protocole.setup()
protocole.start()
sleep(1)
protocole.stop()
sleep(1)
protocole.start()
protocole.close()


