import re
import lib
import tools
from handlers import Nom
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


def main(token):
    # Извлечение данных по токену
    gr = Nom(token)

    # Стемминг
    if gr.d_old not in ('м', 'тв'):
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)
    else:
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.pron_infl)

    s_new = s_old

    if s_new == 'NONE':
        return ('', 'NONE'), ''

    # Суффиксы сравнительной степени
    if gr.comp:
        s_new = de_comp_suff(s_new, gr.case, gr.num, gr.gen)

    # Плюс-минус
    s_new = tools.plus_minus(s_new, gr.nb)

    # Отмена палатализации
    if '*' in gr.nb:
        s_new = tools.de_palat(s_new, gr.pos, (gr.d_old, gr.d_new))

    # Удаление редуцированных в конечном слоге основы (всегда слабом)
    if (any(tag in gr.nb for tag in ('-о', '-е')) or s_new.endswith('ЕН')
            and tools.reduction_on(gr.pos, gr.d_new, gr.case, gr.num, gr.gen)):
        s_new = s_new[:-2] + s_new[-1]

    # TODO: заменить минус в '-о' и '-е' на плюс и внести в разметку (в таком случае не удалять)

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
