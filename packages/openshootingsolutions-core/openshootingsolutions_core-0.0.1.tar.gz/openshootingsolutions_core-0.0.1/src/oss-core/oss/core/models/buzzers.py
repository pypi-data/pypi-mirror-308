from enum import Enum

from oss.buzzer.buzzers.virtual import VirtualBuzzer


class Buzzer(Enum):
    VIRTUAL: VirtualBuzzer = VirtualBuzzer
