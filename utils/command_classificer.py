import re
from configparser import ConfigParser
from typing import Union, List, Dict, Set, Tuple

from utils import Calculator, nearest_string


class Parameter:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"Parameter({self.name})"

    def __hash__(self):
        return hash(self.name)

IntParametr = Parameter("int")
StringParamtr = Parameter("str")
FloatParametr = Parameter("float")


class CommandClassificer:
    def __init__(self, config_file: Union[str, ConfigParser]):
        self.calc = Calculator(None, config_file)
        self.cmds = {}
        self.tokens = {}

    def add_command(self, command: str, parametrs: Set[Parameter], category: str, tokens: Set[Union[Tuple[str], str]]):
        command = command.lower()
        cmd = " ".join(sorted(command.split()))
        self.cmds[cmd] = (command, parametrs, category)
        self.tokens[cmd] = tokens

    def get_params_by_command(self, command: str):
        command = command.lower()
        cmd = self.find_nearest_command(command, raw=True)
        if cmd is None:
            return []
        cmd = cmd[0]
        ans = []
        _, parametrs, category = self.cmds[cmd]
        for _type in parametrs:
            if _type == IntParametr:
                ans += re.findall("\d+", command)
            elif _type == FloatParametr:
                ans += re.findall("\d*.\d+", command)
            elif _type == StringParamtr:
                passif = cmd.split()
                for ss in command.split():
                    if nearest_string(passif, ss) is None:
                        ans.append(ss)
        return category, ans

    def add_commands(self, commands: List[str], parametrs: Set[Parameter], category: str, tokens: Set[Union[Tuple[str], str]]):
        for c in commands:
            self.add_command(c.lower(), parametrs, category, tokens)


    def find_nearest_command(self, command: str, raw: bool = False):
        command = command.lower()
        potencial = list(filter(
            lambda x: self.check_tokens(self.tokens[x], command),
            self.cmds.keys()
        ))
        ans = None
        for pot in potencial:
            pot = pot.split()
            success = 0
            for ss in command.split():
                if bool(nearest_string(pot, ss)):
                    success += 1
            if success >= int(2 * len(pot) / 3):
                ans = " ".join(pot)
                break
        if ans is None:
            return None
        return self.cmds[ans][0] if not raw else ans, self.cmds[ans][2]

    @staticmethod
    def check_tokens(tokens: Set[Union[Tuple[str], str]], command: str):
        for i in tokens:
            if type(i) == str:
                if i not in command:
                    return False
            elif type(i) == tuple:
                if not any([j in command for j in i]):
                    return False
        return True
