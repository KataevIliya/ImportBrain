from configparser import ConfigParser
from typing import Tuple, Union

from pint import UnitRegistry
import json

from povarenokAPI import RecpieFinder
from .intuitive_calc import IntuitiveCalcAddon
from .levi import nearest_string


class Calculator:
    ureg = UnitRegistry()
    ureg.define('spoon = 18 * ml')
    ureg.define('tee_spoon = 5 * ml = tspon')
    ureg.define('cap = 250 * ml')
    ureg.define('glass = 300 * ml')
    russian_meters = {
        "чайная ложка": "tee_spoon",
        "маленькая ложка": "tee_spoon",
        "столовая ложка": "spoon",
        "десертная ложка": "spoon",
        "ложка": "spoon",
        "стакан": "glass",
        "гранённый стакан": "glass",
        "столовый стакан": "glass",
        "стаканчик": "glass",
        "кухонный стакан": "glass",
        "чайная чашка": "cap",
        "чашка": "cap",
        "кружка": "cap",
        "чашечка": "cap",
        "кружечка": "cap",
        "мг": "mg",
        "миллиграмм": "mgram",
        "г": "g",
        "грамм": "gram",
        "кг": "kg",
        "килограмм": "kilogram",
        "мл": "ml",
        "миллилитр": "mliter",
        "л": "l",
        "литр": "liter",
        "м": "m",
        "метр": "meter",
        "см": "cm",
        "сантиметр": "cmeter",
        "дм": "dm",
        "дециметр": "dmeter",
        "мм": "mm",
        "миллиметр": "mmeter",
        "градус по цельсию": "degree_Celsius",
        "цельсий": "degree_Celsius",
        "градус по фаренгейту": "degree_Fahrenheit",
        "фаренгейт": "degree_Fahrenheit",
        "градус по реомюру": "degree_Reaumur",
        "реомюр": "degree_Reaumur",
        "градус по кельвину": "kelvin",
        "кельвин": "kelvin",
    }
    def __init__(self, calc_file_name: Union[str, None], config_file: Union[str, ConfigParser]):
        try:
            with open(calc_file_name, "r", encoding="utf-8") as f:
                self.calc = json.load(f)
        except (FileNotFoundError, TypeError):
            self.calc = None
        self.config_file = config_file
        self.ic = IntuitiveCalcAddon(self)

    def translate(self, value: float, _from: str, to: str) -> Tuple[float, Tuple[str, str]]:
        """
        Перевод одних единиц измерения в другие.

        :param value: Сколько
        :param _from: Чего
        :param to: Переводим во что
        :return: Результат перевода
        """
        f = nearest_string(self.russian_meters.keys(), _from.lower())
        t = nearest_string(self.russian_meters.keys(), to.lower())
        if None in [f, t]:
            return float("nan"), (_from, to)
        return self.ureg.convert(value, self.russian_meters[f], self.russian_meters[t]), (f, t)

    def get_grammes_intuitive(self, command: str) -> Tuple[str, float]:
        return self.ic.get_grammes_intuitive(command)

    def get_grammes_by_ml(self, ingredient: str, ml: float) -> float:
        """
        Переводим массу сыпучего вещества в объём.

        :param ingredient: Чего
        :param ml: Сколько мл
        :return: Сколько грамм
        """
        if ingredient not in self.calc:
            ingredient = RecpieFinder.find_probably_ingredients(ingredient, self.config_file)
            if not len(ingredient):
                return float("nan")
            ingredient = ingredient[0]
        if ingredient not in self.calc:
            return float("nan")
        data = self.calc[ingredient]
        if str(ml) in data:
            return data[ml]
        return data["100"] * ml / 100

    def get_ml_by_grammes(self, ingredient: str, grammes: float) -> float:
        """
        Переводим объём сыпучего вещества в массу.

        :param ingredient: Чего
        :param grammes: Сколько грамм
        :return: Сколько мл
        """
        g100 = self.get_grammes_by_ml(ingredient, 100)
        return grammes * 100 / g100
