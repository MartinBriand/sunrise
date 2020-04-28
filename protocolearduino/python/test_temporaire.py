from protocole import CODEARD, CODEPY, Protocole
import serial
from time import sleep

p = Protocole(serial.Serial('COM4', 9600), 4000)
sleep(3)

#p.init()

p.send_speed()
p.send_speed()
p.init()
p.init()
p.send_speed()
p.init()
p.ask_memory()
p.ask_memory()
p.send_speed()
p.init()
p.ask_memory()
p.send_start()
sleep(5)
p.send_stop()
sleep(5)
p.send_start()
sleep(5)
p.send_stop()
sleep(5)
p.send_start()
sleep(5)
p.send_stop()
sleep(5)
# sleep(1)
# p.init()
# print(p.serial.in_waiting)
# p.ask_memory()



