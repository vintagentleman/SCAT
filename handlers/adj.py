import re
import lib
import tools
from handlers import Nom


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
    gr = Nom(token)

    # Стемминг
    if gr.d_old not in ('м', 'тв'):
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)
    else:
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.pron_infl)

    s_new = s_old

    if s_new != 'NONE':
        # Суффиксы сравнительной степени
        if gr.pos == 'прил/ср':
            s_new = de_comp_suff(s_new, gr.case, gr.num, gr.gen)

        # Плюс-минус
        s_new = tools.plus_minus(s_new, gr.nb)

        # Отмена палатализации
        if '*' in gr.nb:
            s_new = tools.de_palat(s_new, gr.pos, (gr.d_old, gr.d_new))

        # Прояснение/исчезновение редуцированных
        if (any(tag in gr.nb for tag in ('+о', '+е', '-о', '-е'))
                or tools.reduction_on(gr.pos, gr.d_new, gr.case, gr.num, gr.gen)):
            s_new = tools.de_reduce(s_new, gr.pos, gr.d_old, gr.nb)

        # Возвращение маркера одушевлённости
        if gr.prop:
            s_old = '*' + s_old
            s_new = '*' + s_new

        # Нахождение флексии
        if gr.d_old not in ('м', 'тв'):
            infl = adj_nom_infl(s_new, gr.d_old)
        else:
            infl = adj_pron_infl(s_new, gr.d_old)

    else:
        infl = ''

    return (s_old, s_new), infl
