import re
from configparser import ConfigParser
from typing import Union, List, Tuple, Dict

from povarenokAPI.request_executer import Atom


class Recpie(Atom):
    find_digits   = re.compile("\d+\.*\d*")
    find_words    = re.compile("[A-Za-zА-Яа-я]+")
    check_word    = re.compile("[A-Za-zА-Яа-я0-9]+")
    replacable    = "\n\r\t "
    def __init__(
            self,
            id: int,
            config_file: Union[str, ConfigParser],
            host: str = None):
        """
        Класс для получения данных о рецепте.

        :param id: ID рецепта.
        :param config_file: Файл конфигурации.
        :param host: Хост для совершения запросов.
        """
        super().__init__(config_file, host)
        self.id = id
        self.soup = self.execute_request("getRecpie", format={"id": self.id})

    def get_author(self) -> str:
        """
        Получить автора рецепта.

        :return: Ник автора.
        """
        author = str(self.get_list_attr(self.find_by_xpath(self.soup, "//span[@itemprop='author']/ancestor::a"), "attrib", {"href": "/nan/povarenok/"})["href"].strip("/").split("/")[-1])
        return author

    def get_description(self) -> str:
        """
        Получить описание рецерта.

        :return: Описание рецепта.
        """
        description = self.get_list_attr(self.find_by_xpath(self.soup, "//div[@itemprop='description']/p"), "text", "")
        return description

    def get_ingridients(self) -> List[Tuple[str, str]]:
        """
        ПОлучение списка ингредиентов.

        :return: Выводится список пар (название ингредиента, количество ингредиента)
        """
        ings = self.find_by_xpath(self.soup, "//li[@itemprop='recipeIngredient']")
        ings = [
            (
                self.get_list_attr(i.xpath("./a/span"), "text", ""),
                self.get_list_attr(i.xpath("./fr") + i.xpath("./span"), "text", ""))
            for i in ings
        ]
        return ings

    def get_nutrition(self) -> Dict[str, Tuple[float, str]]:
        """
        ПОлучение пищевой ценности.

        :return: Словарь вида {
            "calories":            (количество, еденица измерений)  # калории
            "proteinContent":      (количество, кдкница измерений)  # белки
            "fatContent":          (количество, кдкница измерений)  # жиры
            "carbohydrateContent": (количество, кдкница измерений)  # углеводы
        }
        """
        data = {
            "calories":            (float("nan"), "ккал"),
            "proteinContent":      (float("nan"), "г"),
            "fatContent":          (float("nan"), "г"),
            "carbohydrateContent": (float("nan"), "г")
        }
        try:
            nuts = self.find_by_xpath(self.soup, "//div[@itemprop='nutrition']/table")[0]
        except IndexError:
            return data
        for t in data.keys():
            try:
                fr = nuts.xpath(f"//strong[@itemprop='{t}']")[0].text
                data[t] = float(self.find_digits.findall(fr)[0]), self.find_words.findall(fr)[0]
            except (IndexError, StopIteration):
                pass
        return data

    def get_recpie(self) -> List[str]:
        """
        Передаёт список шагов текущего рецепта.

        :return: Список шагов.
        """
        raw_recpie = self.find_by_xpath(self.soup, "//ul[@itemprop='recipeInstructions']/*/div/p/text()")
        if not raw_recpie:
            raw_recpie = self.find_by_xpath(self.soup,
                                            "//h2/text()[contains(.,'Рецепт')]/ancestor::h2/following-sibling::div[not(@class='video-bl')]/text()")
        recpie = []
        for step in raw_recpie:
            if self.check_word.findall(str(step)):
                recpie.append(str(step).strip(self.replacable))
        return recpie
