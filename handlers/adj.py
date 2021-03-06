import re
import lib
import tools
from handlers.noun import noun_infl


def de_comp_suff(s, case, num, gen):

    if (case, num, gen) not in (('им', 'ед', 'м'), ('им', 'ед', 'ср')):
        suf = re.search('[ИЪЬ]?Ш$', s)
        if suf:
            s = s[:-len(suf.group())]

    return s


def adj_pron_infl(s, decl):

    if decl in ('a', 'o', 'тв'):
        if s.endswith(lib.cons_palat):
            return 'ИИ'
        else:
            return 'ЫИ'

    else:
        if s.endswith(lib.vows):
            return 'И'
        else:
            return 'ИИ'


def main(gr):
    # Стемминг
    if gr.d_old not in ('м', 'тв'):
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)
    else:
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.pron_infl)

    s_new = s_old

    if s_new == 'NONE':
        return ('', 'NONE'), ''

    # Суффиксы сравнительной степени
    if gr.pos == 'прил/ср':
        s_new = de_comp_suff(s_new, gr.case, gr.num, gr.gen)

    # Плюс-минус
    s_new = tools.plus_minus(s_new, gr.nb)

    # Вторая палатализация
    if '*' in gr.nb and s_new[-1] in 'ЦЗСТ':
        s_new = s_new[:-1] + lib.palat_2[s_new[-1]]

    # Удаление прояснённых редуцированных
    if '-о' in gr.nb or '-е' in gr.nb:
        s_new = s_new[:-2] + s_new[-1]

    # Возвращение маркера одушевлённости
    if gr.prop:
        s_old = '*' + s_old
        s_new = '*' + s_new

    # Нахождение флексии
    if gr.prop and gr.d_old not in ('м', 'тв'):
        infl = noun_infl(s_new, gr.pt, gr.d_old, gr.gen)
    else:
        infl = adj_pron_infl(s_new, gr.d_old)

    return (s_old, s_new), infl
