try:
    import RPi.GPIO as rpi
except ImportError:
    pass
from src.objects.constants import CHANNELS
from src.objects.constants import PIN_MAP

__all__ = [
    'GPIO',
]


class GPIO:
    PIN_MAP = PIN_MAP
    # PIN_MAP = rpi.BCM

    CHANNELS = CHANNELS

    def make_list(self, ch: int):
        _ch = ch - 1
        l = [bool(_ch & (1 << i)) for i in range(4)]
        return tuple(l)

    def __init__(self) -> None:
        self.last_settings = [False] * 4
        self.is_opened = False
        self.open()

    def open(self):
        mode = rpi.getmode()
        if mode != self.PIN_MAP:
            if mode is not None:
                rpi.cleanup()
            rpi.setmode(self.PIN_MAP)
        self.is_opened = True
        rpi.setwarnings(False)
        rpi.setup(self.CHANNELS, rpi.OUT)

    def set(self, ch: int) -> None:
        self.last_settings = self.make_list(ch)
        rpi.output(self.CHANNELS, self.last_settings)

    def get(self):
        return [rpi.input(ch) for ch in self.CHANNELS]

    def close(self):
        if self.is_opened:
            rpi.cleanup()
            self.is_opened = False

    def __del__(self):
        self.close()
