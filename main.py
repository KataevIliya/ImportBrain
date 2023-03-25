import os
from pprint import pprint

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

# Пример поиска по имени (сортировка по дате)
f = RecpieFinder.find_by_name("Селдь под шубой", config_file, orderby=3)
pprint(f.get_results())

# Пример поиска по ингредиентам (Селдь, рис; без Моркови; кухня русская)
f2 = RecpieFinder.find_by_ingredients(["Селдь", "Рис"], ["Морковь"], config_file, cat="Русская")
pprint(f2.get_results())