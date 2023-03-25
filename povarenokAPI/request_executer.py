import calendar
import string
import time
from configparser import ConfigParser
from typing import List, Any

import requests
from bs4 import BeautifulSoup
from lxml import etree

from povarenokAPI.errors import *


class RequestExecuter:
    def __init__(self, parser: ConfigParser, host: str = None):
        """
        Красиво обращается к API.
        :param parser: Файл с константами - или открытый ConfigParser, или путь к файлу.
        :param host: Хост, с которого совершаются запросы
        """
        self.config = parser
        self.host = host if host is not None else self.config.get("BASE", "host")
        self.headers = {}

    # noinspection PyShadowingBuiltins
    def execute_request(self, request_name: str, data: dict = None, headers: dict = None, section: str = "URL",
                        format=None, **kwargs) -> requests.Response:
        """
        Красивое обращение к API.

        :param format: При необходимости форматирования запроса.
        :param request_name: Имя запроса в файле.
        :param data: Даннве запроса.
        :param headers: Заголовки запроса.
        :param section: Секция в файле, где лежат запросы.
        :param kwargs: Всякая прочая хрень для request.get или request.post
        :return: Возвращает типа результат.
        """
        if format is None:
            format = {}
        if data is None:
            data = {}
        if headers is None:
            headers = self.headers
        url, method = self.config.get(section, request_name).split(",")
        if method == "get":
            args = "?" + "&".join(f"{i}={j}" for i, j in data.items())
            return requests.get(f"{self.host}{url.format(**format)}{args}", headers=headers, **kwargs)
        elif method == "post":
            return requests.post(f"{self.host}{url.format(**format)}", data=data, headers=headers, **kwargs)
        else:
            raise UnknownMethodError


class Atom:
    def __init__(self, config_file, host):
        if type(config_file) == ConfigParser:
            self.config = config_file
        else:
            self.config: ConfigParser = ConfigParser()
            self.config.read(config_file)
        self.executer: RequestExecuter = RequestExecuter(self.config, host=host)
        self.config_file: str = config_file

    # noinspection PyShadowingBuiltins
    def execute_request(self, request_name: str, data: dict = None, headers: dict = None, section: str = "URL",
                        format=None, **kwargs) -> BeautifulSoup:
        responce = self.executer.execute_request(request_name, data=data, headers=headers, section=section,
                        format=format, **kwargs)
        return BeautifulSoup(responce.text, features="lxml")

    @staticmethod
    def find_by_xpath(soup: BeautifulSoup, xpath: str) -> List[etree._Element]:
        """
        ПОлучить список элементов по XPATH.

        :param soup: Откуда получаем элементы.
        :param xpath: XPATH.
        :return: Список элементов
        """
        dom = etree.HTML(str(soup))
        return list(dom.xpath(xpath))

    @staticmethod
    def get_list_attr(arr: List[Any], param: str, default: Any = None, idx: int = 0) -> Any:
        """
        Если в массиве arr есть элемент с индексом idx, то возвращает его параметр param, иначе defaault\
        """
        if len(arr) > idx:
            return getattr(arr[idx], param)
        return default

    @staticmethod
    def quote(s: str) -> str:
        """
        Кодирование запросов для поиска.

        :param s: Страка, которую надо закодировать.
        :return: Закодированная строка.
        """
        s = list(map(lambda x: hex(ord(x) - 848)[-2:].upper() if x not in string.printable else x, s))
        s = list(map("%".__add__, s))
        return "".join(s).replace("% ", "+")

    @property
    def timestamp(self):
        return calendar.timegm(time.gmtime())
