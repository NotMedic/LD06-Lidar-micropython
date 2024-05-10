### Micropython code to process LD06 Lidar data packets
There are 3 files in this repo, a library to process individual data packets, and two ways to retrieve the packets over serial:

1. main.py: an inefficent method that looks for the packet header and version
2. main-bulkprocess.py: a way to grab the entire data buffer from the serial port

ld06.py contains a fairly efficient way to process the data and is heavily commented. 