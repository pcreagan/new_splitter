from src.constants import CONFIG_PATH
from src.error import FatalError

__all__ = [
    'CONFIG',
]


class Config:
    _spm_address = None

    # noinspection PyPep8Naming
    @property
    def SPM_ADDRESS(self):
        """
        cached (ip, port)
        """
        if not self._spm_address:
            self._spm_address = self.get_address()
        return self._spm_address

    def find_config(self):
        """
        if config file location is known and static, return it
        else implement glob or something to find it
        """
        # TODO
        _ = self
        fp = CONFIG_PATH
        return fp

    def get_address(self):
        """
        get and parse smp ip address config file
        fatal on fail
        """
        try:
            with open(self.find_config()) as f:
                ip, port = list(f.readlines())
            _address = ip.strip(), int(port)
            return _address

        except Exception as e:
            raise FatalError('FAILED TO LOAD CONFIG') from e


CONFIG = Config()
