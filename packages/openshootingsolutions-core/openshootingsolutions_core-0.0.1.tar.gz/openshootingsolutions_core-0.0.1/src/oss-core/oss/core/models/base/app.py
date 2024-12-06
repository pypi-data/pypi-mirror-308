from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class BaseApp(ABC):
    """
    A base app
    """

    # Each app needs an uuid so we can keep track of each app that is loaded
    _identifier: UUID = uuid4()

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def terminate(self) -> None:
        raise NotImplementedError
