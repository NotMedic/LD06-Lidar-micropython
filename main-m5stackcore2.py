#this is a playground.

from ld06 import processpacket
from machine import UART
from m5stack import lcd, btnA, btnB, btnC
import math
import time


def draw_pixel(angle, distance, intensity, scale):
  # Convert the angle to radians
  angle_rad = math.radians(angle)

  # Scale the distance
  distance_scaled = distance / scale

  # Calculate the x and y coordinates
  x = int(distance_scaled * math.cos(angle_rad))
  y = int(distance_scaled * math.sin(angle_rad))

  # Center the coordinates
  x_centered = 240 // 2 - x  # Subtract x from the half of the screen's height
  y_centered = y + 320 // 2
  color = intensity << 16 | intensity << 8 | intensity

  # If the pixel for this angle is already drawn at the same coordinates, skip drawing
  if pixels[angle] != 0 and pixels[angle] == (y_centered, x_centered):
    return

  # If the pixel for this angle is drawn at different coordinates, blank the old pixel
  if pixels[angle] != 0:
    lcd.pixel(pixels[angle][0], pixels[angle][1], 0x000000)

  # Store the new coordinates and draw the new pixel
  pixels[angle] = (y_centered, x_centered)
  lcd.pixel(y_centered, x_centered, color)
    
last_updated = {}
lcd.setRotation(lcd.LANDSCAPE_FLIP)
ser = UART(1, baudrate=230400, tx=0, rx=13)

pixels = [0] * 361

scale = 25

def buttonC_wasPressed():
  global scale, pixels
  lcd.clear()
  pixels = [0] * 361
  scale = scale + 5

def buttonA_wasPressed():
  global scale, pixels
  lcd.clear()
  pixels = [0] * 361
  scale = scale - 5

def buttonB_wasPressed():
  global pixels
  lcd.clear()
  pixels = [0] * 361

btnA.wasPressed(buttonA_wasPressed)
btnB.wasPressed(buttonB_wasPressed)
btnC.wasPressed(buttonC_wasPressed)

import time

def doit():
    lcd.clear()
    pixel_count = 0
    start_time = time.time()
    while True:
        char = ser.read(1)
        if char == b'\x54':  # Packet Header
            char = ser.read(1)
            if char == b'\x2c':  # Packet Version
                packet = ser.read(45)
                data = processpacket(packet)
                for reading in data:
                    draw_pixel(round(reading[0]), reading[1], reading[2], scale)
                    pixel_count += 1

        # Calculate and print pixels per second every second
        if time.time() - start_time >= 1:
            pixels_per_second = pixel_count / (time.time() - start_time)
            print('Pixels per second: {}'.format(pixels_per_second))
            pixel_count = 0
            start_time = time.time()

# This is the same as the previous function, but with a larger buffer
def doit2():
    buffer = b''
    pixel_count = 0
    start_time = time.time()

    while True:
      # Read a large chunk of data. Micropython holds >1k of data in the buffer, or ~20 packets
      chunk = ser.read(1500)
      if chunk is not None:
        buffer += chunk

      # Process all complete packets in the buffer
      while True:
        # Look for the packet header and version
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
          draw_pixel(round(reading[0]), reading[1], reading[2], scale)
          pixel_count += 1

        # Remove processed packet from buffer
        buffer = buffer[start+2+47:]

      # Calculate and print pixels per second every second
      if time.time() - start_time >= 1:
        pixels_per_second = pixel_count / (time.time() - start_time)
        print('Pixels per second: {}'.format(pixels_per_second))
        pixel_count = 0
        start_time = time.time()

doit2()