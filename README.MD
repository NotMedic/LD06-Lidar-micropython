### Micropython code to process LD06 Lidar data packets
There are 3 files in this repo, a library to process individual data packets, and two ways to retrieve the packets over serial:

1. main.py: an inefficent method that looks for the packet header and version
2. main-bulkprocess.py: a way to grab the entire data buffer from the serial port

ld06.py contains a fairly efficient way to process the data and is heavily commented. 


References:
[Inno Maker Product Page](https://www.inno-maker.com/product/lidar-ld06/)
[Inno Maker Datasheet](https://www.inno-maker.com/wp-content/uploads/2020/11/LDROBOT_LD06_Datasheet.pdf)
[Elecrow Development Manual](https://www.elecrow.com/download/product/SLD06360F/LD19_Development%20Manual_V2.3.pdf)
