import struct

# Packet Structure
# All packets start with 0x54 for the first byte, have a static version of 0x2c for the second byte, then the following structure:
#packet = b'\x0b\x0e\xc8\x45\x33\x02\xea\x43\x02\xec\x24\x02\xec\xa8\x01\xe4\xa1\x01\xee\x9e\x01\xee\xa3\x01\xee\xa5\x01\xee\xa0\x01\xef\xa4\x01\xed\xa6\x01\xee\xa7\x01\xee\x04\x49\x37\x6b\xc0'
#           speed  ,startan,distanc,int,distanc,int,distanc,int,distanc,int,distanc,int,distanc,int,distanc,int,distanc,int,distanc,int,distanc,int,distanc,int,distanc,int,endangl,timesta,crc

# speed:  35.95, 0e 0b
# startangle:  178.64, 45 c8
# endangle:  186.92, 49 04
# timestamp:  27447, 6b 37
# crc:  192, c0
#
# --------Data: 3 bytes per reading, 12 readings
# Distance: 563, 02 33
# Confidence: ea
# Angle: 178.6
# Distance: 579, 02 43
# Confidence: ec
# Angle: 179.3
# 

def processpacket(packet):
    ## Some things are commented out for efficiency. Uncomment if you need them.
    ## Packet Header
    #speed = struct.unpack('<H', packet[0:2])[0] #Bytes 0 and 1, little endian, degrees per second
    startangle = struct.unpack('<H', packet[2:4])[0] / 100 #Bytes 2 and 3, little endian, convert to float

    ## Packet Footer
    endangle = struct.unpack('<H', packet[40:42])[0] / 100 #Bytes 40 and 41, little endian, convert to float
    #timestamp = struct.unpack('<H', packet[42:44])[0] #Bytes 42 and 43
    #crc = struct.unpack('<B', packet[44:45])[0] #Byte 44

    #print("Speed:", speed, "Start Angle:", startangle, "End Angle:", endangle, "TimeStamp:", timestamp, "CRC:", crc)

    ## Packet Data
    if(endangle - startangle > 0):
        angleStep = float(endangle - startangle)/(12)
    else:
        angleStep = float((endangle + 360) - startangle)/(12)

    angleStep %= 360 # Normalize angleStep to 0-360

    data = []
    counter = 0
    num_readings = 12 # 12 readings per packet
    bytes_per_reading = 3 # 3 bytes per reading: 2 for distance, 1 for intensity
    sample_ratio = 1 # 1 = process every reading, 2 = process every other packet, etc.

    for i in range(0, num_readings * bytes_per_reading, 3 * sample_ratio):
        angle = round((angleStep * i/3 + startangle) % 360, 1) # Angle of the reading, Degrees
        distance = struct.unpack('<H', packet[4+i:6+i])[0] # First 2 bytes of the data structure, little endian, distance in mm
        #intensity = struct.unpack('<B', packet[6+i:7+i])[0] # Last byte of the data structure, intensity of returned light, 0-255
        counter += 1
        
        data.append([angle, distance])

    return data