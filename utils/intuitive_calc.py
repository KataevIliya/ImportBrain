import re

from povarenokAPI import RecpieFinder
from utils.command_classificer import CommandClassificer, StringParamtr


cc = CommandClassificer()
cc.add_commands([
        "Какое количество S в S?",
        "Сколько граммов S в S?",
        "Какое количество S необходимо для наполнения S?",
        "Вес S в S?",
        "Какой вес S поместится в S?",
        "Сколько грамм S можно насыпать в S?",
        "Какое количество S можно поместить в этот S?",
        "Сколько граммов S необходимо, чтобы наполнить S?",
        "Какой вес должен иметь S в S?",
        "Сколько S необходимо, чтобы заполнить S?",
        "Сколько граммов S можно насыпать в S?",
        "Какое количество S необходимо для заполнения S?",
        "Сколько S помещается в S?"
], {StringParamtr}, "calculator", {("количе", "вес", "грам", "помещается")})

class IntuitiveCalcAddon:
    cap = ["чашк", "чайн"]
    glass = ["гранен", "гранён", "стакан"]
    tee_spoon = ["чайн", "ложк"]
    spoon = ["столов", "десертн", "ложк"]
    rf = {0: 5, 1: 250, 2: 300, 3: 18}
    all_patterns = list(set(cap + glass + tee_spoon + spoon))

    value_re = re.compile("(?:(?<=^)|(?<=\s))((милли)|(мили)|м)?л(итр)?(е|(ом)|а|у)?(?=(\s|$))")

    def __init__(self, calc: "Calculator"):
        self.calc = calc
        self.cc = cc

    def get_grammes_intuitive(self, command: str):
        a = self.cc.get_params_by_command(command)
        if not a[1]:
            return None
        pt = " ".join(a[1])
        category = -1
        for n, vr in enumerate([self.tee_spoon, self.cap, self.glass, self.spoon]):
            if any([i in pt for i in vr]):
                category = n
                break
        if category == -1:
            return None
        sa = set(a[1])
        for pat in self.all_patterns:
            for el in sa.copy():
                if pat in el:
                    sa.remove(el)
        ings = []
        for el in sa:
            ings += RecpieFinder.find_probably_ingredients(el, self.calc.config_file, return_empty=True)

        for ing in ings:
            if ing not in self.calc.calc:
                continue
            count = self.calc.get_grammes_by_ml(ing, self.rf[category])
            return count
        return None

