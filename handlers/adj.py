import re
import lib
import tools
from handlers import adj_noun_tools


def de_comp_suff(s, case, num, gen):

    if (case, num, gen) not in (('им', 'ед', 'м'), ('им', 'ед', 'ср')):
        suf = re.search('[ИЪЬ]Ш$', s)
        if suf:
            s = s[:-len(suf.group())]

    if not s.endswith(('+', 'А', 'Е')):
        s += 'И'

    return s


def adj_nom_fl(s, decl):

    if decl in ('a', 'o'):
        return 'Ъ'

    else:
        if s.endswith(lib.cons_soft + lib.cons_hush):
            return 'Ь'
        else:
            return 'И'


def adj_pron_fl(s, decl):

    if decl == 'тв':
        if s.endswith(lib.cons_palat):
            return 'ИИ'
        else:
            return 'ЫИ'

    else:
        if s.endswith(lib.vows):
            return 'И'
        else:
            return 'ИИ'


def main(token):
    # Извлечение данных по токену
    form, prop, pos, decl, new_decl, case, num, pt, gen, nb = adj_noun_tools.get_params(token)

    # Стемминг
    if decl not in ('м', 'тв'):
        stem = tools.find_stem(form, (new_decl, case, num, gen), lib.nom_infl)
    else:
        stem = tools.find_stem(form, (new_decl, case, num, gen), lib.pron_infl)

    if stem != 'NONE':
        # Суффиксы сравнительной степени
        if pos == 'прил/ср':
            stem = de_comp_suff(stem, case, num, gen)

        # Плюс-минус
        stem = tools.plus_minus(stem, nb)

        # Отмена палатализации
        if '*' in nb:
            stem = tools.de_palat(stem, decl, new_decl)

        # Прояснение/исчезновение редуцированных
        if (any(tag in nb for tag in ('+о', '+е', '-о', '-е'))
                or adj_noun_tools.reduction_on(pos, new_decl, case, num, gen)):
            stem = adj_noun_tools.de_reduce(stem, pos, decl, nb)

        # Возвращение маркера одушевлённости
        if prop:
            stem = '*' + stem

        # Нахождение флексии
        if decl not in ('м', 'тв'):
            fl = adj_nom_fl(stem, decl)
        else:
            fl = adj_pron_fl(stem, decl)

    else:
        fl = ''

    return stem, fl
