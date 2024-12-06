from enum import Enum

from oss.timer.timers.competition import CompetitionTimer
from oss.timer.timers.stage import StageTimer


class Timer(Enum):
    STAGE: StageTimer = StageTimer
    COMPETITION: CompetitionTimer = CompetitionTimer
