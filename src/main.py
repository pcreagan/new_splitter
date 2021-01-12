import time

from src.objects.gpio import GPIO
from src.objects.uart import *
from src.objects.udp import UDP


def test_serial():
    try:
        gpio = GPIO()
        uart = UART()
        for ch in range(1, 12):
            gpio.set(ch)
            print('GPIO setting:', gpio.get())
            time.sleep(.1)
            try:
                print('SN', uart.SN)
            except Exception as e:
                print('ERROR:', str(e))
    except KeyboardInterrupt:
        print('stopped early')


def test_udp():
    udp = UDP()
    udp.get_and_write()


if __name__ == '__main__':
    test_udp()
