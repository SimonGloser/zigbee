import serial
"""
Dieser Teil wird spaeter in eine seperate funktion ausgelagert. Dieser stand dient nur zu demozwecken
"""

ser = serial.Serial('com4', baudrate = 38400, parity= serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)

while 1:
    a=ser.readline()
    print(a)

