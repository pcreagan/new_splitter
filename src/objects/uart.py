import functools
from struct import unpack
from time import perf_counter
from time import sleep
from typing import List
from typing import Optional

from serial import Serial
from serial import SerialTimeoutException

from src.constants import BAUDRATE_REGISTER
from src.constants import BREAK_LEN
from src.constants import BROADCAST_ADDRESS
from src.constants import CRC_OPERAND_ARRAY
from src.constants import MAB_LEN
from src.constants import MEMORY_CHANNEL_ID_REGISTER
from src.constants import OPCODE
from src.constants import SERIAL_KWARGS
from src.constants import SN_REGISTER
from src.constants import TARGET
from src.constants import TX_WAIT_S
from src.error import UARTBadResponseError
from src.error import UARTNoResponseError

__all__ = [
    'UART',
]


# noinspection PyPep8Naming
class UART:
    # ? https://www.raspberrypi.org/forums/viewtopic.php?t=188233
    CRC_OPERAND_ARRAY = CRC_OPERAND_ARRAY
    BROADCAST_ADDRESS = BROADCAST_ADDRESS
    SERIAL_KWARGS = SERIAL_KWARGS
    TX_WAIT_S = TX_WAIT_S
    BREAK_LEN = BREAK_LEN
    MAB_LEN = MAB_LEN
    SN_REGISTER = SN_REGISTER
    BAUDRATE_REGISTER = BAUDRATE_REGISTER
    MEMORY_CHANNEL_ID_REGISTER = MEMORY_CHANNEL_ID_REGISTER

    def calc_crc(self, packet: List[int]) -> List[int]:
        _array = self.CRC_OPERAND_ARRAY
        crc = 0
        for b in packet:
            crc = _array[crc ^ b]
        return [crc]

    @functools.lru_cache(maxsize=256)
    def format_dec(self, dec: int, num_bytes: int = 4) -> list:
        return [(dec & (0xFF << i)) >> i for i in range(0, num_bytes * 8, 8)]

    @staticmethod
    def get_payload(rx: List[int]) -> int:
        return int(''.join([str(byte)[2:].zfill(2) for byte in map(hex, reversed(rx))]), 16)

    # noinspection DuplicatedCode
    def build_packet(self, address: int, target: TARGET, opcode: OPCODE, index: int, value: int = 0):
        if not isinstance(target, TARGET):
            target = TARGET(target)
        payload, opcode = [index], opcode.value
        if not bool(opcode):
            payload = [index] + self.format_dec(value, num_bytes=4)
        size = len(payload) + 1
        packet = [0x77, size] + self.format_dec(address, num_bytes=3) + \
                 [target.value * 2 + opcode] + \
                 [0x0] * (size % 4) + payload
        return packet + self.calc_crc(packet)

    def validate_packet(self, rx: List[int]) -> None:
        if rx[0] != 0x77:
            raise ValueError
        if rx[-1:] != self.calc_crc(rx[:-1]):
            raise ValueError

    def parse_rx(self, rx: bytes) -> int:
        try:
            print('RX RAW:', rx)
            rx = list(unpack('<' + ("B" * len(rx)), rx))
            self.validate_packet(rx)
            return self.get_payload(rx)
        except ValueError:
            raise UARTBadResponseError

    def write_eeprom(self, target: TARGET, index: int, payload: int) -> None:
        self.tx_uart(bytes(self.build_packet(self.BROADCAST_ADDRESS, target, OPCODE.WRITE, index, payload)))

    def read_eeprom(self, target: TARGET, index: int) -> int:
        self.tx_uart(bytes(self.build_packet(self.BROADCAST_ADDRESS, target, OPCODE.READ, index)))
        return self.rx_uart()

    def rx_uart(self, num_bytes: int = 9) -> Optional[int]:
        try:
            return self.parse_rx(self.serial.read(num_bytes))
        except SerialTimeoutException:
            raise UARTNoResponseError

    def __init__(self) -> None:
        self.serial = None
        self.next_activity = None
        self.open()

    def open(self, baudrate=None) -> None:
        kwargs = dict(**self.SERIAL_KWARGS)
        if baudrate:
            kwargs = dict(**kwargs, baudrate=baudrate)
        self.serial = Serial(**kwargs)
        self.next_activity = perf_counter() + self.TX_WAIT_S

    @property
    def baud(self) -> int:
        return self.serial.baudrate

    @baud.setter
    def baud(self, value: int):
        self.serial.close()
        self.serial = Serial(value)

    # noinspection DuplicatedCode
    def tx_uart(self, data: bytes) -> None:

        # wait for micro mainloop to cycle
        wait_time = self.next_activity - perf_counter()
        sleep(max(0., wait_time))

        # serial break
        self.serial.break_condition = True
        sleep(self.BREAK_LEN)

        # MAB
        self.serial.break_condition = False
        self.serial.reset_input_buffer()
        sleep(self.MAB_LEN)

        # write bytes to UART and flush serial port
        self.serial.write(data)
        self.serial.flush()

        self.next_activity = perf_counter() + self.TX_WAIT_S

    def cleanup(self) -> None:
        try:
            self.serial.close()
        except Exception as e:
            print(str(e))

    @property
    def SN(self) -> int:
        return self.read_eeprom(TARGET.CONFIG, self.SN_REGISTER)

    @SN.setter
    def SN(self, payload: int):
        self.write_eeprom(TARGET.CONFIG, self.SN_REGISTER, payload)

    @property
    def BAUDRATE(self) -> int:
        return self.read_eeprom(TARGET.CONFIG, self.BAUDRATE_REGISTER)

    @BAUDRATE.setter
    def BAUDRATE(self, payload: int):
        self.write_eeprom(TARGET.CONFIG, self.BAUDRATE_REGISTER, payload)

    @property
    def MEMORY_CHANNEL_ID(self):
        return self.read_eeprom(TARGET.CONFIG, self.MEMORY_CHANNEL_ID_REGISTER)

    @MEMORY_CHANNEL_ID.setter
    def MEMORY_CHANNEL_ID(self, payload: int):
        self.write_eeprom(TARGET.CONFIG, self.MEMORY_CHANNEL_ID_REGISTER, payload)
