from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4

from oss.core.message import BrokerConnection


@dataclass
class SchedulerAction:
    stage_number: int
    stage_name: str
    phase_number: int
    phase_name: str
    step_number: int
    step_name: str
    action_number: int
    action: str
    action_worker: str
    action_arguments: list
    start_offset: float


class SchedulerState(Enum):
    STOPPED: str = "STOPPED"
    PAUSED: str = "PAUSED"
    WAITING: str = "WAITING"
    RUNNING: str = "RUNNING"
    INVALID: str = "INVALID"


class TimerControl(Enum):
    TOGGLE_PHASE: str = "TOGGLE_PHASE"
    RESET_PHASE: str = "STOP_PHASE"
    NEXT_PHASE: str = "NEXT_PHASE"
    PREVIOUS_PHASE: str = "PREVIOUS_PHASE"
    RESET_STAGE: str = "RESET_STAGE"
    NEXT_STAGE: str = "NEXT_STAGE"
    PREVIOUS_STAGE: str = "PREVIOUS_STAGE"
    SET_TOGGLE_DELAY: str = "SET_TOGGLE_DELAY"


class BaseTimer(ABC):
    # Each timer needs an uuid so we can keep track of which timer triggered an action.
    # This is mostly for debugging.
    _identifier: UUID = uuid4()

    # Each remote needs an connection to the message broker to send commands
    _broker_connection: BrokerConnection

    state: SchedulerState

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def __del__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _handle_broker_message(self, ch, method, properties, body) -> None:
        raise NotImplementedError
