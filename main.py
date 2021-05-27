import serial


ser = serial.Serial('com4', baudrate = 38400, parity= serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)

while 1:
    a=ser.readline()
    print(a)

