import board
import busio
import io

import pynmea2
import serial

from PIL import Image, ImageDraw, ImageFont
import time

# ser = serial.Serial('/dev/ttyS0', 9600, timeout=3.0)
# sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ssd1306

BORDER=5


oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# # Load default font.
font = ImageFont.load_default()

# # Draw Some Text
# text = "Hello World!"
# (font_width, font_height) = font.getsize(text)
# draw.text(
#     (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
#     text,
#     font=font,
#     fill=255,
# )

ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
# font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

offset = 0  # flips between 0 and 32 for double buffering
ti = 0
while True:
    # write the current time to the display after each scroll
    draw.rectangle((0, 0, oled.width, oled.height * 2), outline=0, fill=0)
    text = f"Lat: {str(round(float(ti)/100,2))}"
    # ti +=1
    draw.text((0, 8), text, font=font, fill=255)
    oled.image(image)
    oled.show()

    time.sleep(1)



    try:
        line = sio.readline()
        msg = pynmea2.parse(line)
        print(type(msg))
        if type(msg) == 'pynmea2.types.talker.TXT':
            print("s")
        else:
            if "latitude" in dir(msg):
                ti = msg.lat
                print(msg.longitude)
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        # print('Parse error: {}'.format(e))
        continue


    # for i in range(0, oled.height // 2):
    #     offset = (offset + 1) % oled.height
    #     oled.write_cmd(adafruit_ssd1306.SET_DISP_START_LINE | offset)
    #     oled.show()
    #     time.sleep(0.001)
