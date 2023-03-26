import os
from pprint import pprint

from povarenokAPI import get_author_gender
from povarenokAPI.finder import RecpieFinder
from povarenokAPI.recpie import Recpie

config_file = os.path.join(
    *os.path.split(__file__)[:-1],
    "constants.ini"
)


# Пример использования Recpie
r = Recpie(111324, config_file)
print(r.get_ingridients())
print(r.get_nutrition())
pprint(r.get_recpie())
pprint(r.get_description())

# Пример поиска по имени (сортировка по дате)
f = RecpieFinder.find_by_name("Селдь под шубой", config_file, orderby=3)
pprint(f.get_results())

# Пример поиска по ингредиентам (Селдь, рис; без Моркови; кухня русская)
f2 = RecpieFinder.find_by_ingredients(["Селёдка", "Рис"], ["Морковь"], config_file, kitchen="Русская")
pprint(f2.get_results())

# Поиск похожих по названию ингредиентов
f = RecpieFinder.find_probably_ingredients("Фа", config_file)
print(f)

# Определение гендера автора
print(get_author_gender("olchik40", config_file))
print(get_author_gender("ndemon", config_file))
