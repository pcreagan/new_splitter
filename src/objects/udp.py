from socket import socket
from socket import timeout
from typing import Optional

from src.objects.constants import LENGTH
from src.objects.constants import SOCKET_KWARGS
from src.objects.constants import TIMEOUT
from src.objects.error import FatalError

__all__ = [
    'UDP',
]


class UDP:
    PACKET_LENGTH = LENGTH
    SOCKET_KWARGS = SOCKET_KWARGS

    def __init__(self, address=None) -> None:
        self._opened = False
        if address:
            self._socket_address = address
        else:
            from src.objects.config import Config

            config = Config()
            self._socket_address = config.SPM_ADDRESS

        self.open()

    def open(self):
        self.udp = socket(**self.SOCKET_KWARGS)
        try:
            self.udp.bind(self._socket_address)
            self.udp.settimeout(TIMEOUT)

        except OSError as e:
            raise FatalError from e
        else:
            self._opened = True

    def get(self) -> Optional[bytes]:
        try:
            return self.udp.recvfrom(self.PACKET_LENGTH)[0]

        except timeout:
            return None

    def get_and_write(self):
        data = self.get()
        if data:
            from pathlib import Path
            p = Path().resolve().absolute()
            print('dir:', p)
            with open(p / 'from_spm.txt', 'w+') as f:
                f.write(repr(data))

    def close(self) -> None:
        if self._opened:
            self.udp.close()
            self._opened = False

    def __del__(self):
        self.close()
