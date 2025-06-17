import time
from const import *



class Interface:
    def __init__(self, spi, cs, dc, rst, busy):
        
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        
    def cmd(self, command):
        
        self.dc.value(0)
        
        self.spi.write(bytes([command]))
        
    def data(self, data):
        
        self.dc.value(1)
        
        self.spi.write(bytes(data))
        
    def cmd_and_data(self, command, data):
        self.cmd(command)
        self.data(data)
        
    def wait_idle(self):
        while self.busy.value():
            #print("WAITING")
            time.sleep_ms(10)
            
    def reset(self):
        self.rst.value(0)
        time.sleep_ms(10)
        self.rst.value(1)
        time.sleep_ms(10)
        


class SSD1680:
    def __init__(self, interface):
        
        self.interface = interface
    
    def init(self):
        
        self.interface.reset()
        self.interface.cmd(SW_RESET)
        self.interface.wait_idle()

        self.interface.cmd_and_data(DRIVER_CONTROL, [HEIGHT - 1, 0x00, 0x00])
        
        self.use_full_frame()
        
        self.interface \
            .cmd_and_data(
                 BORDER_WAVEFORM_CONTROL,
                [BORDER_WAVEFORM_FOLLOW_LUT | BORDER_WAVEFORM_LUT1]
            )
        
        self.interface \
            .cmd_and_data(
                TEMP_CONTROL,
                [INTERNAL_TEMP_SENSOR]
            )
        
        self.interface \
            .cmd_and_data(
                DISPLAY_UPDATE_CONTROL,
                [0x80, 0x80],
            )
        
        self.interface.cmd_and_data(DATA_ENTRY_MODE, [DATA_ENTRY_INCRY_INCRX])

        
        #self.display_frame()


        
        
        
        
        
        self.interface.wait_idle()
        
        
    def use_full_frame(self):
        self.set_ram_area(0, 0, WIDTH - 1, HEIGHT - 1)
        self.set_ram_counter(0, 0)
        
    def set_ram_area(self, start_x, start_y, end_x, end_y):
        self.interface.cmd_and_data( \
            SET_RAMXPOS,
            [(start_x >> 3), (end_x >> 3)],
        )

        self.interface.cmd_and_data( \
            SET_RAMYPOS,
            [
                start_y,
                (start_y >> 8),
                end_y,
                (end_y >> 8),
            ],
        )
        
    def set_ram_counter(self, x, y):
        
        self.interface \
            .cmd_and_data(SET_RAMX_COUNTER, [(x >> 3)])

        self.interface \
            .cmd_and_data(SET_RAMY_COUNTER, [y, (y >> 8)])
        
    def clear_bw_frame(self):
        self.use_full_frame()
        
        self.interface.cmd(WRITE_BW_DATA)
        #for i in range((WIDTH / 8)  * HEIGHT):
        self.interface.data([0xFF] * ((16)  * HEIGHT))
            
    def clear_red_frame(self):
        self.use_full_frame()
        
        self.interface.cmd(WRITE_RED_DATA)
        
        self.interface.data([0xFF] * ((16)  * HEIGHT))
        
        
    def display_frame(self):
        self.interface.cmd_and_data(
            UPDATE_DISPLAY_CTRL2,
            [DISPLAY_MODE_1]
        )
        
        self.interface.wait_idle()
        
        self.interface.cmd(MASTER_ACTIVATE)
        self.interface.wait_idle()
        
    def update_bw_frame(self, buf):
        self.use_full_frame()
        self.interface.cmd_and_data(WRITE_BW_DATA, buf)
        
