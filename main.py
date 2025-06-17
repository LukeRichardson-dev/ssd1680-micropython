import ssd1680 as epd
from const import *
from machine import Pin, SPI
import time

sck = Pin(2, mode=Pin.OUT)
tx = Pin(3, mode=Pin.OUT)
dc = Pin(4, mode=Pin.OUT)
cs = Pin(5, mode=Pin.OUT)
res = Pin(6, mode=Pin.OUT)
busy = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)

cs.value(0)

spi = SPI(0, 1_000_000, mosi=tx, miso=Pin(20), sck=sck)

inf = epd.Interface(spi, cs, dc, res, busy)


disp = epd.SSD1680(inf)
disp.init()


#disp.clear_bw_frame()
disp.clear_red_frame()

data = [0 for i in range(250*16)]
data[0:15] = [255]*15
data[15]=0b11111111
data[16] = 0xFF
disp.update_bw_frame(data)


disp.display_frame()



