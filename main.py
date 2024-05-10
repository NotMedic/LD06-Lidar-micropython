from ld06 import processpacket
from machine import UART

ser = UART(1, baudrate=230400, tx=0, rx=26)

while True:
    char = ser.read(1)
    if char == b'\x54':  # Packet Header
        char = ser.read(1)
        if char == b'\x2c':  # Packet Version
            packet = ser.read(45)
            data = processpacket(packet)
            for reading in data:
                print(reading)
    else:
        print("Invalid Packet Header")