from protocole import CODEARD, CODEPY, Protocole
import serial
from time import sleep

p = Protocole(serial.Serial('COM4', 9600))
sleep(3)

p.init()



