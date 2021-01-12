
try:
    import RPi.GPIO as rpi
except ImportError:
    pass


from enum import Enum
from socket import AF_INET
from socket import SOCK_DGRAM

from serial import EIGHTBITS
from serial import STOPBITS_TWO

FRAME_PERIOD = .033
CONFIG_PATH = r'C:\Projects\dmx_splitter\cfg\ini'

TIMEOUT = FRAME_PERIOD * 1.5

PIN_MAP = rpi.BOARD
# PIN_MAP = rpi.BCM
CHANNELS = [7, 11, 13, 15]


LENGTH = 1048
HEADER_LENGTH = 24
FRAME_SIZE = 2 ** 9
FRAME_2_START = HEADER_LENGTH + FRAME_SIZE
START_CODE_1 = b'\x01'
START_CODE_2 = b'\x02'

SOCKET_KWARGS = dict(
    family=AF_INET,
    type=SOCK_DGRAM,
)


class TARGET(Enum):
    DYNAMIC = 1
    CONFIG = 5
    LEGACY = 7
    COMP = 8


class OPCODE(Enum):
    WRITE = 0
    READ = 1


SN_REGISTER = 0x1
BAUDRATE_REGISTER = 0x3
MEMORY_CHANNEL_ID_REGISTER = 0x13

BREAK_LEN = .2
TX_WAIT_S = .02
MAB_LEN = BREAK_LEN
SERIAL_KWARGS = dict(
    # ? https://pyserial.readthedocs.io/en/latest/pyserial_api.html

    # port=r'/dev/ttyAMA0',
    port=r'/dev/serial0',
    # port=r'/dev/ttyS0',

    # baudrate=500000,
    baudrate=250000,

    bytesize=EIGHTBITS,
    stopbits=STOPBITS_TWO,
    timeout=TIMEOUT,
    write_timeout=TIMEOUT,
)

BROADCAST_ADDRESS = 0x0
CRC_OPERAND_ARRAY = [
    0, 7, 14, 9, 28, 27, 18, 21, 56, 63, 54, 49, 36, 35, 42, 45,
    112, 119, 126, 121, 108, 107, 98, 101, 72,
    79, 70, 65, 84, 83, 90, 93, 224, 231, 238, 233, 252, 251, 242,
    245, 216, 223, 214, 209, 196, 195, 202, 205, 144, 151, 158, 153,
    140, 139, 130, 133, 168, 175, 166, 161, 180, 179, 186, 189,
    199, 192, 201, 206, 219, 220, 213, 210, 255, 248, 241, 246, 227, 228, 237,
    234, 183, 176, 185, 190, 171, 172, 165, 162, 143, 136, 129,
    134, 147, 148, 157, 154, 39, 32, 41, 46, 59, 60,
    53, 50, 31, 24, 17, 22, 3, 4, 13, 10, 87, 80, 89, 94, 75, 76,
    69, 66, 111, 104, 97, 102, 115, 116, 125,
    122, 137, 142, 135, 128, 149, 146, 155, 156, 177, 182, 191,
    184, 173, 170, 163, 164, 249, 254, 247, 240, 229,
    226, 235, 236, 193, 198, 207, 200, 221, 218,
    211, 212, 105, 110, 103, 96, 117, 114, 123, 124, 81, 86, 95,
    88, 77, 74, 67, 68, 25, 30, 23, 16, 5, 2, 11, 12, 33,
    38, 47, 40, 61, 58, 51, 52, 78, 73, 64, 71, 82, 85, 92,
    91, 118, 113, 120, 127, 106, 109, 100, 99, 62, 57, 48, 55,
    34, 37, 44, 43, 6, 1, 8, 15, 26, 29, 20, 19, 174, 169,
    160, 167, 178, 181, 188, 187, 150, 145, 152, 159, 138, 141, 132,
    131, 222, 217, 208, 215, 194, 197, 204, 203, 230, 225, 232, 239, 250, 253, 244, 243,
]
