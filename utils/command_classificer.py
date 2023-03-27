from configparser import ConfigParser
from typing import Union, List

from utils import Calculator


class Parameter:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"Parameter({self.name})"

IntParametr = Parameter("int")
StringParamtr = Parameter("str")
FloatParametr = Parameter("float")


class CommandClassificer:
    def __init__(self, config_file: Union[str, ConfigParser], tokens: List[str]):
        self.calc = Calculator(None, config_file)
        self.cmds = []
        self.tokens = tokens

    def add_command(self, command: str, parametrs: List[Parameter]):
        pass
