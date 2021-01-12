from socket import socket
from socket import timeout
from typing import Optional

from src.constants import LENGTH
from src.constants import SOCKET_KWARGS
from src.constants import TIMEOUT
from src.error import FatalError
from src.objects.config import CONFIG

__all__ = [
    'UDP',
]


class UDP:
    PACKET_LENGTH = LENGTH
    SOCKET_KWARGS = SOCKET_KWARGS

    def __init__(self) -> None:
        self._socket_address = CONFIG.SPM_ADDRESS

    def __post_init__(self):
        self.udp = socket(**self.SOCKET_KWARGS)
        try:
            self.udp.bind(self._socket_address)
            self.udp.settimeout(TIMEOUT)

        except OSError as e:
            raise FatalError from e

    def get(self) -> Optional[bytes]:
        try:
            return self.udp.recvfrom(self.PACKET_LENGTH)[0]

        except timeout:
            return None

    def cleanup(self) -> None:
        self.udp.close()
