import time

from gpio import GPIO
from uart import *


def test_one(gpio: GPIO, uart: UART, ch: int) -> None:
	gpio.set(ch)
	print('GPIO setting:', gpio.get())
	time.sleep(.1)
	try:
		print('SN', uart.SN)
	except Exception as e:
		print('ERROR:', str(e))

def main():
	try:
		gpio = GPIO()
		uart = UART()
		[test_one(gpio, uart, i) for i in range(1, 12)]
	except KeyboardInterrupt:
		print('stopped early')


if __name__ == '__main__':
	main()
