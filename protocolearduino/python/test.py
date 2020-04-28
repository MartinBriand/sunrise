import serial
from time import sleep


ser = serial.Serial('COM4', 9600)
sleep(3)
print(ser)



k = 3

vector = [300 for i in range (k)]
print (vector)
for i in vector:
	ser.write(int.to_bytes(i, 2, 'big'))


print('cest envoye')
print(int.from_bytes(ser.read(2), 'little'))
# print(int.from_bytes(ser.read(), 'big') == sum(vector))
# print(ser.in_waiting)

# print('tamere')

# for k in range(10):