from ld06 import processpacket
from machine import UART

ser = UART(1, baudrate=230400, tx=0, rx=26)

buffer = b''

while True:
    # Read a large chunk of data. Micropython holds >1k of data in the buffer, or ~20 packets
    chunk = ser.read(1024)
    if chunk is not None:
        buffer += chunk

    # Process all complete packets in the buffer
    while True:
        #Look for the packet header and version
        start = buffer.find(b'\x54\x2c')
        if start == -1:
            # No complete packet in buffer
            break
        if len(buffer) < start + 47:
            # Incomplete packet in buffer
            break

        # Extract and process packet
        packet = buffer[start+2:start+47]
        data = processpacket(packet)
        for reading in data:
            print(reading)

        # Remove processed packet from buffer
        buffer = buffer[start+2+47:]