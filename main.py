import os
from pprint import pprint

from povarenokAPI import get_author_gender
from povarenokAPI.finder import RecpieFinder
from povarenokAPI.recpie import Recpie
from utils import Calculator
from utils.command_classificer import *

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

# Перевод в единиц измерения
c = Calculator("./utils/calc.json", config_file)
# Намеренно допущены ошибки
print(c.translate(10, "Метры", "мимиметры"))
print(c.translate(100, "Фаренготик", "Цельсий"))
print(c.translate(100, "градусников по реюмке", "Цельсий"))
# Несуществующие величины
print(c.translate(-1, "абвгдеё", "жзиклмн"))
print(c.translate(5, "метров", "световых лет"))
# Сыпучие продукты
print(c.get_grammes_by_ml("Мука", 50))
print(c.get_grammes_by_ml("Мёд", 50))
# Неточно написанный продукт (марципан)
print(c.get_grammes_by_ml("Марцип", 50))
# Несуществующий продукт
print(c.get_grammes_by_ml("абакаба", 50))

# Пример использования классияикатора команд
c = CommandClassificer(config_file)
c.add_commands([
    "поставь таймер на XX минут",
    "таймер на XX минут",
    "засеки XX минут",
    "отмерь XX минут",
    "скажи когда пройдёт XX минут"
], {IntParametr}, "minutes timer", {("тайм", "отмер", "засек", "пройд"), "мин"})
c.add_commands([
    "поставь таймер на X часа",
    "таймер на X часа",
    "засеки X часа",
    "отмерь X часа",
    "скажи когда пройдёт X часа",
], {IntParametr}, "hour timer", {("тайм", "отмер", "засек", "пройд"), "час"})
c.add_commands([
    "найди рецепт SSSSSSSSSSSS",
    "какой рецепт у SSSSSSSSSSSS",
    "поиск рецепта SSSSSSSSSS"
], {StringParamtr}, "find recpie", {"рецепт"})

print(c.get_params_by_command("поставь пожалуйста таймер на 25 минут"))
print(c.get_params_by_command("алисочка поставь таймер на 3 часика"))

print(c.get_params_by_command("Найди мне рецепт борща"))
print(c.get_params_by_command("слышь книга поваренная какой там рецепт у борща"))