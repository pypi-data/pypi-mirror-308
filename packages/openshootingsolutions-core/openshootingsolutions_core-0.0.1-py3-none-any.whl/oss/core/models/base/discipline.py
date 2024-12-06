from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass
class BaseAction:
    name: str
    start_offset: float
    description: str
    worker: str
    action: str
    arguments: list


@dataclass
class BaseStep:
    name: str


@dataclass
class BasePhase:
    name: str
    name_abbreviation: str
    description: str


@dataclass
class BaseStage:
    name: str
    name_abbreviation: str
    description: str


@dataclass
class BaseDiscipline:
    # Each discipline needs an uuid so we can keep track of the discipline in logging.
    # This is mostly for debugging.
    identifier: UUID
    name: str
    name_abbreviation: str
    managing_organization: str
    timer_type: str
    description: str
