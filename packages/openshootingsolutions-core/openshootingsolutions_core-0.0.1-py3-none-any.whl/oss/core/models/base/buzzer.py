from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from oss.core.message import BrokerConnection


class BaseBuzzer(ABC):
    # Each buzzer needs an uuid so we can keep track of the buzzer in logging.
    # This is mostly for debugging.
    _identifier: UUID = uuid4()

    # Each buzzer needs an connection to the message broker to receive commands
    _broker_connection: BrokerConnection

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def __del__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _handle_broker_message(self, ch, method, properties, body) -> None:
        raise NotImplementedError

    @abstractmethod
    def play(self, duration: float):
        raise NotImplementedError
