from machine import Pin,I2C,SPI,PWM,Timer,ADC
import framebuf
import time

import bmp_file_reader as bmpr
from lcd import LCD_1inch28
from qmi import QMI8658

Vbat_Pin = 29

def DOF_READ():
    qmi8658=QMI8658()
    Vbat= ADC(Pin(Vbat_Pin))   

    while(True):
        # read QMI8658
        xyz=qmi8658.Read_XYZ()
        print('[Telemetry output]', [round(i, 2) for i in xyz])
        
        LCD.fill(LCD.white)
        
        LCD.fill_rect(0,0,240,40,LCD.green)
        LCD.text("Alien Tracker",70,25,LCD.black)
        
        LCD.fill_rect(0,40,240,40,LCD.blue)
        LCD.text("VUCTF{Wh00sh}",70,60,LCD.white)

        LCD.fill_rect(0,80,120,120,0x1805)
        LCD.text("ACC_X={:+.2f}".format(xyz[0]),20,100-3,LCD.white)
        LCD.text("ACC_Y={:+.2f}".format(xyz[1]),20,140-3,LCD.white)
        LCD.text("ACC_Z={:+.2f}".format(xyz[2]),20,180-3,LCD.white)

        LCD.fill_rect(120,80,120,120,0xF073)
        LCD.text("GYR_X={:+3.2f}".format(xyz[3]),125,100-3,LCD.white)
        LCD.text("GYR_Y={:+3.2f}".format(xyz[4]),125,140-3,LCD.white)
        LCD.text("GYR_Z={:+3.2f}".format(xyz[5]),125,180-3,LCD.white)
        
        LCD.fill_rect(0,200,240,40,0x180f)
        reading = Vbat.read_u16()*3.3/65535 * 3
        LCD.text("Vbat={:.2f}".format(reading),80,215,LCD.black)
        
        LCD.show()


def to_color(red, green, blue):
    brightness = 1.0
    
    # Convert from 8-bit colors for red, green, and blue to 5-bit for blue and red and 6-bit for green.
    b = int((blue / 255.0) * (2 ** 5 - 1) * brightness)
    r = int((red / 255.0) * (2 ** 5 - 1) * brightness)
    g = int((green / 255.0) * (2 ** 6 - 1) * brightness)
    
    # Shift the 5-bit blue and red to take the correct bit positions in the final color value
    bs = b << 8
    rs = r << 3
    
    # Shift the 6-bit green value, properly handling the 3 bits that overlflow to the beginning of the value
    g_high = g >> 3
    g_low = (g & 0b000111) << 13
    
    gs = g_high + g_low
    
    # Combine together the red, green, and blue values into a single color value
    color = bs + rs + gs
    
    return color

def read_bmp_to_buffer(lcd_display, file_handle):
    reader = bmpr.BMPFileReader(file_handle)
    
    for row_i in range(0, reader.get_height()):
        row = reader.get_row(row_i)
        for col_i, color in enumerate(row):
            lcd_display.pixel(col_i, row_i, to_color(color.red, color.green, color.blue))



if __name__=='__main__':
    qmi8658=QMI8658()
    LCD = LCD_1inch28()

    LCD.fill(LCD.black)
    LCD.text("Booting..",90,115,LCD.green)
    LCD.show()
    
    print("loading")
    with open("images/studsec_logo.bmp", "rb") as input_stream:
        read_bmp_to_buffer(LCD, input_stream)
    print("done")
    LCD.show()
    LCD.set_bl_pwm(65535)

    # Wait for device to be picked up
    while True:
        xyz=qmi8658.Read_XYZ()
        if abs(round(xyz[3], 2)) > 50 or abs(round(xyz[4], 2)) > 50 or abs(round(xyz[5], 2)) > 50:
            break
    print("[Device picked up] VUCTF{I_E4t_S3r14l_f0r_brEAkfAst}")
        
    print("[Info] Calibrating sensors...")
    LCD.text("Calibrate sensors",50,30,LCD.black)
    LCD.show()
    for i in range(3):
        while True:
            xyz=qmi8658.Read_XYZ()
            if abs(round(xyz[i], 2)) > 3:
                break
        LCD.text(f"Sensor {i} calibrated",40,40 + i*10,LCD.black)
        LCD.show()
        print(f"[Info] Sensor {i} calibrated")
    
    for i in range(3,6):
        while True:
            xyz=qmi8658.Read_XYZ()
            if abs(round(xyz[i], 2)) > 500:
                break
        print(f"[Info] Sensor {i} calibrated")
        LCD.text(f"Sensor {i} OK",40,70 + i*10,LCD.black)
        LCD.show()
    print("[Device ready]")

    DOF_READ()
