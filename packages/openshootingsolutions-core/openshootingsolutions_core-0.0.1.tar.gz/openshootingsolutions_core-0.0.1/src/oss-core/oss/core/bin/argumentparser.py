import argparse
import os
from typing import Any

from dotenv import load_dotenv


class ArgumentParser:
    @staticmethod
    def load_dotenv_file(filepath: str) -> None:
        # First load the supplied .env file. This way any "default" or packaged env variables can being overwritten.
        # every argument can be loaded via the environment variables
        load_dotenv(dotenv_path=filepath)

    @staticmethod
    def parse_environment_variables(launch_argument_model: Any) -> dict:
        environment_variables: dict = {}
        for field_name, field_metadata in launch_argument_model.model_fields.items():
            environment_variable_name = field_name.upper()

            # If it is an Optional type then extract the inner (real) type
            if hasattr(field_metadata.annotation, "__args__"):
                field_type = [
                    variable_type
                    for variable_type in field_metadata.annotation.__args__
                    if variable_type is not type(None)
                ][0]
            else:  # This is already a real type
                field_type = field_metadata.annotation

            # Retrieve the environment variable and cast it into the required type
            environment_variable_value = os.getenv(environment_variable_name)
            if environment_variable_value is not None:
                environment_variables[field_name] = field_type(environment_variable_value)
        return environment_variables

    @staticmethod
    def parse_commandline_arguments(launch_argument_model: Any) -> dict:
        argument_parser: argparse.ArgumentParser = argparse.ArgumentParser()
        argument_parser.prog = "oss_worker"

        for field_name, field_metadata in launch_argument_model.model_fields.items():
            argument_name = f"--{field_name}"  # Use --field_name format
            default = field_metadata.default if field_metadata.default is not None else argparse.SUPPRESS

            # If it is an Optional type then extract the inner (real) type
            if hasattr(field_metadata.annotation, "__args__"):
                field_type = [
                    variable_type
                    for variable_type in field_metadata.annotation.__args__
                    if variable_type is not type(None)
                ][0]
            else:  # This is already a real type
                field_type = field_metadata.annotation

            help_text = field_metadata.description or ""

            # Add argument based on field type and constraints
            if field_type == bool:  # Boolean needs to be handled differently
                argument_parser.add_argument(argument_name, action="store_true", help=help_text)
            else:
                argument_parser.add_argument(argument_name, type=field_type, default=default, help=help_text)
        commandline_arguments: dict = argument_parser.parse_known_args()[0].__dict__
        return commandline_arguments

    @staticmethod
    def parse_arguments(launch_argument_model: Any) -> Any:
        # Parse commandline arguments
        commandline_arguments: dict = ArgumentParser.parse_commandline_arguments(
            launch_argument_model=launch_argument_model
        )

        # If the commandline arguments specify a worker_config .env file load it.
        if commandline_arguments.get("worker_config"):
            # Load the dotenv files to overwrite default environment variables
            ArgumentParser.load_dotenv_file(filepath=commandline_arguments["worker_config"])

        # Parse the environment variables
        environment_variables: dict = ArgumentParser.parse_environment_variables(
            launch_argument_model=launch_argument_model
        )

        # Merge the environment variables and commandline arguments. Commandline arguments have priority.
        return launch_argument_model(**{**environment_variables, **commandline_arguments})
