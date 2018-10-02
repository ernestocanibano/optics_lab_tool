"""
Date: 6/4/2017
Author: Ernesto Cañibano
Documentation: This module is a library to manage the Konika CS200 luminance meter.
Due the use of Kmsecs200.dll, this module only works with Python 3 32 bits.
Main function: Wrap dll library inside a Python module.
Target: Manage the luminance meter.
"""

from ctypes import *
import time

# Utilizacion de las libreris de la DLL. Hay que importarla 
# con WinDLL porque es del tipo stdcall.
dll = WinDLL('luminance_meter/Kmsecs200.dll')  


def read64_usb(index=0, timeout=1, readLen=250):
    aux = create_string_buffer(250)
    dll.read64_usb(c_int(index), aux, c_int(timeout), c_int(readLen))
    aux2 = cast(aux, c_char_p)
    #print(aux2.value) #DEBUG MODE
    return aux2.value

def write64_usb(index, cmd, timeout=1):
    dll.write64_usb(c_int(index), c_char_p(cmd), c_int(timeout), c_int(len(cmd)))
    return 0
	
def sendCommand_usb(index, cmd, timeout=1):
    write64_usb(index, cmd) #send command
    return read64_usb(index)

def open_instrument(index):
    if dll.int_usb(c_int(index)) < 0:
        print("ERROR: Cannot open instrument")
        return -1
    time.sleep(0.5)
    sendCommand_usb(index, b"RMT,1\r\n") #enable remote mode
    sendCommand_usb(index, b"MSS,0\r\n") #set measurement mode 
    sendCommand_usb(index, b"SPS,5, 1\r\n") #set measurement speed and duration
    sendCommand_usb(index, b"OBS,0\r\n") #set observer setting
    sendCommand_usb(index, b"LNS,0\r\n") #set lens
    return 0
	
def close_instrument(index):
    sendCommand_usb(index, b"RMT,0\r\n") #disable remote mode
    dll.end_usb(c_int(index))
    return 0
	
def read_instrument(index):
    result = sendCommand_usb(index, b"MES,1\r\n") #enable measure
    if b"OK" in result:
        keywords = result.decode().split(",")
        nTime = int(keywords[1])
        time.sleep(nTime)
        measure = sendCommand_usb(index, b"MDR,0\r\n") #read measure
        if b"OK" in measure:
            measures = measure.decode().split(",")
            return [0.0, float(measures[9]), float(measures[10]), float(measures[11])]
    return [-1.0, 0.0, 0.0, 0.0]
		