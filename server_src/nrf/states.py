from enum import Enum

class States(Enum):
    """ Possible states of a nRF52480 Dongle """
    STATE_LEADER   = b'leader'
    STATE_CHILD    = b'child'
    STATE_ROUTER   = b'router'
    STATE_DISABLED = b'disabled'
