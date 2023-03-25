from _typeshed import Self
from configparser import ConfigParser
from typing import Union, List, Dict

from povarenokAPI.request_executer import Atom


class Constanter:
    """
    Контейнер для хранения множества необходимых величин.
    """
    # Параметры сортировки
    orderby = {
        0: "rating",  # Рейтинг рецепта
        1: "owner_rating",  # Рейтинг автора
        2: "views",  # Количество просмотров
        3: "reviews",  # Количество отзывов
        4: "comments",  # Количество комментариев
        5: "dt+desc",  # Дата рецепта (сначала новые)
        6: "dt+asc"  # Дата рецепта (сначала старые)
    }
    # Кухня
    kitchen = {
        "Все": 0,
        "Русская": 101,
        "Итальянская": 56,
        "Французская": 64,
        "Украинская": 104,
        "Американская": 108,
        "Немецкая": 59,
        "Китайская": 73,
        "Греческая": 54,
        "Турецкая": 78,
        "Испанская": 57,
        "Грузинская": 93,
        "Японская": 79,
        "Индийская": 72,
        "Английская": 47,
        "Корейская": 74,
        "Азербайджанская": 89,
        "Узбекская": 103,
        "Еврейская": 111,
        "Арабская": 85,
        "Мексиканская": 112,
        "Кавказская": 94,
        "Болгарская": 50,
        "Белорусская": 91,
        "Венгерская": 52,
        "Тайская": 77,
        "Армянская": 90,
        "Польская": 60,
        "Португальская": 61,
        "Магриба": 84,
        "Чешская": 65,
        "Шведская": 67,
        "Австрийская": 48,
        "Марокканская": 83,
        "Татарская": 115,
        "Швейцарская": 66,
        "Казахская": 95,
        "Молдавская": 100,
        "Финская": 63,
        "Латышская": 98,
        "Эстонская": 105,
        "Африканская": 80,
        "Сирийская": 86,
        "Австралийская": 106,
        "Вьетнамская": 71,
        "Норвежская": 70,
        "Канадская": 120,
        "Египетская": 81,
        "Литовская": 99,
        "Голландская": 53,
        "Югославская": 69,
        "Ирландская": 58,
        "Шотландская": 68,
        "Датская": 55,
        "Иранская": 119,
        "Аргентинская": 107,
        "Бразильская": 109,
        "Румынская": 62,
        "Кубинская": 113,
        "Малазийская": 75,
        "Таджикская": 102,
        "Абхазская": 88,
        "Бельгийская": 49,
        "Тунисская": 82,
        "Уральская": 114,
        "Коми": 97,
        "Чилийская": 116,
        "Бурятская": 92,
        "Перуанская": 117,
        "Гавайская": 110,
        "Иракская": 87,
        "Хорватская": 124,
        "Валлийская": 51,
        "Курдская": 118,
        "Монгольская": 76,
        "Калмыцкая": 96,
        "Башкирская": 123,
        "Афганская": 125,
        "Исландская": 122
    }
    # Категории
    cat = {
        "Все": 0,
        "Блюда из лаваша": 228,
        "Бульоны и супы": 2,
        "Выпечка": 25,
        "Горячие блюда": 6,
        "Блюда для аэрогриля": 227,
        "Блюда для мультиварки": 308,
        "Блюда для пароварки": 247,
        "Десерты": 30,
        "Заготовки": 35,
        "Закуски": 15,
        "Каши": 55,
        "Маринад, панировка": 356,
        "Напитки": 19,
        "Молочные продукты": 289,
        "Салаты": 12,
        "Соусы": 23,
        "Украшения для блюд": 187
    }


class RecpieFinder(Atom, Constanter):
    def __init__(
            self,
            params: dict,
            config_file: Union[str, ConfigParser],
            host: str = None):
        """
        Класс для поиска по имени и ингредиентам.

        :param params: Параметры поиска.
        :param config_file: Файл конфигурации.
        :param host: Хост для совершения запросов.
        """
        super().__init__(config_file, host)
        self.params = params
        self.soup = self.execute_request("findRecpie", data=params)

    def get_results(self) -> List[Dict[str: Union[str, int, List[str]]]]:
        """
        Получить результаты поиска.

        :return: Словарь следующего формата: {
            "id": ID рецепта,
            "title": Название рецепта,
            "cetegories": Категории к которым принадлежит рецепт,
            "ingredients": Ингредиенты рецепта,
        }
        """
        recpies = self.find_by_xpath(self.soup, "//article[@class='item-bl']")
        results = []
        for r in recpies:
            idt = int(self.get_list_attr(r.xpath("./h2/a"), "attrib", {"href": "/0/"})["href"].split("/")[-2])
            title = self.get_list_attr(r.xpath("./h2/a"), "text", "")
            cats = list(map(str, r.xpath("./div[@class='article-breadcrumbs']/p/span/a/text()")))
            ings = list(map(str, r.xpath("./div[@class='article-tags']/div/div/p/span/a/text()")))
            results.append({"id": idt, "title": title, "cetegories": cats, "ingredients": ings})
        return results

    @classmethod
    def find_by_name(cls, name: str, config_file: Union[str, ConfigParser], host: str = None, orderby: int = 0) -> Self:
        """
        Поиск рецептов по названию.

        :param name: Название (или часть названия) по которому производится поиск.
        :param config_file: Файл конфигурации.
        :param host: Хост для совершения запросов.
        :param orderby: Сортировка ответов (смотри виды в Constanter)
        :return: RecpieFinder выполнивший поиск по заданным параметрам.
        """
        return cls({"name": cls.quote(name), "orderby": cls.orderby[orderby]}, config_file, host=host)

    @classmethod
    def find_by_ingredients(
            cls, need_to_be: List[str], doesnt_be: List[str],
            config_file: Union[str, ConfigParser], host: str = None,
            kitchen: str = "Все", cat: str = "Все", orderby: int = 0
    ) -> Self:
        """
        Поиск рецептов по ингредиентам.

        :param need_to_be: Какие ингредиенты должны быть.
        :param doesnt_be: А каких быть не должно.
        :param config_file: Файл конфигурации.
        :param host: Хост для совершения запросов.
        :param kitchen: Кухня (смотри виды в Constanter)
        :param cat: Катенория (смотри виды в Constanter)
        :param orderby: Сортировка ответов (смотри виды в Constanter)
        :return: RecpieFinder выполнивший поиск по заданным параметрам.
        """
        return cls(
            {
                "ing": ", ".join(map(cls.quote, need_to_be)),
                "ing_exc": ", ".join(map(cls.quote, doesnt_be)),
                "kitchen": cls.kitchen[kitchen],
                "orderby": cls.orderby[orderby],
                "cat": cls.cat[cat]
            }, config_file, host=host)


