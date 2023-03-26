from typing import Literal

from .recpie import Recpie
from .finder import RecpieFinder
from .request_executer import Atom


def get_author_gender(name: str, config_file) -> Literal["male", "female"]:
    """
    Определение гендера автора.

    :param name: Ник автора.
    :param config_file: Файл конфигурации.
    :return: Гендер автора ("male" или "female")
    """
    a = Atom(config_file, "https://www.spletenie.ru")
    page = a.execute_request("getAuthor", format={"name": name})
    if a.find_by_xpath(page, "//div[@class='data girl']"):
        return "female"
    return "male"
