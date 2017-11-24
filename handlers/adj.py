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


def adj_nom_infl(s, decl):

    if decl in ('a', 'o'):
        return 'Ъ'

    else:
        if s.endswith(lib.cons_soft + lib.cons_hush):
            return 'Ь'
        else:
            return 'И'


def adj_pron_infl(s, decl):

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
        s_old = tools.find_stem(form, (new_decl, case, num, gen), lib.nom_infl)
    else:
        s_old = tools.find_stem(form, (new_decl, case, num, gen), lib.pron_infl)

    s_new = s_old

    if s_new != 'NONE':
        # Суффиксы сравнительной степени
        if pos == 'прил/ср':
            s_new = de_comp_suff(s_new, case, num, gen)

        # Плюс-минус
        s_new = tools.plus_minus(s_new, nb)

        # Отмена палатализации
        if '*' in nb:
            s_new = tools.de_palat(s_new, decl, new_decl)

        # Прояснение/исчезновение редуцированных
        if (any(tag in nb for tag in ('+о', '+е', '-о', '-е'))
                or adj_noun_tools.reduction_on(pos, new_decl, case, num, gen)):
            s_new = adj_noun_tools.de_reduce(s_new, pos, decl, nb)

        # Возвращение маркера одушевлённости
        if prop:
            s_old = '*' + s_old
            s_new = '*' + s_new

        # Нахождение флексии
        if decl not in ('м', 'тв'):
            infl = adj_nom_infl(s_new, decl)
        else:
            infl = adj_pron_infl(s_new, decl)

    else:
        infl = ''

    return (s_old, s_new), infl
