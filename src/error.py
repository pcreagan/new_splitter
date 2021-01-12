__all__ = [
    'ThreadError',
    'FatalError',
    'UARTNoResponseError',
    'UARTBadResponseError',
]


class FatalError(Exception):
    pass


class ThreadError(Exception):
    pass


class UARTNoResponseError(Exception):
    pass


class UARTBadResponseError(Exception):
    pass
