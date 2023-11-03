# Board: Waveshare RP2040-one
# Interpreter: Adafruit CircuitPython 8.0.5
# 100K pullup: between GP29 u. 3V3
# NTC: between GP29 und GND
#
# created by M. Schmidl, November 2023
#
import time
import microcontroller
import board
import analogio
import usb_cdc

def read_serial(serial):
    available = serial.in_waiting
    text = ""
    while available:
        raw = serial.read(available)
        text = raw.decode("utf-8")
        available = serial.in_waiting
    return text

# NTC connected to ADC3/GP29 with 100K Pullup
ntc = analogio.AnalogIn(board.A3)

def get_voltage():
    return (ntc.value * 3.3) / 65535

def calc_RtR25():
    Vadc = get_voltage()
    Rt = (100000 * Vadc) / (3.3 - Vadc)
    return (Rt / 100000)

def get_temperature( RtR25 ):
   if RtR25 >= 3.75:
      return 0
   if RtR25 >= 2.82:
      return 5
   if RtR25 >= 2.67:
      return 6
   if RtR25 >= 2.53:
      return 7
   if RtR25 >= 2.39:
      return 8
   if RtR25 >= 2.27:
      return 9
   if RtR25 >= 2.15:
      return 10
   if RtR25 >= 2.04:
      return 11
   if RtR25 >= 1.93:
      return 12
   if RtR25 >= 1.83:
      return 13
   if RtR25 >= 1.74:
      return 14
   if RtR25 >= 1.65:
      return 15      
   if RtR25 >= 1.57:
      return 16      
   if RtR25 >= 1.49:
      return 17      
   if RtR25 >= 1.42:
      return 18      
   if RtR25 >= 1.35:
      return 19      
   if RtR25 >= 1.28:
      return 20
   if RtR25 >= 1.22:
      return 21
   if RtR25 >= 1.16:
      return 22
   if RtR25 >= 1.10:
      return 23
   if RtR25 >= 1.05:
      return 24
   if RtR25 >= 1.0:
      return 25
   if RtR25 >= 0.95:
      return 26
   if RtR25 >= 0.91:
      return 27
   if RtR25 >= 0.87:
      return 28
   if RtR25 >= 0.83:
      return 29
   if RtR25 >= 0.79:
      return 30
   if RtR25 >= 0.75:
      return 31
   if RtR25 >= 0.72:
      return 32
   if RtR25 >= 0.69:
      return 33
   if RtR25 >= 0.65:
      return 34
   if RtR25 <= 0.63:
      return 35
   if RtR25 >= 0.50:
      return 40
   if RtR25 >= 0.40:
      return 45
   if RtR25 >= 0.33:
      return 50
   if RtR25 >= 0.27:
      return 55
   if RtR25 >= 0.22:
      return 60
   if RtR25 >= 0.18:
      return 65
   if RtR25 >= 0.15:
      return 70
   if RtR25 >= 0.12:
      return 75
   return 100
       
def showHelp():
    print("")
    print("")
    print("?   show this help")
    print("!   measure NTC temperature")
    print(".   measure CPU temperature")
    print("n  measure automatically every n seconds")
    print("0  stops automatic measurement")
    print(">")

showHelp()
serial = usb_cdc.console
buffer = ""
nextTime = 0
interval = 1
while True:
    temperature = microcontroller.cpu.temperature
    #print(str(int(time.monotonic())) + ',' + str(int(temperature)))
    
    if interval != 0 and time.monotonic() >= nextTime:
       nextTime = time.monotonic() + interval
       print(get_temperature(calc_RtR25()))    
    
    buffer += read_serial(serial)
    if buffer.endswith("\n") or buffer.endswith("\r"):
        # strip line end
        input_line = buffer[:-1]
        # clear buffer
        buffer = ""
        # handle input
        if input_line.startswith("?"):
            showHelp()
        if input_line.startswith("!"):
            print(get_temperature(calc_RtR25()))
        if input_line.startswith("."):
            print(int(microcontroller.cpu.temperature))
        if input_line.isdigit():
            interval = int(input_line)
            nextTime = time.monotonic() + interval

