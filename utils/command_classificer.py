import re
from configparser import ConfigParser
from typing import Union, List, Dict, Set, Tuple

import pymorphy2 as pymorphy2

from utils import Calculator, nearest_string


class Parameter:
    def __init__(self, name: str):
        """
        Контейнер, содержащий строку. Создан для удобства.

        :param name: Имя параметра
        """
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
    morph = pymorphy2.MorphAnalyzer(lang="ru")
    def __init__(self, config_file: Union[str, ConfigParser]):
        """
        Классификатор команд по заданным категориям.

        :param config_file: Файл конфигурации.
        """
        self.calc = Calculator(None, config_file)
        self.cmds = {}
        self.tokens = {}

    def add_command(self, command: str, parametrs: Set[Parameter], category: str, tokens: Set[Union[Tuple[str], str]]):
        """
        Добавление типа команд.

        :param command: Пример команды.
        :param parametrs: Параметры, которые необходимо из команды извлекать.
        :param category: Категория команды (для схожих типов команд).
        :param tokens: Токены команды. Если в проверяемой команде не присутствует хотябы один токен - команда точно не принадлежит этому типу.
        В качестве токена может передаваться tuple. Тогда будет проверяться наличие хотябы одной из строк tuple-а в команде.
        """
        command = command.lower()
        cmd = " ".join(sorted(command.split()))
        self.cmds[cmd] = (command, parametrs, category)
        self.tokens[cmd] = tokens

    def get_params_by_command(self, command: str) -> Tuple[str, List[Union[int, str, float]]]:
        """
        Распарсить команду.

        :param command: Команда
        :return: (категория, [*параметры])
        """
        command = command.lower()
        cmd = self.find_nearest_command(command, raw=True)
        if cmd is None:
            return "", []
        cmd = cmd[0]
        ans = []
        _, parametrs, category = self.cmds[cmd]
        for _type in parametrs:
            if _type == IntParametr:
                ans += map(int, re.findall("\d+", command))
            elif _type == FloatParametr:
                ans += map(float, re.findall("\d*.\d+", command))
            elif _type == StringParamtr:
                passif = cmd.split()
                for ss in command.split():
                    if self.correct_gramatic(ss) and nearest_string(passif, ss) is None:
                        ans.append(self.to_simple_form(ss))
        return category, ans

    def add_commands(self, commands: List[str], parametrs: Set[Parameter], category: str, tokens: Set[Union[Tuple[str], str]]):
        """
        Добавление схожих типов команд.

        :param commands: Примеры команд.
        :param parametrs: Параметры, которые необходимо из команды извлекать.
        :param category: Категория команды (для схожих типов команд).
        :param tokens: Токены команды. Если в проверяемой команде не присутствует хотябы один токен - команда точно не принадлежит этому типу.
        В качестве токена может передаваться tuple. Тогда будет проверяться наличие хотябы одной из строк tuple-а в команде.
        """
        for c in commands:
            self.add_command(c.lower(), parametrs, category, tokens)


    def find_nearest_command(self, command: str, raw: bool = False):
        """
        Возвращает тип команды наидолее похожий на

        :param command: Команда.
        :param raw: Служебный параметр. Лучше его не трогать.
        :return:
        """
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

    def correct_gramatic(self, string: str):
        parsed = self.morph.parse(string)
        if not parsed:
            return False
        return parsed[0].tag.POS not in ["ADJS", "COMP", "VERB", "INFN", "PRTS", "GRND", "ADVB", "NPRO", "PRED", "PREP", "CONJ", "PRCL", "INTJ"]

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

    def to_simple_form(self, string: str) -> str:
        parsed = self.morph.parse(string)
        if not parsed:
            return ""
        return parsed[0].normal_form
