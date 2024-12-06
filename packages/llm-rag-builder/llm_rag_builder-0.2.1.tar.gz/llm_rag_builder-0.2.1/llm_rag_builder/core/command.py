from abc import ABC
import re
import json

RUN_COMMAND_STRING = '<RUNFUNC> {name}({data}) </RUNFUNC>'
RUN_COMMAND_PATTERN = r'.*<RUNFUNC>\s*(?P<name>\w+)\s*\((?P<data>.*?)\)\s*</RUNFUNC>.*'


class BaseCommand(ABC):
    name: str
    description: str
    params: dict
    examples: list
    run: callable

    def __init__(self, name: str, description, run: callable, examples: list | None = None, params: dict | None = None):
        self.name = name
        self.description = description
        self.params = params or {}
        self.examples = examples or []
        self.run = run

    def to_dict(self) -> dict:
        """Convert the command to a dictionary."""
        return {
            'command': self.name,
            'args': self.params,
            'description': self.description
        }

    def check_params(self, params: dict) -> bool:
        """Check if the given parameters are valid."""
        for param in self.params:
            if param not in params.keys():
                return False
        return True

    def check_is_command(self, run_command_string: str) -> bool:
        """Check if the function is a valid function."""
        run_command_string = run_command_string.replace('\n', '')
        groups = re.match(RUN_COMMAND_PATTERN, run_command_string)
        if groups is None:
            return False

        func_name = groups.group('name')
        if not func_name:
            return False
        if func_name != self.name:
            return False

        func_data = groups.group('data')
        if not func_data and self.params:
            return False
        try:
            data = json.loads(func_data) if func_data else {}
        except json.JSONDecodeError:
            return False
        if not self.check_params(data):
            return False

        return True

    def get_command_string(self, data) -> str:
        """Get the command string."""
        return RUN_COMMAND_STRING.format(name=self.name, data=data)

    def run_command(self, run_command_string: str) -> str:
        """Run the command."""
        run_command_string = run_command_string.replace('\n', '')
        groups = re.match(RUN_COMMAND_PATTERN, run_command_string)
        func_data = groups.group('data')
        data = json.loads(func_data) if func_data else {}
        return self.run(**data)
