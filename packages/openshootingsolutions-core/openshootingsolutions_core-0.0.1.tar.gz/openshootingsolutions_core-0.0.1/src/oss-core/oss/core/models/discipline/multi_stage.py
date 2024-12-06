import json
import pkgutil
from dataclasses import dataclass

from oss.core.models.base.discipline import (
    BaseAction,
    BaseDiscipline,
    BasePhase,
    BaseStage,
    BaseStep,
)
from oss.core.models.discipline.single_stage import SingleStageDiscipline


@dataclass
class DisciplineAction(BaseAction):
    # No extra fields for now
    pass


@dataclass
class MultiStageStep(BaseStep):
    actions: list[DisciplineAction]


@dataclass
class MultiStagePhase(BasePhase):
    steps: list[MultiStageStep]


@dataclass
class MultiStageStage(BaseStage):
    phases: list[MultiStagePhase]


@dataclass
class MultiStageDiscipline(BaseDiscipline):
    stages: list[MultiStageStage]


class Discipline:

    @staticmethod
    def load_discipline(
        discipline_filename: str, discipline_package: str = "oss.core.models.discipline.configurations"
    ) -> MultiStageDiscipline | SingleStageDiscipline:
        file_content = pkgutil.get_data(package=discipline_package, resource=discipline_filename)
        if not file_content:
            raise FileNotFoundError(f"Discipline file not found: {discipline_filename}")

        # Load the json file as dict. This first needs to be a standard dict so the timer type can be extracted.
        # The timer type is needed for determining the correct class to cast to.
        discipline_configuration = json.loads(file_content)

        timer_type = discipline_configuration.get("timer_type")

        print(timer_type)

        # Pointer to single or multi-stage
        return MultiStageDiscipline(**discipline_configuration)
